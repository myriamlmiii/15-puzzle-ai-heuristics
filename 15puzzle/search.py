# search.py
# ---------
# Licensing Information: You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

"""
In search.py, we implement generic search algorithms that can be used with different heuristics
and are compatible with external scripts for automation and further analysis.
"""

import math
import time
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

def Branching_factor(depth, num_expandedNodes):
    if depth == 0:
        return 'ERROR'
    return round(math.pow(num_expandedNodes, (1 / depth)), 3)

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze. For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """Search the deepest nodes in the search tree first."""
    frontier = util.Stack()
    explored = set()
    frontier.push((problem.getStartState(), [], 0))  # (state, actions, current depth)
    expanded_nodes = 0
    max_fringe_size = 0

    while not frontier.isEmpty():
        state, actions, depth = frontier.pop()
        if state not in explored:
            explored.add(state)
            expanded_nodes += 1

            if problem.isGoalState(state):
                return len(actions), expanded_nodes, max_fringe_size

            for successor, action, _ in problem.getSuccessors(state):
                frontier.push((successor, actions + [action], depth + 1))
                max_fringe_size = max(max_fringe_size, len(frontier.list))

    return None, expanded_nodes, max_fringe_size

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    frontier = util.Queue()
    explored = set()
    frontier.push((problem.getStartState(), [], 0))
    expanded_nodes = 0
    max_fringe_size = 0

    while not frontier.isEmpty():
        state, actions, _ = frontier.pop()
        if state not in explored:
            explored.add(state)
            expanded_nodes += 1

            if problem.isGoalState(state):
                return len(actions), expanded_nodes, max_fringe_size

            for successor, action, _ in problem.getSuccessors(state):
                frontier.push((successor, actions + [action], 0))
                max_fringe_size = max(max_fringe_size, len(frontier.list))

    return None, expanded_nodes, max_fringe_size

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    frontier = util.PriorityQueue()
    explored = set()
    frontier.push((problem.getStartState(), [], 0), 0)
    expanded_nodes = 0
    max_fringe_size = 0

    while not frontier.isEmpty():
        state, actions, cost = frontier.pop()
        if state not in explored:
            explored.add(state)
            expanded_nodes += 1

            if problem.isGoalState(state):
                return len(actions), expanded_nodes, max_fringe_size

            for successor, action, step_cost in problem.getSuccessors(state):
                new_actions = actions + [action]
                new_cost = cost + step_cost
                frontier.update((successor, new_actions, new_cost), new_cost)
                max_fringe_size = max(max_fringe_size, len(frontier.heap))

    return None, expanded_nodes, max_fringe_size
  #start of task 2
def nullHeuristic(state, problem=None):
    """A trivial heuristic function that always returns 0."""
    return 0

# Heuristic functions
def H1(state, problem=None):
    """Number of misplaced tiles heuristic."""
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
    current_state = [tile for row in state.cells for tile in row]
    return sum([1 for i in range(16) if current_state[i] != goal_state[i] and current_state[i] != 0])

def H2(state, problem=None):
    """Euclidean distance heuristic."""
    goal_positions = {val: (val // 4, val % 4) for val in range(16)}
    total_distance = 0
    for r in range(4):
        for c in range(4):
            tile = state.cells[r][c]
            if tile != 0:
                goal_r, goal_c = goal_positions[tile]
                total_distance += ((goal_r - r) ** 2 + (goal_c - c) ** 2) ** 0.5
    return total_distance

def H3(state, problem=None):
    """Manhattan distance heuristic."""
    goal_positions = {val: (val // 4, val % 4) for val in range(16)}
    total_distance = 0
    for r in range(4):
        for c in range(4):
            tile = state.cells[r][c]
            if tile != 0:
                goal_r, goal_c = goal_positions[tile]
                total_distance += abs(goal_r - r) + abs(goal_c - c)
    return total_distance

def H4(state, problem=None):
    """Heuristic based on tiles not in their goal row and/or column."""
    goal_positions = {val: (val // 4, val % 4) for val in range(16)}
    not_in_row = 0
    not_in_column = 0
    for r in range(4):
        for c in range(4):
            tile = state.cells[r][c]
            if tile != 0:
                goal_r, goal_c = goal_positions[tile]
                if goal_r != r:
                    not_in_row += 1
                if goal_c != c:
                    not_in_column += 1
    return not_in_row + not_in_column

#end of task 2 

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = util.PriorityQueue()
    start = problem.getStartState()
    frontier.push((start, [], 0), heuristic(start, problem))
    visited = set()
    expandedNodes = 0
    maxFringeSize = 0
    depth = 0
    start_time = time.time()

    while not frontier.isEmpty():
        state, actions, cost = frontier.pop()

        if problem.isGoalState(state):
            return {
                'Solved': True,
                'Solution': actions,
                'Depth': len(actions),
                'Expanded Nodes': expandedNodes,
                'Max Fringe Size': maxFringeSize,
                'Time': time.time() - start_time
            }

        if state not in visited:
            visited.add(state)
            expandedNodes += 1
            depth = max(depth, len(actions))

            for nextState, action, nextCost in problem.getSuccessors(state):
                newActions = actions + [action]
                frontier.push((nextState, newActions, cost + nextCost), cost + nextCost + heuristic(nextState, problem))
            maxFringeSize = max(maxFringeSize, frontier.count)

    return {
        'Solved': False,
        'Solution': None,
        'Depth': 0,
        'Expanded Nodes': expandedNodes,
        'Max Fringe Size': maxFringeSize,
        'Time': time.time() - start_time
    }

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
ucs = uniformCostSearch
astar = aStarSearch
