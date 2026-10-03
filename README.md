# AI Agent Battle — Tic-Tac-Toe

## 1. Project Overview

AI Agent Battle is a Python-based Artificial Intelligence project that implements two AI agents, **NEXUS** and **TITAN**, to play Tic-Tac-Toe against each other.

The project uses the Minimax algorithm, Alpha-Beta pruning, heuristic evaluation functions, and configurable search depth to make decisions. It also records game statistics and performance measurements for analysis.

The main purpose of this project is to understand how AI agents make decisions in adversarial games and how search depth and pruning affect computational performance.

## 2. Objectives

* Implement a Tic-Tac-Toe game engine.
* Implement the Minimax algorithm.
* Implement Alpha-Beta pruning.
* Create two AI agents with different heuristic evaluation functions.
* Allow configurable search depth.
* Run 10 AI-versus-AI games with alternating starting players.
* Conduct experiments at search depths 1, 2, 3, and 4.
* Record game outcomes, evaluated nodes, pruned nodes, and execution time.
* Save experimental results in CSV files.
* Analyze the performance of the two AI agents.

## 3. Technologies Used

* Python 3.14.0
* Object-Oriented Programming
* Minimax algorithm
* Alpha-Beta pruning
* Heuristic evaluation
* CSV file handling

The program uses Python's standard library and does not require external packages.

## 4. Project Structure

```text
AI-Agent-Battle/
│
├── game.py
├── heuristic.py
├── minimax.py
├── agents.py
├── experiment.py
├── main.py
├── README.md
│
└── results/
    ├── results.csv
    └── depth_experiment.csv
```

### File Descriptions

| File                           | Purpose                                                                                        |
| ------------------------------ | ---------------------------------------------------------------------------------------------- |
| `game.py`                      | Implements the Tic-Tac-Toe game board, valid moves, move execution, and terminal-state checks. |
| `heuristic.py`                 | Defines the H1 and H2 heuristic evaluation functions.                                          |
| `minimax.py`                   | Implements Minimax, Alpha-Beta pruning, and best-move selection.                               |
| `agents.py`                    | Defines the AI agent and creates the NEXUS and TITAN agents.                                   |
| `experiment.py`                | Runs the AI battle and search-depth experiments, collects statistics, and saves CSV results.   |
| `main.py`                      | Provides the main program entry point and command-line experiment selection.                   |
| `results/results.csv`          | Stores the results of the AI-versus-AI battle.                                                 |
| `results/depth_experiment.csv` | Stores the search-depth experiment results.                                                    |

## 5. Game Engine

The game is played on a 3 × 3 board using the symbols `X` and `O`.

The game engine supports:

* Initializing the board.
* Finding valid moves.
* Executing moves.
* Checking whether a player has won.
* Detecting a draw.
* Determining whether the game has ended.

A player wins by completing a row, column, or diagonal. If the board is full and neither player has won, the game ends in a draw.

## 6. AI Agents

The project contains two AI agents.

### 6.1 NEXUS — H1

NEXUS uses the heuristic evaluation function `evaluate_h1`.

This function evaluates board positions and provides scores used by the search algorithm to select moves.

### 6.2 TITAN — H2

TITAN uses the heuristic evaluation function `evaluate_h2`.

This function evaluates board positions using a different scoring approach from H1. The difference between the two heuristics allows the agents to evaluate possible moves differently.

Both agents use the search and move-selection implementation provided in `minimax.py`.

The exact scoring rules are defined in `heuristic.py`.

## 7. Algorithms

### 7.1 Minimax

Minimax is an adversarial search algorithm used in two-player games.

It considers possible moves for both players and selects a move based on the best achievable outcome, assuming that the opponent also makes decisions to improve their own outcome.

The algorithm explores the game tree up to the configured search depth and uses the evaluation function to assess positions when the search reaches its stopping condition.

### 7.2 Alpha-Beta Pruning

Alpha-Beta pruning reduces the number of branches explored by Minimax.

* **Alpha:** The best score currently available to the maximizing player.
* **Beta:** The best score currently available to the minimizing player.

Branches that cannot improve the final decision are skipped. This reduces unnecessary search while preserving the Minimax result when implemented correctly with the same search depth and evaluation function.

### 7.3 Heuristic Evaluation

The heuristic functions estimate the value of a board position.

