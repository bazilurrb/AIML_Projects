# AI Campus Route Navigator
### AI/ML Laboratory — Assignment X_03 | B.Tech. 5th Semester
**University of Calcutta — CU Technology Campus**

---

## Overview

This project builds an **AI-based campus navigation system** for the CU Technology Campus.  
The satellite map is converted into a weighted graph and given to two AI agents that solve  
source-to-destination routing problems using different search strategies.

| Agent | Algorithm | Priority Function |
|-------|-----------|-------------------|
| **PATHFINDER** | Greedy Best-First Search | `f(n) = h(n)` |
| **ORBIT** | A\* Search | `f(n) = g(n) + h(n)` |

---

## Project Structure

```
campus-navigator/
├── main.py          ← User interface / program entry point
├── campus_map.py    ← Graph loader, heuristic, CSE-constraint neighbours
├── search.py        ← Greedy Best-First and A* algorithms
├── agents.py        ← PATHFINDER and ORBIT agent classes
├── experiment.py    ← Multi-route experiment runner + analysis
├── campus.json      ← Campus graph data (nodes, edges, weights)
├── results.csv      ← Auto-generated experiment results
└── README.md        ← This file
```

---

## How to Run

```bash
cd campus-navigator
python main.py
```

**Menu options:**
1. **Interactive Navigation** — enter any source and destination; both agents solve it
2. **Run All Experiments** — runs 10 pre-defined routes and saves `results.csv`
3. **List Campus Locations** — prints all accessible nodes
4. **Exit**

---

## Campus Graph (Part 1–2)

### Nodes (20 locations from the satellite map)

| # | Node ID | Label | CSE Zone |
|---|---------|-------|----------|
| 1 | `Entry Gate 1` | Entry Gate 1 (G1) | — |
| 2 | `Entry Gate 2` | Entry Gate 2 (G2) — Bottom Right | — |
| 3 | `Entry Gate 3` | Entry Gate 2 (G3) — *Permanently Closed* | — |
| 4 | `Entry Gate 4` | Entry Gate 2 (G4) — Top Right | — |
| 5 | `Parking Area` | Parking Area | — |
| 6 | `Tower 2 Front Entry` | Tower 2 Front Entry | — |
| 7 | `Tower 2 Rear Entry` | Tower 2 Rear Entry | — |
| 8 | `Lift Area` | Lift Area (CSE Gateway) | — |
| 9 | `CSE Laboratory` | CSE Laboratory | ★ |
| 10 | `CSE_Reflexon Room` | CSE\_Reflexon Room | ★ |
| 11 | `CSE_AKC Seminar Hall` | CSE\_AKC Seminar Hall | ★ |
| 12 | `Library` | Library | — |
| 13 | `Garden Area` | Garden Area — Technology Campus | — |
| 14 | `New Building 1` | New Building 1 | — |
| 15 | `New Building 2` | New Building 2 (Workshop Building) | — |
| 16 | `CRNN Centre` | CRNN Centre (Nano Technology) | — |
| 17 | `Auditorium Hall` | Auditorium Hall | — |
| 18 | `Reception` | Reception of Calcutta University | — |
| 19 | `Canteen` | Canteen, CU Technology Campus | — |
| 20 | `Playground` | Playground of Technology Campus | — |

> **Entry Gate 3** is permanently closed — it has no edges and cannot be visited.

### Edges & Weights

All weights are approximate walking distances in **metres**, estimated from the satellite map  
(scale ≈ 0.6 m/pixel). They are stored in `campus.json` and loaded at runtime.

Key connections (undirected):

```
Entry Gate 1       ──  90m ──  Canteen
Entry Gate 1       ── 150m ──  Reception
Canteen            ──  65m ──  Reception
Reception          ── 130m ──  Tower 2 Front Entry
Tower 2 Front Entry── 180m ──  Lift Area
Tower 2 Front Entry── 110m ──  Tower 2 Rear Entry
Tower 2 Rear Entry ──  30m ──  Lift Area
Tower 2 Rear Entry ──  70m ──  Library
Tower 2 Rear Entry ── 110m ──  Garden Area
Lift Area          ──  50m ──  CSE Laboratory     [CSE zone]
Lift Area          ──  70m ──  CSE_Reflexon Room  [CSE zone]
Lift Area          ──  60m ──  CSE_AKC Seminar Hall [CSE zone]
Library            ── 125m ──  New Building 1
Garden Area        ── 105m ──  New Building 1
Garden Area        ── 110m ──  New Building 2
New Building 1     ── 140m ──  Entry Gate 4
...  (full list in campus.json)
```

