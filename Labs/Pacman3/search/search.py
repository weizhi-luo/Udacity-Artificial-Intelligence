# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
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
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
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

class Node:
    
    def __init__(self, state, action, cost, parent_node):
        self.state = state
        self.cost = cost
        self.parent_node = parent_node
        self.action = Directions.EAST if Directions.EAST == action else \
                      Directions.SOUTH if Directions.SOUTH == action else \
                      Directions.WEST if Directions.WEST == action else \
                      Directions.NORTH if Directions.NORTH == action else \
                      Directions.STOP if Directions.STOP == action else None
        
def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    
    if problem.isGoalState(start_state):
        return [Directions.STOP]
    
    explored_state = set()
    frontier = util.Stack()
    
    start_node = Node(start_state, None, None, None)
    frontier.push(start_node)
    
    while True:
        if frontier.isEmpty():
            return
        
        pop_node = frontier.pop()
        explored_state.add(pop_node.state)
        
        for successor in problem.getSuccessors(pop_node.state):
        #for successor in reversed(problem.getSuccessors(pop_node.state)):
            child = Node(successor[0], successor[1], successor[2], pop_node)
            
            if child.state not in explored_state:
                if problem.isGoalState(child.state):
                    actions = [child.action]
                    parent = child.parent_node
                    while parent != start_node:
                        actions.append(parent.action)
                        parent = parent.parent_node
                    return list(reversed(actions))
                frontier.push(child)
                
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()

    if problem.isGoalState(start_state):
        return [Directions.STOP]
    
    explored_state = set()
    frontier = util.Queue()
    
    start_node = Node(start_state, None, None, None)
    frontier.push(start_node)
    
    while True:
        if frontier.isEmpty():
            return
        
        pop_node = frontier.pop()
        explored_state.add(pop_node.state)
        
        for successor in problem.getSuccessors(pop_node.state):
            child = Node(successor[0], successor[1], successor[2], pop_node)
            
            if (child.state not in explored_state) and (child.state not in frontier.list):
                if problem.isGoalState(child.state):
                    actions = [child.action]
                    parent = child.parent_node
                    while parent != start_node:
                        actions.append(parent.action)
                        parent = parent.parent_node
                    return list(reversed(actions))
                frontier.push(child)
                
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    if problem.isGoalState(start_state):
        return [Directions.STOP]
    
    explored_state = set()
    frontier = util.PriorityQueue()
    state_g_score = dict()
    state_f_score = dict()
    state_parent_state = dict()

    state_g_score[start_state] = 0
    state_f_score[start_state] = heuristic(start_state, problem)
    state_parent_state[start_state] = None
    frontier.push(start_state, state_f_score[start_state])
    
    while True:
        if frontier.isEmpty():
            return
        
        pop_state = frontier.pop()
        if problem.isGoalState(pop_state):
            parent_state = state_parent_state[pop_state]
            actions = []
            path_state = pop_state
            while parent_state:
                if parent_state[0] - path_state[0] > 0:
                    actions.append(Directions.WEST)
                elif parent_state[0] - path_state[0] < 0:
                    actions.append(Directions.EAST)
                elif parent_state[1] - path_state[1] > 0:
                    actions.append(Directions.SOUTH)
                elif parent_state[1] - path_state[1] < 0:
                    actions.append(Directions.NORTH)
                path_state = parent_state
                parent_state = state_parent_state[path_state]
            return list(reversed(actions))
        
        explored_state.add(pop_state)
        
        for successor in problem.getSuccessors(pop_state):
            successor_state = successor[0]
            successor_cost = successor[2]
            if successor_state in explored_state:
                continue

            if (successor_state not in state_g_score) or ((state_g_score[pop_state] + successor_cost) < state_g_score[successor_state]):
                state_g_score[successor_state] = state_g_score[pop_state] + successor_cost
                state_f_score[successor_state] = state_g_score[successor_state] + heuristic(successor_state, problem)
                state_parent_state[successor_state] = pop_state
                if successor_state not in state_g_score:
                    frontier.push(successor_state, state_f_score[successor_state])
                else:
                    frontier.update(successor_state, state_f_score[successor_state])

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
