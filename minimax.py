import random
import time

from heuristic import evaluate_board


def minimax(
    board,
    current_player,
    ai_player,
    depth,
    alpha,
    beta,
    heuristic_name,
    stats,
    ply=0,
):

    opponent = "O" if ai_player == "X" else "X"

    # Count this search node.
    stats["nodes"] += 1

    # Check for a terminal position.
    winner = check_winner(board)

    if winner == ai_player:
        return 100 - ply

    if winner == opponent:
        return -100 + ply

    if " " not in board:
        return 0

    # Stop searching when the depth limit is reached.
    if depth == 0:
        return evaluate_board(
            board,
            ai_player,
            heuristic_name,
        )

    valid_moves = [
        index
        for index, cell in enumerate(board)
        if cell == " "
    ]

    if current_player == ai_player:
        best_score = float("-inf")

        for move in valid_moves:
            board[move] = current_player

            score = minimax(
                board,
                opponent,
                ai_player,
                depth - 1,
                alpha,
                beta,
                heuristic_name,
                stats,
                ply + 1,
            )

            board[move] = " "
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)

            if beta <= alpha:
                stats["pruned"] += len(valid_moves) - (
                    valid_moves.index(move) + 1
                )
                break

        return best_score

    else:
        best_score = float("inf")

        for move in valid_moves:
            board[move] = current_player

            score = minimax(
                board,
                ai_player,
                ai_player,
                depth - 1,
                alpha,
                beta,
                heuristic_name,
                stats,
                ply + 1,
            )

            board[move] = " "
            best_score = min(best_score, score)
            beta = min(beta, best_score)

            if beta <= alpha:
                stats["pruned"] += len(valid_moves) - (
                    valid_moves.index(move) + 1
                )
                break

        return best_score


def check_winner(board):
    winning_lines = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]

    for a, b, c in winning_lines:
        if (
            board[a] != " "
            and board[a] == board[b]
            and board[b] == board[c]
        ):
            return board[a]

    return None


def choose_best_move(
    board,
    player,
    depth=4,
    heuristic_name="H1",
    seed=None,
):

    if depth < 1:
        raise ValueError("Search depth must be at least 1.")

    valid_moves = [
        index
        for index, cell in enumerate(board)
        if cell == " "
    ]

    if not valid_moves:
        return None, {
            "nodes": 0,
            "pruned": 0,
            "time": 0.0,
        }

    rng = random.Random(seed)
    opponent = "O" if player == "X" else "X"

    stats = {
        "nodes": 0,
        "pruned": 0,
        "time": 0.0,
    }

    start_time = time.perf_counter()

    best_score = float("-inf")
    best_moves = []

    for move in valid_moves:
        board[move] = player

        move_stats = {
            "nodes": 0,
            "pruned": 0,
        }

        score = minimax(
            board,
            opponent,
            player,
            depth - 1,
            float("-inf"),
            float("inf"),
            heuristic_name,
            move_stats,
            ply=1,
        )

        board[move] = " "

        stats["nodes"] += move_stats["nodes"]
        stats["pruned"] += move_stats["pruned"]

        if score > best_score:
            best_score = score
            best_moves = [move]

        elif score == best_score:
            best_moves.append(move)

    stats["time"] = time.perf_counter() - start_time

    # Break ties between equally good moves.
    return rng.choice(best_moves), stats