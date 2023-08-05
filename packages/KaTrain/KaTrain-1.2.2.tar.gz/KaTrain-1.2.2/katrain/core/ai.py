import heapq
import math
import random
import time
from typing import Dict, List, Tuple

from katrain.core.utils import var_to_grid
from katrain.core.constants import (
    OUTPUT_INFO,
    OUTPUT_DEBUG,
    AI_STRATEGIES_POLICY,
    AI_POLICY,
    AI_WEIGHTED,
    AI_STRATEGIES_PICK,
    AI_JIGO,
    AI_SCORELOSS,
    AI_DEFAULT,
    AI_INFLUENCE,
    AI_LOCAL,
    AI_TENUKI,
    AI_TERRITORY,
    AI_PICK,
    AI_RANK,
)
from katrain.core.game import Game, GameNode, Move


def weighted_selection_without_replacement(items: List[Tuple], pick_n: int) -> List[Tuple]:
    """For a list of tuples where the second element is a weight, returns random items with those weights, without replacement."""
    elt = [(math.log(random.random()) / item[1], item) for item in items]  # magic
    return [e[1] for e in heapq.nlargest(pick_n, elt)]  # NB fine if too small


def dirichlet_noise(num, dir_alpha=0.3):
    sample = [random.gammavariate(dir_alpha, 1) for _ in range(num)]
    sum_sample = sum(sample)
    return [s / sum_sample for s in sample]


def fmt_moves(moves: List[Tuple[float, Move]]):
    return ", ".join(f"{mv.gtp()} ({p:.2%})" for p, mv in moves)


def policy_weighted_move(policy_moves, lower_bound, weaken_fac):
    lower_bound, weaken_fac = max(0, lower_bound), max(0.01, weaken_fac)
    weighted_coords = [
        (pv, pv ** (1 / weaken_fac), move) for pv, move in policy_moves if pv > lower_bound and not move.is_pass
    ]
    if weighted_coords:
        top = weighted_selection_without_replacement(weighted_coords, 1)[0]
        ai_thoughts = f"Playing policy-weighted random move {top[2].gtp()} ({top[0]:.1%}) from {len(weighted_coords)} moves above lower_bound of {lower_bound:.1%}."
    else:
        top = policy_moves[0]
        ai_thoughts = f"Playing top policy move because no non-pass move > above lower_bound of {lower_bound:.1%}."
    return top[2], ai_thoughts


def generate_influence_territory_weights(ai_mode, ai_settings, policy_grid, size):
    thr_line = ai_settings["threshold"] - 1  # zero-based
    if ai_mode == AI_INFLUENCE:
        weight = lambda x, y: (1 / ai_settings["line_weight"]) ** (
            max(0, thr_line - min(size[0] - 1 - x, x)) + max(0, thr_line - min(size[1] - 1 - y, y))
        )
    else:
        weight = lambda x, y: (1 / ai_settings["line_weight"]) ** (
            max(0, min(size[0] - 1 - x, x, size[1] - 1 - y, y) - thr_line)
        )
    weighted_coords = [
        (policy_grid[y][x] * weight(x, y), weight(x, y), x, y)
        for x in range(size[0])
        for y in range(size[1])
        if policy_grid[y][x] > 0
    ]
    ai_thoughts = f"Generated weights for {ai_mode} according to weight factor {ai_settings['line_weight']} and distance from {thr_line + 1}th line. "
    return weighted_coords, ai_thoughts


def generate_local_tenuki_weights(ai_mode, ai_settings, policy_grid, cn, size):
    var = ai_settings["stddev"] ** 2
    mx, my = cn.move.coords
    weighted_coords = [
        (policy_grid[y][x], math.exp(-0.5 * ((x - mx) ** 2 + (y - my) ** 2) / var), x, y)
        for x in range(size[0])
        for y in range(size[1])
        if policy_grid[y][x] > 0
    ]
    ai_thoughts = f"Generated weights based on one minus gaussian with variance {var} around coordinates {mx},{my}. "
    if ai_mode == AI_TENUKI:
        weighted_coords = [(p, 1 - w, x, y) for p, w, x, y in weighted_coords]
        ai_thoughts = (
            f"Generated weights based on one minus gaussian with variance {var} around coordinates {mx},{my}. "
        )
    return weighted_coords, ai_thoughts


