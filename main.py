import argparse

from experiment import (
    run_battle,
    run_depth_experiment,
    print_summary,
)

def display_battle_results(rows):
    print("\n" + "=" * 65)
    print("             AI AGENT BATTLE - TIC-TAC-TOE")
    print("=" * 65)

    print(
        f"{'Game':<7}"
        f"{'First':<10}"
        f"{'Winner':<10}"
        f"{'Moves':<8}"
        f"{'NEXUS Nodes':<14}"
        f"{'TITAN Nodes':<14}"
    )

    print("-" * 65)

    for row in rows:
        print(
            f"{row['game']:<7}"
            f"{row['first']:<10}"
            f"{row['winner']:<10}"
            f"{row['moves']:<8}"
            f"{row['nexus_nodes']:<14}"
            f"{row['titan_nodes']:<14}"
        )

    print("-" * 65)
    print("Full results saved to results/results.csv")


def display_depth_results(rows):
    print("\n" + "=" * 78)
    print("                    SEARCH-DEPTH EXPERIMENT")
    print("=" * 78)

    print(
        f"{'Depth':<8}"
        f"{'Wins':<8}"
        f"{'Draws':<8}"
        f"{'Losses':<8}"
        f"{'Avg Nodes':<15}"
        f"{'Avg Pruned':<15}"
        f"{'Avg Time (s)':<15}"
    )

    print("-" * 78)

    for row in rows:
        print(
            f"{row['depth']:<8}"
            f"{row['wins']:<8}"
            f"{row['draws']:<8}"
            f"{row['losses']:<8}"
            f"{row['average_nodes_per_game']:<15}"
            f"{row['average_pruned_per_game']:<15}"
            f"{row['average_execution_time_seconds']:<15}"
        )

    print("-" * 78)
    print("Full results saved to results/depth_experiment.csv")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Tic-Tac-Toe AI tournament using Minimax "
            "and Alpha-Beta pruning."
        )
    )

    parser.add_argument(
        "--experiment",
        choices=["all", "battle", "depth"],
        default="all",
        help="Select all experiments, battle, or depth.",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Seed used for tie-breaking.",
    )

    parser.add_argument(
        "--games",
        type=int,
        default=10,
        help="Number of tournament games.",
    )

    args = parser.parse_args()

    if args.games < 1:
        parser.error("--games must be at least 1.")

    if args.experiment in ("all", "battle"):
        rows, summary = run_battle(
            seed=args.seed,
            games=args.games,
        )

        display_battle_results(rows)
        print_summary(summary)

    if args.experiment in ("all", "depth"):
        depth_rows = run_depth_experiment(
            seed=args.seed + 1,
        )

        display_depth_results(depth_rows)


if __name__ == "__main__":
    main()