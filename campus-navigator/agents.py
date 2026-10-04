"""
agents.py
=========
Defines the two AI navigation agents:

  PATHFINDER  ->  Greedy Best-First Search  (f = h)
  ORBIT       ->  A* Search                 (f = g + h)

Each agent wraps a search algorithm and adds display / reporting logic.
"""

from campus_map import CampusMap
from search import SearchResult, greedy_best_first_search, a_star_search


# ---------------------------------------------------------------------------
# Base agent
# ---------------------------------------------------------------------------

class Agent:
    """Abstract base class for a campus navigation agent."""

    def __init__(self, name: str, campus_map: CampusMap) -> None:
        self.name        = name
        self.campus_map  = campus_map

    def navigate(self, source: str, destination: str) -> SearchResult:
        """Run the agent's search and return a SearchResult."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    def format_result(self, result: SearchResult) -> str:
        """Return a formatted multi-line string summarising the result."""
        border = "=" * 56
        if not result.found:
            return (
                f"\n{border}\n"
                f"  {self.name}\n"
                f"{border}\n"
                f"  [!]  No path found between the given locations.\n"
                f"{border}\n"
            )

        route = " -> ".join(result.path)
        # Wrap long routes neatly
        if len(route) > 52:
            lines  = []
            tokens = result.path
            line   = "  " + tokens[0]
            for tok in tokens[1:]:
                addition = " -> " + tok
                if len(line) + len(addition) > 60:
                    lines.append(line + " ->")
                    line = "    " + tok
                else:
                    line += addition
            lines.append(line)
            route = "\n".join(lines)
        else:
            route = "  " + route

        return (
            f"\n{border}\n"
            f"  {self.name}\n"
            f"{border}\n"
            f"  Route:\n{route}\n\n"
            f"  Cost          : {result.cost:.0f} m\n"
            f"  Nodes Explored: {result.nodes_explored}\n"
            f"  Time          : {result.time_elapsed:.6f} s\n"
            f"{border}\n"
        )

    def print_result(self, result: SearchResult) -> None:
        print(self.format_result(result))


# ---------------------------------------------------------------------------
# PATHFINDER — Greedy Best-First Search
# ---------------------------------------------------------------------------

class Pathfinder(Agent):
    """
    PATHFINDER agent.

    Uses Greedy Best-First Search: at every step it greedily expands the
    node that *appears* closest to the destination based solely on the
    heuristic h(n).  It is fast but does not guarantee an optimal route.

    f(n) = h(n)
    """

    def __init__(self, campus_map: CampusMap) -> None:
        super().__init__("PATHFINDER  [Greedy Best-First Search]", campus_map)

    def navigate(self, source: str, destination: str) -> SearchResult:
        return greedy_best_first_search(self.campus_map, source, destination)


# ---------------------------------------------------------------------------
# ORBIT — A* Search
# ---------------------------------------------------------------------------

class Orbit(Agent):
    """
    ORBIT agent.

    Uses A* Search: balances the actual distance already travelled g(n)
    with the estimated remaining distance h(n).  With an admissible
    heuristic, A* is guaranteed to find the shortest path.

    f(n) = g(n) + h(n)
    """

    def __init__(self, campus_map: CampusMap) -> None:
        super().__init__("ORBIT       [A* Search]              ", campus_map)

    def navigate(self, source: str, destination: str) -> SearchResult:
        return a_star_search(self.campus_map, source, destination)
