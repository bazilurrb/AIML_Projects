from game import TicTacToe

def evaluate_h1(board, player):

    opponent = "O" if player == "X" else "X"
    score = 0

    for a, b, c in TicTacToe.WINNING_LINES:
        line = [board[a], board[b], board[c]]

        player_count = line.count(player)
        opponent_count = line.count(opponent)
        empty_count = line.count(" ")

        if player_count == 3:
            return 100

        if opponent_count == 3:
            return -100

        if player_count == 2 and empty_count == 1:
            score += 10

        elif opponent_count == 2 and empty_count == 1:
            score -= 10

        elif player_count == 1 and empty_count == 2:
            score += 2

        elif opponent_count == 1 and empty_count == 2:
            score -= 2

    # Centre control
    if board[4] == player:
        score += 3
    elif board[4] == opponent:
        score -= 3

    # Corner control
    corners = [0, 2, 6, 8]

    for position in corners:
        if board[position] == player:
            score += 1
        elif board[position] == opponent:
            score -= 1

    return score


def evaluate_h2(board, player):
    opponent = "O" if player == "X" else "X"
    score = 0

    line_weights = {
        1: 3,
        2: 12,
        3: 100,
    }

    for a, b, c in TicTacToe.WINNING_LINES:
        line = [board[a], board[b], board[c]]

        player_count = line.count(player)
        opponent_count = line.count(opponent)
        empty_count = line.count(" ")

        # A line containing both players cannot be won
        # by either player.
        if player_count > 0 and opponent_count > 0:
            continue

        if opponent_count == 0 and player_count > 0:
            score += line_weights[player_count] * (
                1 if empty_count > 0 else 1
            )

        elif player_count == 0 and opponent_count > 0:
            score -= line_weights[opponent_count]

    # A small positional preference
    if board[4] == player:
        score += 2
    elif board[4] == opponent:
        score -= 2

    return score


def evaluate_board(board, player, heuristic_name="H1"):
    if heuristic_name == "H1":
        return evaluate_h1(board, player)

    if heuristic_name == "H2":
        return evaluate_h2(board, player)

    raise ValueError(
        f"Unknown heuristic: {heuristic_name}"
    )