They are used when the search reaches its depth limit before reaching a terminal game state. NEXUS uses H1, while TITAN uses H2.

### 7.4 Search Depth

Search depth determines how many levels of future moves are explored.

A greater depth allows the agent to examine more future possibilities but can also increase computation time and the number of evaluated nodes.

The program allows different depths to be tested experimentally.

## 8. Experiments

### 8.1 AI Battle Experiment

The battle experiment runs 10 games between NEXUS and TITAN.

The starting player alternates between games:

* Odd-numbered games: NEXUS starts.
* Even-numbered games: TITAN starts.

The program records the following measurements:

* Game number.
* Starting player.
* Winner or draw.
* Number of moves.
* Nodes evaluated by NEXUS.
* Nodes evaluated by TITAN.
* Nodes pruned by NEXUS.
* Nodes pruned by TITAN.
* Execution time for each agent.
* Total execution time.

These measurements are saved in `results/results.csv`.

### 8.2 Search-Depth Experiment

The depth experiment evaluates performance at search depths:

* Depth 1
* Depth 2
* Depth 3
* Depth 4

The program records the experiment's configured statistics, including game outcomes and average computational measurements.

The results are saved in `results/depth_experiment.csv`.

These measurements can be used to investigate how changing search depth affects performance.

## 9. How to Run the Program

### Requirements

* Python 3.14.0 installed.
* All six Python source files in the project directory.

### Step 1: Open the Project

Open the project folder in VS Code or another Python IDE.

### Step 2: Check Python Installation

Run:

```bash
python --version
```

On Windows, you can alternatively use:

```bash
py --version
```

### Step 3: Run All Experiments

```bash
python main.py
```

### Step 4: Run Only the AI Battle

```bash
python main.py --experiment battle
```

### Step 5: Run Only the Depth Experiment

```bash
python main.py --experiment depth
```

On Windows, replace `python` with `py` if required.

The program generates or updates the corresponding CSV results when the experiments run successfully.

## 10. Output and Results

### `results/results.csv`

This file contains the individual AI battle records and performance measurements.

It can be opened in Excel, LibreOffice Calc, or a text editor.

### `results/depth_experiment.csv`

This file contains the performance measurements for the search-depth experiment.

It can be used to compare the recorded statistics at depths 1, 2, 3, and 4.

The CSV files generated by the program should be used as the source of truth for all numerical results and conclusions.

## 11. Analysis of Experimental Results

The following questions can be investigated using the generated CSV files.

### Did Search Depth Affect Decisions?

Compare the outcomes and agent behavior at different depths. Deeper searches can reveal future consequences that are not visible at smaller depths.

### Did Execution Time Increase with Search Depth?

Compare the recorded execution times at depths 1, 2, 3, and 4.

### Did the Number of Evaluated Nodes Increase?

Examine the evaluated-node statistics to determine how the explored search space changed with depth.

### Did Alpha-Beta Pruning Reduce Search?

Compare the evaluated and pruned node counts to examine the effect of pruning.

### Did the Agents Make Different Decisions?

Compare the moves or outcomes produced by NEXUS and TITAN. Their different heuristic evaluation functions may lead them to choose different moves.

### Was There a First-Player Advantage?

Compare the results of games started by NEXUS with those started by TITAN.

### Which Agent Won More Games?

Count each agent's wins and the number of draws in `results/results.csv`. Report the observed results without assuming which agent should perform better.

### Did More Computation Lead to Better Results?

Compare each agent's game outcomes with its evaluated-node counts and execution time. The results can show the relationship observed in this experiment, but they do not establish a universal relationship between computation and playing strength.

All findings should be based on the actual generated CSV files.

## 12. Limitations

* The project evaluates agents in Tic-Tac-Toe only.
* Performance depends on the implemented heuristic functions and search depth.
* Execution time can vary with hardware and system load.
* The 10-game battle provides a limited experimental sample.
* The results cannot automatically be generalized to more complex games.

## 13. Conclusion

This project demonstrates the use of Minimax and Alpha-Beta pruning in an AI-based Tic-Tac-Toe game.

Two agents, NEXUS and TITAN, use different heuristic evaluation functions to select their moves. The AI battle and search-depth experiments provide measurements of game outcomes, node exploration, pruning, and execution time.

The generated CSV files support a comparison of the agents and an investigation of the computational effects of search depth and Alpha-Beta pruning.


