from minimax import choose_best_move


class Agent:
    def __init__(
        self,
        name,
        symbol,
        depth,
        heuristic_name,
        seed=42,
    ):
        self.name = name
        self.symbol = symbol
        self.depth = depth
        self.heuristic_name = heuristic_name
        self.seed = seed

        self.total_nodes = 0
        self.total_pruned = 0
        self.total_time = 0.0
        self.move_number = 0

    def choose_move(self, board):
        move, stats = choose_best_move(
            board=board,
            player=self.symbol,
            depth=self.depth,
            heuristic_name=self.heuristic_name,
            seed=self.seed + self.move_number,
        )

        self.move_number += 1
        self.total_nodes += stats["nodes"]
        self.total_pruned += stats["pruned"]
        self.total_time += stats["time"]

        return move

    def reset_statistics(self):
        self.total_nodes = 0
        self.total_pruned = 0
        self.total_time = 0.0
        self.move_number = 0


def create_agents(depth=4, seed=42):
    nexus = Agent(
        name="NEXUS",
        symbol="X",
        depth=depth,
        heuristic_name="H1",
        seed=seed,
    )

    titan = Agent(
        name="TITAN",
        symbol="O",
        depth=depth,
        heuristic_name="H2",
        seed=seed + 100,
    )

    return nexus, titan