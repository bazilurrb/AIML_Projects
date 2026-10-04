"""
campus_map.py
=============
Loads the CU Technology Campus graph from campus.json and provides:
  - Node / edge access
  - Admissible Euclidean heuristic
  - CSE-zone-aware neighbour queries
"""

import json
import math
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

class Node:
    """A single campus location (graph vertex)."""

    def __init__(
        self,
        node_id: str,
        label: str,
        x: float,
        y: float,
        accessible: bool = True,
        cse_zone: bool = False,
    ) -> None:
        self.id         = node_id
        self.label      = label
        self.x          = x
        self.y          = y
        self.accessible = accessible
        self.cse_zone   = cse_zone

    def __repr__(self) -> str:
        return f"Node({self.id!r})"


# ---------------------------------------------------------------------------
# Main graph class
# ---------------------------------------------------------------------------

class CampusMap:
    """
    Weighted undirected graph representing the CU Technology Campus.

    The graph is loaded from *campus.json* so that routing algorithms never
    need to be changed when the campus layout is updated.

    CSE Routing Constraint (Part 7)
    --------------------------------
    Entry  : … → Tower 2 Front/Rear Entry → Lift Area → CSE node
    In zone: only CSE nodes or Lift Area are reachable
    Exit   : CSE node → Lift Area → Tower 2 Front/Rear Entry → campus
    """

    def __init__(self, json_path: str) -> None:
        self.nodes:         Dict[str, Node]              = {}
        self.adjacency:     Dict[str, Dict[str, float]]  = {}
        self.cse_zone_nodes:  List[str] = []
        self.cse_entry_nodes: List[str] = []
        self.cse_gateway:     str       = ""

        self._load(json_path)

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def _load(self, json_path: str) -> None:
        """Parse campus.json and populate graph structures."""
        with open(json_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)

        # Nodes
        for node_id, info in data["nodes"].items():
            self.nodes[node_id] = Node(
                node_id    = node_id,
                label      = info.get("label", node_id),
                x          = float(info["coordinates"]["x"]),
                y          = float(info["coordinates"]["y"]),
                accessible = info.get("accessible", True),
                cse_zone   = info.get("cse_zone", False),
            )
            self.adjacency[node_id] = {}

        # Edges (undirected)
        for edge in data["edges"]:
            src = edge["from"]
            dst = edge["to"]
            w   = float(edge["weight"])
            if src in self.nodes and dst in self.nodes:
                self.adjacency[src][dst] = w
                self.adjacency[dst][src] = w

        # CSE constraint metadata
        self.cse_zone_nodes  = data.get("cse_zone_nodes", [])
        self.cse_entry_nodes = data.get("cse_entry_nodes", [])
        self.cse_gateway     = data.get("cse_gateway", "Lift Area")

    # ------------------------------------------------------------------
    # Basic queries
    # ------------------------------------------------------------------

    def get_node(self, node_id: str) -> Optional[Node]:
        return self.nodes.get(node_id)

    def is_accessible(self, node_id: str) -> bool:
        node = self.nodes.get(node_id)
        return node.accessible if node else False

    def get_all_accessible_ids(self) -> List[str]:
        return [nid for nid, n in self.nodes.items() if n.accessible]

    def path_cost(self, path: List[str]) -> float:
        """Sum of edge weights along a path list."""
        total = 0.0
        for i in range(len(path) - 1):
            total += self.adjacency[path[i]][path[i + 1]]
        return total

    # ------------------------------------------------------------------
    # Heuristic
    # ------------------------------------------------------------------

    def heuristic(self, node_id: str, goal_id: str) -> float:
        """
        Straight-line (Euclidean) distance between *node_id* and *goal_id*.

        Using node coordinates in metres this is always ≤ the true walking
        distance, making the heuristic *admissible* for A*.
        """
        a = self.nodes[node_id]
        b = self.nodes[goal_id]
        return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

    # ------------------------------------------------------------------
    # CSE-aware neighbour query
    # ------------------------------------------------------------------

    def get_valid_neighbors(
        self, node_id: str, path: List[str]
    ) -> Dict[str, float]:
        """
        Return {neighbour_id: edge_weight} for *node_id* after enforcing
        the CSE-zone routing constraint.

        Parameters
        ----------
        node_id : str
            Current node (last element of *path*).
        path : list[str]
            Full path from source up to and including *node_id*.

        Mode logic
        ----------
        'in_cse'   – inside CSE zone: only CSE peers + Lift Area
        'entering' – at Lift Area via Tower 2: go to CSE zone or back
        'exiting'  – at Lift Area via CSE: must exit through Tower 2
        'normal'   – everywhere else: CSE zone is inaccessible
        """
        raw  = self.adjacency.get(node_id, {})
        mode = self._cse_mode(path, node_id)

        if mode == "in_cse":
            return {
                n: w for n, w in raw.items()
                if n in self.cse_zone_nodes or n == self.cse_gateway
            }

        if mode == "entering":
            return {
                n: w for n, w in raw.items()
                if n in self.cse_zone_nodes or n in self.cse_entry_nodes
            }

        if mode == "exiting":
            return {
                n: w for n, w in raw.items()
                if n in self.cse_entry_nodes
            }

        # Normal mode — block direct access to CSE zone
        return {
            n: w for n, w in raw.items()
            if n not in self.cse_zone_nodes
        }

    def _cse_mode(self, path: List[str], current: str) -> str:
        """
        Derive the CSE routing mode from path history.

        Parameters
        ----------
        path    : full path from source including *current*
        current : the node we are currently evaluating neighbours for

        Returns
        -------
        'in_cse' | 'entering' | 'exiting' | 'normal'
        """
        # Currently inside a CSE zone node
        if current in self.cse_zone_nodes:
            return "in_cse"

        # Currently at the CSE gateway (Lift Area)
        if current == self.cse_gateway and len(path) >= 2:
            prev = path[-2]
            if prev in self.cse_zone_nodes:
                return "exiting"   # arrived from CSE — must leave via Tower 2
            if prev in self.cse_entry_nodes:
                return "entering"  # arrived from Tower 2 — may enter CSE

        return "normal"