def generate_ai_move(game: Game, ai_mode: str, ai_settings: Dict) -> Tuple[Move, GameNode]:
    cn = game.current_node
    while not cn.analysis_ready:
        time.sleep(0.01)
        game.engines[cn.next_player].check_alive(exception_if_dead=True)

    ai_thoughts = ""
    if (ai_mode in AI_STRATEGIES_POLICY) and cn.policy:  # pure policy based move
        policy_moves = cn.policy_ranking
        pass_policy = cn.policy[-1]
        # dont make it jump around for the last few sensible non pass moves
        top_5_pass = any([polmove[1].is_pass for polmove in policy_moves[:5]])

        size = game.board_size
        policy_grid = var_to_grid(cn.policy, size)  # type: List[List[float]]
        top_policy_move = policy_moves[0][1]
        ai_thoughts += f"Using policy based strategy, base top 5 moves are {fmt_moves(policy_moves[:5])}. "
        if (ai_mode == AI_POLICY and cn.depth <= ai_settings["opening_moves"]) or (
            ai_mode in [AI_LOCAL, AI_TENUKI] and not (cn.move and cn.move.coords)
        ):
            ai_mode = AI_WEIGHTED
            ai_thoughts += f"Strategy override, using policy-weighted strategy instead. "
            ai_settings = {"pick_override": 0.9, "weaken_fac": 1, "lower_bound": 0.02}

        if top_5_pass:
            aimove = top_policy_move
            ai_thoughts += "Playing top one because one of them is pass."
        elif ai_mode == AI_POLICY:
            aimove = top_policy_move
            ai_thoughts += f"Playing top policy move {aimove.gtp()}."
        else:  # weighted or pick-based
            legal_policy_moves = [(pol, mv) for pol, mv in policy_moves if not mv.is_pass and pol > 0]
            board_squares = size[0] * size[1]
            if ai_mode == AI_RANK:  # calibrated, override from 0.8 at start to ~0.4 at full board
                override = 0.8 * (1 - 0.5 * (board_squares - len(legal_policy_moves)) / board_squares)
            else:
                override = ai_settings["pick_override"]

            if policy_moves[0][0] > override:
                aimove = top_policy_move
                ai_thoughts += f"Top policy move has weight > {override:.1%}, so overriding other strategies."
            elif ai_mode == AI_WEIGHTED:
                aimove, ai_thoughts = policy_weighted_move(
                    policy_moves, ai_settings["lower_bound"], ai_settings["weaken_fac"]
                )
            elif ai_mode in AI_STRATEGIES_PICK:

                if ai_mode != AI_RANK:
                    n_moves = int(ai_settings["pick_frac"] * len(legal_policy_moves) + ai_settings["pick_n"])
                else:
                    n_moves = int(round(board_squares / 361 * 10 ** (-0.05737 * ai_settings["kyu_rank"] + 1.9482)))

                if ai_mode in [AI_INFLUENCE, AI_TERRITORY, AI_LOCAL, AI_TENUKI]:
                    if cn.depth > ai_settings["endgame"] * board_squares:
                        weighted_coords = [(pol, 1, *mv.coords) for pol, mv in legal_policy_moves]
                        x_ai_thoughts = (
                            f"Generated equal weights as move number >= {ai_settings['endgame'] * size[0] * size[1]}. "
                        )
                        n_moves = int(max(n_moves, 0.5 * len(legal_policy_moves)))
                    elif ai_mode in [AI_INFLUENCE, AI_TERRITORY]:
                        weighted_coords, x_ai_thoughts = generate_influence_territory_weights(
                            ai_mode, ai_settings, policy_grid, size
                        )
                    else:  # ai_mode in [AI_LOCAL, AI_TENUKI]
                        weighted_coords, x_ai_thoughts = generate_local_tenuki_weights(
                            ai_mode, ai_settings, policy_grid, cn, size
                        )
                    ai_thoughts += x_ai_thoughts
                else:  # ai_mode in [AI_PICK, AI_RANK]:
                    weighted_coords = [
                        (policy_grid[y][x], 1, x, y)
                        for x in range(size[0])
                        for y in range(size[1])
                        if policy_grid[y][x] > 0
                    ]

                pick_moves = weighted_selection_without_replacement(weighted_coords, n_moves)
                ai_thoughts += f"Picked {min(n_moves,len(weighted_coords))} random moves according to weights. "

                if pick_moves:
                    new_top = [
                        (p, Move((x, y), player=cn.next_player)) for p, wt, x, y in heapq.nlargest(5, pick_moves)
                    ]
                    aimove = new_top[0][1]
                    ai_thoughts += f"Top 5 among these were {fmt_moves(new_top)} and picked top {aimove.gtp()}. "
                    if new_top[0][0] < pass_policy:
                        ai_thoughts += f"But found pass ({pass_policy:.2%} to be higher rated than {aimove.gtp()} ({new_top[0][0]:.2%}) so will play top policy move instead."
                        aimove = top_policy_move
                else:
                    aimove = top_policy_move
                    ai_thoughts += f"Pick policy strategy {ai_mode} failed to find legal moves, so is playing top policy move {aimove.gtp()}."
            else:
                raise ValueError(f"Unknown Policy-based AI mode {ai_mode}")
    else:  # Engine based move
        candidate_ai_moves = cn.candidate_moves
        top_cand = Move.from_gtp(candidate_ai_moves[0]["move"], player=cn.next_player)
        if top_cand.is_pass:  # don't play suicidal to balance score - pass when it's best
            aimove = top_cand
            ai_thoughts += f"Top move is pass, so passing regardless of strategy."
        else:
            if ai_mode == AI_JIGO:
                sign = cn.player_sign(cn.next_player)
                jigo_move = min(
                    candidate_ai_moves, key=lambda move: abs(sign * move["scoreLead"] - ai_settings["target_score"])
                )
                aimove = Move.from_gtp(jigo_move["move"], player=cn.next_player)
                ai_thoughts += f"Jigo strategy found {len(candidate_ai_moves)} candidate moves (best {top_cand.gtp()}) and chose {aimove.gtp()} as closest to 0.5 point win"
            elif ai_mode == AI_SCORELOSS:
                c = ai_settings["strength"]
                moves = [
                    (
                        d["pointsLost"],
                        math.exp(min(200, -c * max(0, d["pointsLost"]))),
                        Move.from_gtp(d["move"], player=cn.next_player),
                    )
                    for d in candidate_ai_moves
                ]
                topmove = weighted_selection_without_replacement(moves, 1)[0]
                aimove = topmove[2]
                ai_thoughts += f"ScoreLoss strategy found {len(candidate_ai_moves)} candidate moves (best {top_cand.gtp()}) and chose {aimove.gtp()} (weight {topmove[1]:.3f}, point loss {topmove[0]:.1f}) based on score weights."
            else:
                if ai_mode != AI_DEFAULT:
                    game.katrain.log(f"Unknown AI mode {ai_mode} or policy missing, using default.", OUTPUT_INFO)
                    ai_thoughts += f"Strategy {ai_mode} not found or unexpected fallback."
                aimove = top_cand
                ai_thoughts += f"Default strategy found {len(candidate_ai_moves)} moves returned from the engine and chose {aimove.gtp()} as top move"
    game.katrain.log(f"AI thoughts: {ai_thoughts}", OUTPUT_DEBUG)
    played_node = game.play(aimove)
    played_node.ai_thoughts = ai_thoughts
    return aimove, played_node
