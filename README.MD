# Sliding Puzzle Solver

This project is a Python implementation of various search algorithms to solve the **Sliding Puzzle Problem**, including BFS, IDDFS, GBFS, and A*.

The project was created for the **Introduction to Artificial Intelligence (AI)** course at the **Open University**.

**Author**: Omer Lebel  

### struct:
```
├── Tile.py        # Main script; defines the Sliding Puzzle problem and program entry point  
├── searchAI.py    # Implements search algorithms (BFS, IDDFS, GBFS, A*)  
├── heuristic.py   # Heuristic functions (Manhattan Distance and Linear Conflict)
```
 
---
## 🖇️ Tile.py - problem formalization
The problem is formalized in the `SlidingPuzzle` class, which defines the puzzle's structure and behavior in a general way:

- **state:** presenting as a tuple. for n×n puzzle, the size of the state space is n!
- **initial state:** provided by the user through the command line interface. Can be any valid configuration of the tiles.
- **goal state:** (0, 1, 2,...,n×n - 1) 
- **action:** From each state, the blank tile (0) can move in four directions: left, right, up, and down.
- **tradition model:** Let i be the index of the blank tile. The resulting state after an action is:
  * left: swap(state[i], state[i-1])
  * right: swap(state[i], state[i+1])
  * up: swap(state[i], state[i-size])
  * down: swap(state[i], state[i+size])

Here’s an illustration of the blank tile’s movement on 8-puzzle:

|     $$0$$     |   i-size $$1$$   |     $$2$$     |
|:-------------:|:----------------:|:-------------:|
| **i-1** $$3$$ | **[ i ]** $$4$$  | **i+1** $$5$$ |
|     $$6$$     | **i+size** $$7$$ |     $$8$$     |


---
## 🌳 searchAI.py - Searching in the state space 
To solve the puzzle, each algorithm constructs a search tree.
The `Node` class defines the structure of a tree node, containing:
- **state**: The current configuration of the board.
- **parent**: The parent node from which this node was expanded.
- **action**: The move taken to reach this node.
- **path cost**: The cost of the path from the root to this node.
---


## 🔎 Heuristic
The heuristic used is a soft version of `Linear Conflict`, which is an enhancement of the Manhattan Distance.
Here’s the process of how I arrived at this idea:

### Manhattan Distance:
The Manhattan heuristic computes the sum of the distances each tile is from its goal position:
> $$
\ 
ManhattanDistance(node) = \sum_{i=1}^{n} D_t = |r_i - r'_i| + |c_i - c'_i|
\
$$
> where $(ri, ci)$ and $(r'_i, c'_i)$ are the current and goal position of tile i, respectively.

However, Manhattan Distance is often too optimistic. For instance, consider this board:

|       | 2     | 1     |
|-------|-------|-------|
| **6** | **4** | **5** |
| **3** | **7** | **8** |

In this case, tiles 2, 1, 3, and 6 are misplaced, but each of them is a neighbor of its target position. 
Therefore, the Manhattan distance is $1 + 1 + 1 = 4$, but the actual distance is much larger—22!

If we look on the flat board $(2, 1, 6, 4, 5, 3, 7, 8)$
We can see in this board that there are 4 inversion in this board. So, to improve the heuristic, we can penalize
the Manhattan Distance by adding 1 for each inversion. Formally: 
### Inversion heuristic:
First define an inversion properly:
> $$
\
Inversion((p_1, p_2,...,p_n)) = \sum_{1 \leq i < j \leq n} \mathbf{1}_{\{ p_i > p_j \}}
\
$$

Now, the improved heuristics will be the Manhattan Distance and the inversion count.
Unfortunately this is not a consistent heuristic. For example, consider this board:

| 3     | 1     | 2     |
|-------|-------|-------|
| **6** | **4** | **5** |
|       | **7** | **8** |

The board is represented as $(3, 1, 2, 6, 4, 5, 7, 8)$ which has 3 inversion: $(3,1), (3,2), (6,4), (6,5)$.
So, the inversion heuristic gives a value of 4, while the real distance is 2, achieved by moving tiles 3 and 6 down. 
This results in an overestimate even before adding the Manhattan distance.

Let's return to the previous board where the Manhattan Distance was incorrect:

|       | 2     | 1     |
|-------|-------|-------|
| **6** | **4** | **5** |
| **3** | **7** | **8** |

This is converted to the flat board: $(2, 1, 6, 4, 5, 3, 7, 8)$

