from collections import deque
import heapq

MAX_DEPTH = 30

class Node:
    """
       A class representing a node in the search tree.

       Attributes:
           state (tuple): The current state that the represented be the node.
           parent (Node): The parent node (from which this node was expanded).
           action (str): The action taken to reach this node.
           path_cost (int): The cost of the path from the root node to this node.
       """
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def expand(self, problem):
        """
        Expands the current node into its child nodes by applying all possible actions.
        """
        children = []
        for action in problem.actions:
            new_state, moved_num = problem.transition_model(self.state, action)
            if new_state != self.state:
                cost = self.path_cost + problem.action_cost(action)
                children.append(Node(new_state, parent = self, action = moved_num, path_cost = cost))
        return children

    def __str__(self): # for debugging
        action = self.action or "init"
        return f"{action} {self.state}"

    def __lt__(self, other):
        # used by the heap when 2 node have the same heuristic value
        return self.state < other.state


    def get_path(self):
        """
            Traces back path in the search tree from node to the initial node
            by following parent nodes.
            """
        path = []
        node = self
        while node.parent is not None:
            path.insert(0, node.action)
            node = node.parent
        return ' -> '.join(map(str, path))

    """
        Traces back path in the search tree from node to the initial node 
        by following parent nodes.
        """

    def is_in_cycle(self):
        node = self.parent
        while node is not None:
            if node.state == self.state:
                return True
            node = node.parent
        return False

# ---------------------------------------------------------------




"""
=================================================================
                       Un-Informed Search
=================================================================
"""
def bfs(problem):
    node, count = Node(problem.initial), 0
    queue = deque([node])
    reached = {node.state}

    if problem.is_goal(node.state):
        return node, count

    while queue:
        node = queue.popleft() # pop in FIFO order
        count += 1

        for child in node.expand(problem):

            if problem.is_goal(child.state):
                return child, count

            if child.state not in reached:
                reached.add(child.state)
                queue.append(child)

    return None, count

# ---------------------------------------------------------------

def iddfs(problem):
    node, count = None, 0
    depth = 0
    while depth < MAX_DEPTH:
        node, curr_count = depth_limited_search(problem, depth)
        count += curr_count
        if node is not None: #found solution
            break

        depth += 1

    return node, count

def depth_limited_search(problem, limit_depth):
    stack = deque([(Node(problem.initial), 0)]) # each entry is (node, depth)
    count = 0

    while stack:
        node, depth = stack.pop() # pop from the head of the stack (LIFO)

        if problem.is_goal(node.state):
            return node, count

        if depth < limit_depth and not node.is_in_cycle():
            count += 1
            for child in node.expand(problem):
                stack.append((child, depth + 1))

    return None, count



"""
=================================================================
                        Informed Search
=================================================================
"""

def best_search_first(problem, evaluation_func):
    node = Node(problem.initial)
    priority_queue = [ (evaluation_func(node), node) ]
    reached = {node.state: 0} # dictionary of (k = state : v = path cost)
    count = 0

    while priority_queue:
        _,node = heapq.heappop(priority_queue) # pop the node with the smallest evaluation

        if problem.is_goal(node.state):
            return node, count

        count += 1
        for child in node.expand(problem):

            # if child is state that hasn't reached yet, or we found better path
            if child.state not in reached or child.path_cost < reached[child.state]:
                reached[child.state] = child.path_cost
                heapq.heappush(priority_queue, (evaluation_func(node), child))

    return None, count
# ---------------------------------------------------------------

def gbfs(problem, heuristic):
    return best_search_first(problem, heuristic)

# ---------------------------------------------------------------


def a_star(problem, heuristic):

    # inner function to evaluate A*'s f(n) = g(n) + h(n)
    def evaluate_a_star(node):
        # print(f"n={node}\tg(n)={node.path_cost} h(n)={heuristic(node)}")
        return node.path_cost + heuristic(node)

    return best_search_first(problem, evaluate_a_star)

# ---------------------------------------------------------------
