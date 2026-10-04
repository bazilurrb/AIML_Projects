"""
experiment.py
=============
Runs multiple source→destination experiments, records per-run metrics,
saves results to results.csv, and prints a comparative analysis.
"""

import csv
import os
from typing import List, Optional, Tuple

from campus_map import CampusMap
from agents import Pathfinder, Orbit
from search import SearchResult


# ---------------------------------------------------------------------------
# Default experiment suite (Part 8)
# ---------------------------------------------------------------------------

DEFAULT_EXPERIMENTS: List[Tuple[str, str]] = [
    # Ordinary routes
    ("Reception",      "Library"),
    ("Canteen",        "New Building 2"),
    ("Library",        "Canteen"),
    ("Entry Gate 4",   "Auditorium Hall"),
    ("New Building 2", "Entry Gate 1"),
    ("Playground",     "Entry Gate 2"),
    # CSE-related routes
    ("Entry Gate 1",   "CSE Laboratory"),
    ("Auditorium Hall","CSE_AKC Seminar Hall"),
    ("Playground",     "CSE_Reflexon Room"),
    ("CSE Laboratory", "Canteen"),
]


# ---------------------------------------------------------------------------
# Experiment runner
# ---------------------------------------------------------------------------

class Experiment:
    """
    Runs PATHFINDER and ORBIT on a list of (source, destination) pairs,
    prints results to stdout, and saves a CSV summary.
    """

    CSV_FIELDS = [
        "Route", "Agent", "Path", "Cost (m)", "Nodes Explored", "Time (s)"
    ]

    def __init__(
        self,
        campus_map:   CampusMap,
        results_file: str = "results.csv",
    ) -> None:
        self.campus_map   = campus_map
        self.results_file = results_file
        self.pathfinder   = Pathfinder(campus_map)
        self.orbit        = Orbit(campus_map)
        self._rows: List[dict] = []

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def run(
        self,
        experiments: Optional[List[Tuple[str, str]]] = None,
    ) -> None:
        """Execute all experiments, print results, save CSV."""
        if experiments is None:
            experiments = DEFAULT_EXPERIMENTS

        self._rows.clear()
        print("\n" + "=" * 70)
        print("  CAMPUS ROUTE NAVIGATOR  -  EXPERIMENT SUITE")
        print("=" * 70)

        valid_pairs = 0
        for src, dst in experiments:
            ok = self._validate(src, dst)
            if not ok:
                continue
            valid_pairs += 1

            print(f"\n  ▶  {src}  →  {dst}")
            print("  " + "-" * 60)

            pf_res    = self.pathfinder.navigate(src, dst)
            orb_res   = self.orbit.navigate(src, dst)

            self.pathfinder.print_result(pf_res)
            self.orbit.print_result(orb_res)

            self._record(src, dst, "PATHFINDER", pf_res)
            self._record(src, dst, "ORBIT",      orb_res)

        self._save_csv()
        if valid_pairs > 0:
            self._print_analysis()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _validate(self, src: str, dst: str) -> bool:
        errors = []
        for loc in (src, dst):
            if loc not in self.campus_map.nodes:
                errors.append(f"'{loc}' is not a recognised campus location.")
            elif not self.campus_map.is_accessible(loc):
                errors.append(f"'{loc}' is permanently inaccessible (e.g., closed gate).")
        if errors:
            print(f"\n  ⚠  Skipping ({src} → {dst}):")
            for e in errors:
                print(f"     {e}")
            return False
        return True

    def _record(
        self, src: str, dst: str, agent: str, result: SearchResult
    ) -> None:
        self._rows.append({
            "Route":          f"{src} → {dst}",
            "Agent":          agent,
            "Path":           " → ".join(result.path) if result.found else "No path found",
            "Cost (m)":       f"{result.cost:.0f}" if result.found else "N/A",
            "Nodes Explored": result.nodes_explored,
            "Time (s)":       f"{result.time_elapsed:.6f}",
        })

    def _save_csv(self) -> None:
        if not self._rows:
            return
        with open(self.results_file, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=self.CSV_FIELDS)
            writer.writeheader()
            writer.writerows(self._rows)
        print(f"\n  ✔  Results saved → {os.path.abspath(self.results_file)}")

    def _print_analysis(self) -> None:
        """Comparative analysis answering Part 9 questions."""
        pf_rows  = [r for r in self._rows if r["Agent"] == "PATHFINDER"]
        orb_rows = [r for r in self._rows if r["Agent"] == "ORBIT"]

        total            = 0
        diff_paths       = 0
        orbit_lower_cost = 0
        orbit_equal_cost = 0
        pf_no_path       = 0
        orb_no_path      = 0

        for pf, orb in zip(pf_rows, orb_rows):
            if pf["Path"] == "No path found" or orb["Path"] == "No path found":
                if pf["Path"]  == "No path found": pf_no_path  += 1
                if orb["Path"] == "No path found": orb_no_path += 1
                continue

            total += 1
            pf_cost  = float(pf["Cost (m)"])
            orb_cost = float(orb["Cost (m)"])

            if pf["Path"] != orb["Path"]:
                diff_paths += 1
            if orb_cost < pf_cost:
                orbit_lower_cost += 1
            elif orb_cost == pf_cost:
                orbit_equal_cost += 1

        border = "=" * 70
        print(f"\n{border}")
        print("  COMPARATIVE ANALYSIS  -  PATHFINDER vs ORBIT")
        print(border)
        print(f"  Routes compared (both found paths) : {total}")
        print(f"  Routes with DIFFERENT paths        : {diff_paths}")
        print(f"  Routes where ORBIT found lower cost: {orbit_lower_cost}")
        print(f"  Routes where costs were equal      : {orbit_equal_cost}")
        if pf_no_path or orb_no_path:
            print(f"  Routes PATHFINDER had no path      : {pf_no_path}")
            print(f"  Routes ORBIT had no path           : {orb_no_path}")

        print(f"""
  Answers to Part 9 Observation Questions
  ----------------------------------------
  Q1. Does Greedy Best-First always find the shortest route?
      No. PATHFINDER follows the heuristic greedily and can be misled
      into longer routes when a node "looks" close but requires a costly
      detour to reach.

  Q2. How does A* use distance already travelled?
      ORBIT adds g(n) (accumulated cost) to h(n) at every expansion.
      This prevents it from chasing a "close-looking" node that was
      reached via an expensive path.

  Q3. When do the two agents choose different paths?
      They diverge when the heuristic is misleading - i.e., when a
      greedy step toward the goal actually leads to a longer overall
      route. ORBIT's g(n) term corrects this.

  Q4. How does the heuristic affect their behaviour?
      Both agents use the same Euclidean heuristic.  For PATHFINDER it
      IS the decision criterion; for ORBIT it supplements real cost.
      A tighter (more accurate) heuristic makes ORBIT expand fewer nodes.

  Q5. What happens when the CSE constraint restricts routes?
      Both agents are forced through Tower 2 → Lift Area as the sole
      CSE gateway. This reduces the branching factor inside the CSE zone
      and often produces identical paths, since there is only one valid
      entry/exit sequence.
{border}""")