The inversions $(6,4)$ or $(6,5)$ aren’t problematic, as they can be easily fixed.
However, the inversion (6,3) creates a significant issue. Both 3 and 6 are in their target column, 
and to resolve the inversion, each will have to move, increasing the distance by at least 2.
This leads us to the next definition:

### Linear conflict:
> **Row linear conflict**: two tiles $t_i$ and $t_j$ are in a conflict if
> - both are in their target row
> - $t_j$ is to the right of $t_i$, and the goal position of $t_j$ is to the left of the goal position of $t_i$.
> 
> **Col linear conflict**: similar

Combining it together with the Manhattan distance we get the formula:
> $$ 
 \ 
> LinearConflict(node) = ManhattanDistance(node) + 2×rowConflict(node) + 2×colConflict(node)
> \
 $$

Almost the same idae wad suggested by Richard E.Korf and Larry A.Taylor in 1966. 
Their formula is much more accurate: for each inversion it counts number of tiles that need to be removed from row/col in order to resolve the conflict.
For further explanation you may want to read [this article](https://cse.sc.edu/~mgv/csce580sp15/gradPres/HanssonMayerYung1992.pdf). 
You can also see the [original article](https://cdn.aaai.org/AAAI/1996/AAAI96-178.pdf).
---

## ▶️ Usage and run example

To run the sliding puzzle solver, execute the main script using Python.
The program expects the initial state of the puzzle board to be entered as a space-separated list of integers,
where 0 represents the blank tile. For example:
```bash
python tile.py 1 4 0 5 8 2 3 6 7
```
will lead to the output:

```
BFS
 nodes expanded: 357
 path: 2 -> 8 -> 5 -> 3 -> 6 -> 7 -> 8 -> 5 -> 4 -> 1 

IDDFS
 nodes expanded: 868
 path: 2 -> 8 -> 5 -> 3 -> 6 -> 7 -> 8 -> 5 -> 4 -> 1 

GBFS
 nodes expanded: 15
 path: 2 -> 8 -> 5 -> 3 -> 6 -> 7 -> 8 -> 5 -> 4 -> 1 

A*
 nodes expanded: 15
 path: 2 -> 8 -> 5 -> 3 -> 6 -> 7 -> 8 -> 5 -> 4 -> 1 

```
The path represents the sequence of tile moves from the initial state to the goal state

**Note:**
* No validation is done for input, so be sure to enter a valid configuration: numbers separated by space.
* The program supports solving puzzles of any size, as long as the number of tiles forms a square (e.g., 3x3, 4x4, etc.).
---

## 🧪 Result
- [x] BFS - Always finds the optimal solution.
- [ ] IDDFS - Usually finds the optimal solution but may terminate prematurely if a depth limit is reached. <br>
Depth limit is set to 30 due to poor and limited resources of my computer.
- [ ] GBFS - Finds a solution but does not guarantee optimality.
- [x] A* - Always finds the optimal solution.

for the input 8 4 5 3 2 1 0 6 7, we will get the output:
```
BFS
 nodes expanded: 31922
 path: 6 -> 2 -> 4 -> 8 -> 3 -> 4 -> 8 -> 5 -> 1 -> 8 -> 2 -> 7 -> 8 -> 2 -> 5 -> 1 -> 2 -> 5 -> 4 -> 3 

IDDFS
 nodes expanded: 232297
 path: 6 -> 2 -> 4 -> 8 -> 3 -> 4 -> 8 -> 5 -> 1 -> 8 -> 2 -> 7 -> 8 -> 2 -> 5 -> 1 -> 2 -> 5 -> 4 -> 3 


GBFS
 nodes expanded: 140
 path: 6 -> 7 -> 1 -> 5 -> 4 -> 8 -> 3 -> 2 -> 8 -> 4 -> 5 -> 8 -> 2 -> 3 -> 4 -> 2 -> 8 -> 5 -> 2 -> 4 -> 3 -> 6 -> 7 -> 8 -> 4 -> 2 -> 5 -> 1 -> 8 -> 7 -> 6 -> 4 -> 1 -> 5 -> 2 -> 1 -> 4 -> 3 

A*
 nodes expanded: 379
 path: 6 -> 2 -> 4 -> 8 -> 3 -> 4 -> 8 -> 5 -> 1 -> 8 -> 2 -> 7 -> 8 -> 2 -> 5 -> 1 -> 2 -> 5 -> 4 -> 3 
```

In which we can see:
1. GBFS didn't find the optimal solution. This is happening because the GBFS does not take care of the past, but only look of the future (the heuristic)
2. A* expanded more nodes than GBFS. I actually don't know why this happens, but testing shows that the Manhattan heuristic has the same behavior.
---
