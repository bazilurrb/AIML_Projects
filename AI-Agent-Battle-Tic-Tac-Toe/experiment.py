import csv
import os
import time

from agents import Agent, create_agents
from game import TicTacToe


RESULTS_DIR = "results"
BATTLE_CSV = os.path.join(RESULTS_DIR, "results.csv")
DEPTH_CSV = os.path.join(
    RESULTS_DIR,
    "depth_experiment.csv",
)


def ensure_results_directory():
    os.makedirs(RESULTS_DIR, exist_ok=True)


def run_single_game(nexus, titan, first_agent):

    game = TicTacToe()
    nexus.reset_statistics()
    titan.reset_statistics()

    current_agent = first_agent
    move_count = 0
    start_time = time.perf_counter()

    while not game.is_terminal():
        move = current_agent.choose_move(game.board)

        if move is None:
            break

        game.make_move(move, current_agent.symbol)
        move_count += 1

        if game.is_terminal():
            break

        # Alternate between the two agents.
        if current_agent is nexus:
            current_agent = titan
        else:
            current_agent = nexus

    elapsed_time = time.perf_counter() - start_time
    winner_symbol = game.check_winner()

    if winner_symbol == nexus.symbol:
        winner = nexus.name
    elif winner_symbol == titan.symbol:
        winner = titan.name
    else:
        winner = "DRAW"

    result = {
        "winner": winner,
        "moves": move_count,
        "nexus_nodes": nexus.total_nodes,
        "titan_nodes": titan.total_nodes,
        "nexus_pruned": nexus.total_pruned,
        "titan_pruned": titan.total_pruned,
        "nexus_time_seconds": round(nexus.total_time, 6),
        "titan_time_seconds": round(titan.total_time, 6),
        "execution_time_seconds": round(elapsed_time, 6),
    }

    return result


def save_csv(filename, rows, fieldnames):
    ensure_results_directory()

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)


def calculate_summary(rows):
    total_games = len(rows)

    nexus_wins = sum(
        row["winner"] == "NEXUS" for row in rows
    )
    titan_wins = sum(
        row["winner"] == "TITAN" for row in rows
    )
    draws = sum(
        row["winner"] == "DRAW" for row in rows
    )

    def average(key):
        if not rows:
            return 0.0

        return sum(row[key] for row in rows) / len(rows)

    return {
        "Total games": total_games,
        "NEXUS wins": nexus_wins,
        "TITAN wins": titan_wins,
        "Draws": draws,
        "NEXUS win rate (%)": round(
            nexus_wins * 100 / total_games, 2
        ) if total_games else 0.0,
        "TITAN win rate (%)": round(
            titan_wins * 100 / total_games, 2
        ) if total_games else 0.0,
        "Average NEXUS nodes": round(
            average("nexus_nodes"), 2
        ),
        "Average TITAN nodes": round(
            average("titan_nodes"), 2
        ),
        "Average NEXUS pruned": round(
            average("nexus_pruned"), 2
        ),
        "Average TITAN pruned": round(
            average("titan_pruned"), 2
        ),
        "Average execution time (s)": round(
            average("execution_time_seconds"), 6
        ),
    }


def print_summary(summary):
    """Print the tournament summary."""

    print("\nTournament Summary")
    print("-" * 40)

    for key, value in summary.items():
        print(f"{key}: {value}")

    print("-" * 40)


def run_battle(seed=42, games=10):
    if games < 1:
        raise ValueError("Number of games must be at least 1.")

    nexus, titan = create_agents(
        depth=4,
        seed=seed,
    )

    rows = []

    for game_number in range(1, games + 1):
        # Alternate the starting agent.
        if game_number % 2 == 1:
            first_agent = nexus
        else:
            first_agent = titan

        result = run_single_game(
            nexus,
            titan,
            first_agent,
        )

        row = {
            "game": game_number,
            "first": first_agent.name,
            **result,
        }

        rows.append(row)

    fieldnames = [
        "game",
        "first",
        "winner",
        "moves",
        "nexus_nodes",
        "titan_nodes",
        "nexus_pruned",
        "titan_pruned",
        "nexus_time_seconds",
        "titan_time_seconds",
        "execution_time_seconds",
    ]

    save_csv(
        BATTLE_CSV,
        rows,
        fieldnames,
    )

    summary = calculate_summary(rows)

    return rows, summary


def run_depth_experiment(seed=43):
    depths = [1, 2, 3, 4]
    games_per_depth = 10
    depth_rows = []

    for depth in depths:
        depth_nexus = Agent(
            name="NEXUS",
            symbol="X",
            depth=depth,
            heuristic_name="H1",
            seed=seed + depth,
        )

        depth_titan = Agent(
            name="TITAN",
            symbol="O",
            depth=4,
            heuristic_name="H2",
            seed=seed + 100 + depth,
        )

        wins = 0
        draws = 0
        losses = 0
        total_nodes = 0
        total_pruned = 0
        total_time = 0.0

        for game_number in range(1, games_per_depth + 1):
            if game_number % 2 == 1:
                first_agent = depth_nexus
            else:
                first_agent = depth_titan

            result = run_single_game(
                depth_nexus,
                depth_titan,
                first_agent,
            )

            if result["winner"] == "NEXUS":
                wins += 1
            elif result["winner"] == "TITAN":
                losses += 1
            else:
                draws += 1

            total_nodes += result["nexus_nodes"]
            total_pruned += result["nexus_pruned"]
            total_time += result["nexus_time_seconds"]

        row = {
            "depth": depth,
            "games": games_per_depth,
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "average_nodes_per_game": round(
                total_nodes / games_per_depth, 2
            ),
            "average_pruned_per_game": round(
                total_pruned / games_per_depth, 2
            ),
            "average_execution_time_seconds": round(
                total_time / games_per_depth, 6
            ),
        }

        depth_rows.append(row)

    fieldnames = [
        "depth",
        "games",
        "wins",
        "draws",
        "losses",
        "average_nodes_per_game",
        "average_pruned_per_game",
        "average_execution_time_seconds",
    ]

    save_csv(
        DEPTH_CSV,
        depth_rows,
        fieldnames,
    )

    return depth_rows