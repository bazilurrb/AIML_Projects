"""
search.py
=========
Pure search algorithm implementations (no agent logic).

PATHFINDER  →  Greedy Best-First Search   f(n) = h(n)
ORBIT       →  A* Search                  f(n) = g(n) + h(n)

Both algorithms:
  - Use a min-heap priority queue (frontier)
  - Track explored states as (node, previous_node) to correctly handle the
    Lift Area's two distinct routing modes (entering / exiting CSE zone)
  - Delegate neighbour validity to CampusMap.get_valid_neighbors()
  - Return a SearchResult object with path, cost, nodes explored, and time
"""

import heapq
import time
from typing import List, Optional, Tuple

from campus_map import CampusMap


# ---------------------------------------------------------------------------
# Result container
# ---------------------------------------------------------------------------

class SearchResult:
    """Holds all output metrics for one search run."""

    def __init__(
        self,
        algorithm:      str,
        path:           List[str],
        cost:           float,
        nodes_explored: int,
        time_elapsed:   float,
    ) -> None:
        self.algorithm      = algorithm
        self.path           = path          # ordered list of node IDs
        self.cost           = cost          # total walking distance (m)
        self.nodes_explored = nodes_explored
        self.time_elapsed   = time_elapsed  # seconds

    @property
    def found(self) -> bool:
        return bool(self.path)

    def __repr__(self) -> str:
        return (
            f"SearchResult(algo={self.algorithm!r}, "
            f"cost={self.cost}, explored={self.nodes_explored})"
        )


# ---------------------------------------------------------------------------
# Greedy Best-First Search  —  PATHFINDER
# ---------------------------------------------------------------------------

def greedy_best_first_search(
    campus_map: CampusMap, source: str, destination: str
) -> SearchResult:
    """
    Greedy Best-First Search.

    Expansion priority  :  f(n) = h(n)
    Strategy            :  Always expand the node that *looks* closest to
                           the destination, ignoring cost already paid.

    Parameters
    ----------
    campus_map  : loaded CampusMap instance
    source      : start node ID
    destination : goal  node ID

    Returns
    -------
    SearchResult
    """
    algo  = "Greedy Best-First Search"
    start = time.perf_counter()

    if source == destination:
        return SearchResult(algo, [source], 0.0, 1, time.perf_counter() - start)

    # Heap entry: (h_value, tie_counter, current_node, path, g_cost)
    h0      = campus_map.heuristic(source, destination)
    counter = 0
    frontier: List[Tuple] = [(h0, counter, source, [source], 0.0)]

    # Explored set uses (node, prev_node) to distinguish Lift Area modes
    explored = set()
    nodes_explored = 0

    while frontier:
        h, _, node, path, g_cost = heapq.heappop(frontier)

        prev_node = path[-2] if len(path) >= 2 else None
        state     = (node, prev_node)
        if state in explored:
            continue
        explored.add(state)
        nodes_explored += 1

        if node == destination:
            elapsed = time.perf_counter() - start
            return SearchResult(algo, path, g_cost, nodes_explored, elapsed)

        for neighbour, weight in campus_map.get_valid_neighbors(node, path).items():
            n_prev  = path[-1]          # = node
            n_state = (neighbour, n_prev)
            if n_state not in explored:
                new_path = path + [neighbour]
                new_g    = g_cost + weight
                h_n      = campus_map.heuristic(neighbour, destination)
                counter += 1
                heapq.heappush(frontier, (h_n, counter, neighbour, new_path, new_g))

    elapsed = time.perf_counter() - start
    return SearchResult(algo, [], float("inf"), nodes_explored, elapsed)


# ---------------------------------------------------------------------------
# A* Search  —  ORBIT
# ---------------------------------------------------------------------------

def a_star_search(
    campus_map: CampusMap, source: str, destination: str
) -> SearchResult:
    """
    A* Search.

    Expansion priority  :  f(n) = g(n) + h(n)
    Strategy            :  Balance actual cost already paid (g) with the
                           estimated remaining cost (h).  Guarantees the
                           optimal path when the heuristic is admissible.

    Parameters
    ----------
    campus_map  : loaded CampusMap instance
    source      : start node ID
    destination : goal  node ID

    Returns
    -------
    SearchResult
    """
    algo  = "A* Search"
    start = time.perf_counter()

    if source == destination:
        return SearchResult(algo, [source], 0.0, 1, time.perf_counter() - start)

    # Heap entry: (f_value, tie_counter, current_node, path, g_cost)
    h0      = campus_map.heuristic(source, destination)
    counter = 0
    frontier: List[Tuple] = [(h0, counter, source, [source], 0.0)]

    explored = set()
    nodes_explored = 0

    while frontier:
        f, _, node, path, g_cost = heapq.heappop(frontier)

        prev_node = path[-2] if len(path) >= 2 else None
        state     = (node, prev_node)
        if state in explored:
            continue
        explored.add(state)
        nodes_explored += 1

        if node == destination:
            elapsed = time.perf_counter() - start
            return SearchResult(algo, path, g_cost, nodes_explored, elapsed)

        for neighbour, weight in campus_map.get_valid_neighbors(node, path).items():
            n_prev  = path[-1]
            n_state = (neighbour, n_prev)
            if n_state not in explored:
                new_path = path + [neighbour]
                new_g    = g_cost + weight
                h_n      = campus_map.heuristic(neighbour, destination)
                f_n      = new_g + h_n          # A* key difference: g + h
                counter += 1
                heapq.heappush(frontier, (f_n, counter, neighbour, new_path, new_g))

    elapsed = time.perf_counter() - start
    return SearchResult(algo, [], float("inf"), nodes_explored, elapsed)
