class TicTacToe:

    WINNING_LINES = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]

    def __init__(self):
        self.board = [" "] * 9

    def get_valid_moves(self):
        return [
            index
            for index, cell in enumerate(self.board)
            if cell == " "
        ]

    def make_move(self, position, player):
        if player not in ("X", "O"):
            raise ValueError("Player must be X or O.")

        if position not in self.get_valid_moves():
            return False

        self.board[position] = player
        return True

    def check_winner(self):
        for a, b, c in self.WINNING_LINES:
            if (
                self.board[a] != " "
                and self.board[a] == self.board[b]
                and self.board[b] == self.board[c]
            ):
                return self.board[a]

        return None

    def is_draw(self):
        return (
            self.check_winner() is None
            and " " not in self.board
        )

    def is_terminal(self):
        return (
            self.check_winner() is not None
            or self.is_draw()
        )

    def display(self):
        cells = [
            str(i + 1) if value == " " else value
            for i, value in enumerate(self.board)
        ]

        print()
        print(f" {cells[0]} | {cells[1]} | {cells[2]}")
        print("---+---+---")
        print(f" {cells[3]} | {cells[4]} | {cells[5]}")
        print("---+---+---")
        print(f" {cells[6]} | {cells[7]} | {cells[8]}")
        print()