"""
main.py
=======
Entry point for the AI Campus Route Navigator.

Menu
----
  1. Interactive Navigation  — user types source & destination
  2. Run All Experiments     — fixed suite printed + saved to results.csv
  3. List Campus Locations   — numbered list of all accessible nodes
  4. Exit
"""

import io
import os
import sys

# Force UTF-8 output on Windows to avoid cp1252 issues
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from campus_map import CampusMap
from agents import Pathfinder, Orbit
from experiment import Experiment

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_HERE        = os.path.dirname(os.path.abspath(__file__))
CAMPUS_JSON  = os.path.join(_HERE, "campus.json")
RESULTS_CSV  = os.path.join(_HERE, "results.csv")

# ---------------------------------------------------------------------------
# Banner
# ---------------------------------------------------------------------------

BANNER = """
+--------------------------------------------------------------+
|          AI CAMPUS ROUTE NAVIGATOR                           |
|          University of Calcutta - Technology Campus          |
+--------------------------------------------------------------+
|   PATHFINDER  -> Greedy Best-First Search   f(n) = h(n)     |
|   ORBIT       -> A* Search                 f(n) = g+h(n)   |
+--------------------------------------------------------------+
"""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_campus() -> CampusMap:
    if not os.path.exists(CAMPUS_JSON):
        print(f"ERROR: campus.json not found at {CAMPUS_JSON}")
        sys.exit(1)
    return CampusMap(CAMPUS_JSON)


def list_locations(campus_map: CampusMap) -> None:
    print("\n  Campus Locations")
    print("  " + "-" * 54)
    accessible = sorted(
        [(nid, n) for nid, n in campus_map.nodes.items() if n.accessible],
        key=lambda x: x[0],
    )
    for i, (nid, node) in enumerate(accessible, 1):
        tag = "  ★ CSE Zone" if node.cse_zone else ""
        print(f"  {i:2}. {nid:<30}{tag}")
    print()


def _match_location(query: str, campus_map: CampusMap) -> str | None:
    """
    Case-insensitive match of *query* against node IDs and labels.
    Supports exact match, label match, and unambiguous partial match.
    Returns matched node ID or None.
    """
    q = query.strip().lower()

    # 1) Exact node-ID match
    for nid in campus_map.nodes:
        if nid.lower() == q:
            return nid

    # 2) Exact label match
    for nid, node in campus_map.nodes.items():
        if node.label.lower() == q:
            return nid

    # 3) Partial match
    matches = [
        nid for nid, node in campus_map.nodes.items()
        if q in nid.lower() or q in node.label.lower()
    ]

    if len(matches) == 1:
        print(f"  Matched → {campus_map.nodes[matches[0]].label}")
        return matches[0]

    if len(matches) > 1:
        print(f"  Multiple matches for '{query}':")
        for i, m in enumerate(matches, 1):
            print(f"    {i}. {m}")
        try:
            idx = int(input("  Choose number: ").strip()) - 1
            return matches[idx]
        except (ValueError, IndexError):
            print("  Invalid selection.")
            return None

    print(f"  Location '{query}' not found. Try listing locations (option 3).")
    return None


# ---------------------------------------------------------------------------
# Interactive navigation
# ---------------------------------------------------------------------------

def navigate_interactive(campus_map: CampusMap) -> None:
    pathfinder = Pathfinder(campus_map)
    orbit      = Orbit(campus_map)

    while True:
        print("\n" + "-" * 58)
        src_raw = input("  Starting location (or 'b' to go back): ").strip()
        if src_raw.lower() in ("b", "back", "q", "quit"):
            break

        source = _match_location(src_raw, campus_map)
        if source is None:
            continue
        if not campus_map.is_accessible(source):
            print(f"  ⚠  '{source}' is not accessible (permanently closed gate).")
            continue

        dst_raw = input("  Destination        (or 'b' to go back): ").strip()
        if dst_raw.lower() in ("b", "back", "q", "quit"):
            break

        destination = _match_location(dst_raw, campus_map)
        if destination is None:
            continue
        if not campus_map.is_accessible(destination):
            print(f"  ⚠  '{destination}' is not accessible.")
            continue

        if source == destination:
            print("  You are already at the destination!")
            continue

        print(f"\n  Navigating: {source}  →  {destination}")

        pf_result  = pathfinder.navigate(source, destination)
        orb_result = orbit.navigate(source, destination)

        pathfinder.print_result(pf_result)
        orbit.print_result(orb_result)

        again = input("  Search another route? (y / n): ").strip().lower()
        if again != "y":
            break


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------

def main() -> None:
    print(BANNER)
    campus_map = load_campus()

    accessible_count = len(campus_map.get_all_accessible_ids())
    print(f"  Loaded {accessible_count} accessible locations  |  "
          f"{len(campus_map.adjacency)} nodes in graph")
    print(f"  CSE Zone : {', '.join(campus_map.cse_zone_nodes)}")
    print(f"  Gateway  : {campus_map.cse_gateway}")

    while True:
        print("\n  ─── MENU ───────────────────────────────────────────")
        print("   1. Interactive Navigation")
        print("   2. Run All Experiments  (saves results.csv)")
        print("   3. List Campus Locations")
        print("   4. Exit")
        print("  ─────────────────────────────────────────────────────")

        choice = input("  Your choice: ").strip()

        if choice == "1":
            navigate_interactive(campus_map)

        elif choice == "2":
            exp = Experiment(campus_map, RESULTS_CSV)
            exp.run()

        elif choice == "3":
            list_locations(campus_map)

        elif choice == "4":
            print("\n  Goodbye!\n")
            break

        else:
            print("  Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
