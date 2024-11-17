import sys
import heuristic
from searchAI import bfs, iddfs, gbfs, a_star
# import test

"""
=================================================================
                       problem formalization
=================================================================
"""
class SlidingPuzzle:
    """
       A class representing a sliding puzzle problem.

       Attributes:
           initial (tuple): The initial state of the puzzle.
           goal (tuple): The goal state of the puzzle (solved configuration).
           actions (tuple): The possible actions from each state
           size (int): The size of the puzzle (dimension of the square grid).
       """
    def __init__(self, initial_board):
        self.initial = initial_board
        self.goal = tuple(range(len(initial_board)))    # Goal state - (0, 1, 2, ..., n-1)
        self.actions = ("left", "right", "up", "down")  # referring as the moving tile is the blank tile
        self.size = int(len(initial_board) ** 0.5)      # number of tiles in col / row

    def action_cost(self, action):
        return 1

    def transition_model(self, state, action):
        """
        Applies the given action to the current state and returns the new state and moved tile.
        """
        i = state.index(0)
        new_index = i
        board = list(state)

        if action == 'left' and i % self.size != 0:
            new_index = i - 1
        elif action == 'right' and i % self.size != self.size - 1:
            new_index = i + 1
        elif action == "up" and i >= self.size:
            new_index = i - self.size
        elif action == "down" and i < self.size ** 2 - self.size:
            new_index = i + self.size

        board[i], board[new_index] = board[new_index], board[i]

        return tuple(board), board[i]

    def is_goal(self, state):
        return state == self.goal

# ------------------------------------------------------------------------------------


def main():

    initial_board = get_cli_input()
    sliding_puzzle = SlidingPuzzle(initial_board)

    print_info("BFS", *bfs(sliding_puzzle))
    print_info("IDDFS", *iddfs(sliding_puzzle))
    print_info("GBFS", *gbfs(sliding_puzzle, heuristic.liner_conflict))
    print_info("A*", *a_star(sliding_puzzle, heuristic.liner_conflict))


def get_stdin_input():
    print('Enter a board:')
    return tuple(map(int,(input().split())))

def get_cli_input():
    return tuple(map(int, sys.argv[1:]))

def print_info(func_name, end_node, count):
    print(func_name)
    print(f" nodes expanded: {count}")
    print(f" path: {end_node.get_path()}" if end_node is not None else " didn't find solution", "\n")



if __name__ == '__main__':
    main()