---

## Heuristic (Part 3)

Each node stores **x, y coordinates in metres** derived from the satellite image.  
The heuristic `h(n)` is the **straight-line (Euclidean) distance** to the destination:

```
h(n) = √((x_n − x_goal)² + (y_n − y_goal)²)
```

This heuristic is:
- **Admissible** — never overestimates (Euclidean ≤ actual walking distance)
- **Consistent** — satisfies the triangle inequality
- **Destination-dependent** — automatically adjusts for any source/destination pair

---

## Search Algorithms (Parts 4 & 6)

### PATHFINDER — Greedy Best-First Search

```
f(n) = h(n)
```

- Uses a min-heap with `h(n)` as priority
- Expands whichever node *looks* nearest to the goal
- Fast but **not guaranteed to find the shortest path**

### ORBIT — A* Search

```
f(n) = g(n) + h(n)
```

- Uses a min-heap with `g(n) + h(n)` as priority
- `g(n)` = total cost from source to node `n`
- With an admissible heuristic, **guarantees the optimal (shortest) path**

Both algorithms use state `(node, prev_node)` in the explored set to  
correctly distinguish the two Lift Area modes (entering vs exiting CSE zone).

---

## CSE Routing Constraint (Part 7)

The following are **CSE zone nodes**:
- `CSE Laboratory`
- `CSE_Reflexon Room`
- `CSE_AKC Seminar Hall`

**Entry rule:**
```
Tower 2 Front/Rear Entry  →  Lift Area  →  CSE nodes
```

**While inside CSE zone:** only CSE nodes or `Lift Area` are reachable.

**Exit rule:**
```
CSE nodes  →  Lift Area  →  Tower 2 Front/Rear Entry  →  rest of campus
```

The constraint is enforced in `CampusMap.get_valid_neighbors()` using a  
mode-detection function (`_cse_mode`) that reads the path history to  
determine whether the agent is in `entering`, `in_cse`, `exiting`, or `normal` mode.

---

## File Handling (Part 11)

- **`campus.json`** — campus graph (nodes, edges, weights, CSE config)  
  Algorithms read this file at startup via `CampusMap`.  
  Change the campus layout without touching any Python file.

- **`results.csv`** — auto-generated after running experiments.  
  Columns: `Route | Agent | Path | Cost (m) | Nodes Explored | Time (s)`

---

## OOP Structure (Part 10)

| Class | File | Responsibility |
|-------|------|----------------|
| `Node` | `campus_map.py` | Campus location data |
| `CampusMap` | `campus_map.py` | Graph, heuristic, CSE-aware neighbours |
| `SearchResult` | `search.py` | Result container (path, cost, stats) |
| `Agent` | `agents.py` | Abstract base agent |
| `Pathfinder` | `agents.py` | PATHFINDER agent (Greedy BFS) |
| `Orbit` | `agents.py` | ORBIT agent (A\*) |
| `Experiment` | `experiment.py` | Batch runner + CSV export + analysis |

---

## Experiment Results (Part 8)

Ten routes are tested by default:

| Route | Type |
|-------|------|
| Reception → Library | Ordinary |
| Canteen → New Building 2 | Ordinary |
| Library → Canteen | Ordinary |
| Entry Gate 4 → Auditorium Hall | Ordinary |
| New Building 2 → Entry Gate 1 | Ordinary |
| Playground → Entry Gate 2 | Ordinary |
| Entry Gate 1 → CSE Laboratory | CSE-related |
| Auditorium Hall → CSE\_AKC Seminar Hall | CSE-related |
| Playground → CSE\_Reflexon Room | CSE-related |
| CSE Laboratory → Canteen | CSE-related |

Results are saved to `results.csv`.

---

## Key Observations (Part 9)

1. **Greedy Best-First does NOT always find the shortest route** — it can be misled by the heuristic into a locally promising but globally longer path.
2. **A\* uses g(n) to penalise expensive partial paths**, preventing it from wasting distance on "close-looking" but costly nodes.
3. **Paths differ** when the greedy shortcut (low h) leads through costlier edges — A\* corrects this.
4. **The heuristic is the sole driver** for PATHFINDER; for ORBIT it is a tiebreaker that speeds up search without sacrificing optimality.
5. **The CSE constraint** reduces the branching factor dramatically — both agents are forced through the single Tower 2 → Lift Area gateway, often producing identical CSE-zone paths.

---

## Requirements

- Python 3.10+
- Standard library only (`heapq`, `json`, `csv`, `math`, `time`, `os`)

No external packages required.
