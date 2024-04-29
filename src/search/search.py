#search.py
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

from cmath import inf
from itertools import accumulate
from queue import PriorityQueue
import random
import util

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

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    # graphs may contian cycles, so we need to keep track of visited nodes
    visited = set()
    stack = util.Stack()
    # find the initial state and push it to queue
    initialState = problem.getStartState()
    startNode = (initialState, '', 0, [])
    stack.push(startNode)
    # loop until the stack is empty
    while not stack.isEmpty():
        currentNode = stack.pop()
        state, action, cost, path = currentNode
        if not state in visited:
            visited.add(state)
            # check if goal state
            if problem.isGoalState(state):
                return path[1:] + [currentNode[1]]
            # expand node to get successors
            for succ in problem.getSuccessors(state):
                succState, succAction, succCost = succ
                newNode = (succState, succAction, cost + succCost, path + [action])
                stack.push(newNode)
    # there is no solution
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # graphs may contian cycles, so we need to keep track of visited nodes
    visited = set()
    queue = util.Queue()
    # find the initial state and push it to queue
    initialState = problem.getStartState()
    startNode = (initialState, '', 0, [])
    queue.push(startNode)
    # loop until the stack is empty
    while not queue.isEmpty():
        currentNode = queue.pop()
        state, action, cost, path = currentNode
        if not state in visited:
            visited.add(state)
            # check if goal state
            if problem.isGoalState(state):
                return path[1:] + [currentNode[1]]
            # expand node to get successors
            for succ in problem.getSuccessors(state):
                succState, succAction, succCost = succ
                newNode = (succState, succAction, cost + succCost, path + [action])
                queue.push(newNode)
    # there is no solution
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    visited = set()
    myPQ = util.PriorityQueue()
    # find the initial state and push it to queue
    initialState = problem.getStartState()
    startNode = (initialState, '', 0, [])
    myPQ.push(startNode, 0)
    # loop until the stack is empty
    while not myPQ.isEmpty():
        currentNode = myPQ.pop()
        state, action, cost, path = currentNode
        if not state in visited:
            visited.add(state)
            # check if goal state
            if problem.isGoalState(state):
                return path[1:] + [currentNode[1]]
            # expand node to get successors
            for succ in problem.getSuccessors(state):
                succState, succAction, succCost = succ
                totalCost = cost + succCost
                newNode = (succState, succAction, totalCost, path + [action])
                myPQ.push(newNode, totalCost)
    # there is no solution
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# Please DO NOT change the following code, we will use it later
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    myPQ = util.PriorityQueue()
    startState = problem.getStartState()
    startNode = (startState, '',0, [])
    myPQ.push(startNode,heuristic(startState,problem))
    visited = set()
    best_g = dict()
    while not myPQ.isEmpty():
        node = myPQ.pop()
        state, action, cost, path = node
        if (not state in visited) or cost < best_g.get(state):
            visited.add(state)
            best_g[state]=cost
            if problem.isGoalState(state):
                path = path + [(state, action)]
                actions = [action[1] for action in path]
                del actions[0]
                return actions
            for succ in problem.getSuccessors(state):
                succState, succAction, succCost = succ
                newNode = (succState, succAction, cost + succCost, path + [(state, action)])
                myPQ.push(newNode,heuristic(succState,problem)+cost+succCost)
    util.raiseNotDefined()

def enforcedHillClimbing(problem, heuristic=nullHeuristic):
    """
    Local search with heuristic function.
    You DO NOT need to implement any heuristic, but you DO have to call it.
    The heuristic function is "manhattanHeuristic" from searchAgent.py.
    It will be pass to this function as second argument (heuristic).
    """
    "*** YOUR CODE HERE FOR TASK 1 ***"
    # make root node
    initialState = problem.getStartState()
    startNode = (initialState, '', 0, [])
    while not problem.isGoalState(startNode[0]):
        startNode = improve(startNode, problem, heuristic)
    path = extractPath(startNode)
    print("path: ", path)
    return path

# Know why you didn't pass the test-cases
# improve the code
def improve(startNode, problem, heuristic=nullHeuristic):
    """Breadth-First Search approach to improve the local search"""
    queue = util.Queue() # open list (FIFO)
    queue.push(startNode)
    visited = set() # closed list
    # loop until the stack is empty
    while not queue.isEmpty():
        currentNode = queue.pop()
        state, action, cost, path = currentNode
        if not state in visited:
            visited.add(state)
            # if we find a better node with shorter heuristic to goal state, return it
            if heuristic(state,problem) < heuristic(startNode[0],problem):
                return currentNode
            # expand node to get successors
            for succ in problem.getSuccessors(state):
                succState, succAction, succCost = succ
                newNode = (succState, succAction, cost + succCost, path + [(state, action)])
                queue.push(newNode)
    util.raiseNotDefined()

def extractPath(goalNode):
    """Extract the path from the node"""
    state, action, cost, totalPath = goalNode
    actions = [x[1] for x in totalPath[1:]]
    actions = actions + [action]
    return actions

from math import inf as INF   
def bidirectionalAStarEnhanced(problem, heuristic=nullHeuristic, backwardsHeuristic=nullHeuristic):
    """
    Bidirectional global search with heuristic function.
    You DO NOT need to implement any heuristic, but you DO have to call them.
    The heuristic functions are "manhattanHeuristic" and "backwardsManhattanHeuristic" from searchAgent.py.
    It will be pass to this function as second and third arguments.
    You can call it by using: heuristic(state,problem) or backwardsHeuristic(state,problem)
    """
    "*** YOUR CODE HERE FOR TASK 2 ***"
    startState = problem.getStartState()
    goalStates = problem.getGoalStates()
    # The problem passed in going to be BidirectionalPositionSearchProblem    
    fPQ = util.PriorityQueue() # open list forward
    bPQ = util.PriorityQueue() # open list backward

    fVisited = set() # closed list forward
    bVisited = set() # closed list backward
    lowerBound = 0 # lower bound
    upperBound = INF # upper bound
    bestPlan = []   
    x = 0 # start forward - binary {0: 'forward', 1: ''backward'}

    # Initialize the open and closed lists
    startNode = (startState, '', 0, [])
    fPQ.push(startNode,heuristic(startState,problem))
    # create multiple goal nodes and put them to fringe
    for goalState in goalStates:
        goalNode = (goalState, '', 0, [])
        bPQ.push(goalNode,backwardsHeuristic(goalState,problem))
    
    # Loop until the open lists (frontier) is empty
    while (not fPQ.isEmpty() and not bPQ.isEmpty()):
        # get min priority values
        # if the heuristic is admissible, then the minimum  
        # value in the open lists represent a lower bound on the 
        # optimal solution cost
        bMinf = fPQ.getMinimumPriority()
        bMinb = bPQ.getMinimumPriority()
        # update lower bound
        lowerBound = (bMinf + bMinb) / 2 # tracks average f(n)
        currentNode = None

        # forward and backward expansion
        if x == 0: # forward
            # print("forward direction:")
            currentNode = fPQ.pop()
            fVisited.add(currentNode[0])
            # check if directions meet if so update plan and upper bound
            upperBound, bestPlan = checkMembership(currentNode, bPQ, upperBound, bestPlan, direction=x)
            # check if lower bound is greater than upper bound
            if lowerBound >= upperBound:
                print("Forward BestPlan: ", bestPlan)
                print("Length Forward BestPlan: ", len(bestPlan))
                return bestPlan
        
            # expand node to get forward successors
            for succ in problem.getSuccessors(currentNode[0]):
                succState, succAction, succCost = succ
                if (succState not in fVisited):
                    # accumulated cost to reach n
                    accCost = currentNode[2] + succCost
                    bfValue = 2*accCost + (heuristic(succState,problem) - backwardsHeuristic(succState,problem))
                    newNode = (succState, succAction, accCost, currentNode[3] + [succAction])
                    fPQ.push(newNode, bfValue)

        # backward iteration
        elif x==1: # backward
            # print("backward direction:")
            currentNode = bPQ.pop()
            bVisited.add(currentNode[0])
            # check if directions meet if so update plan and upper bound
            upperBound, bestPlan = checkMembership(currentNode, fPQ, upperBound, bestPlan, direction=x)
            # check if lower bound is greater than upper bound
            if lowerBound >= upperBound:
                print("Backward BestPlan: ", bestPlan)
                print("Length Backward BestPlan: ", len(bestPlan))
                return bestPlan
            
            # expand node to get backward successors
            for succ in problem.getBackwardsSuccessors(currentNode[0]):
                succState, succAction, succCost = succ
                if (succState not in bVisited):
                    # accumulated cost to reach n
                    accCost = currentNode[2] + succCost
                    bbValue = 2*accCost + (backwardsHeuristic(succState,problem) - heuristic(succState,problem))
                    newNode = (succState, succAction, accCost, [succAction] + currentNode[3]) # reverse
                    bPQ.push(newNode, bbValue)
        # choose direction
        x = chooseDirection(x)
    util.raiseNotDefined()


####### IDEA 2 #######
######################
def bidirectionalAStarEnhanced1(problem, heuristic=nullHeuristic, backwardsHeuristic=nullHeuristic):
    """
    Bidirectional global search with heuristic function.
    You DO NOT need to implement any heuristic, but you DO have to call them.
    The heuristic functions are "manhattanHeuristic" and "backwardsManhattanHeuristic" from searchAgent.py.
    It will be pass to this function as second and third arguments.
    You can call it by using: heuristic(state,problem) or backwardsHeuristic(state,problem)
    """
    "*** YOUR CODE HERE FOR TASK 2 ***"
    # Initialize start state and goal states
    startState = problem.getStartState()
    goalStates = problem.getGoalStates()
    bestPlan = []
    goalsVisited = [] # helper
    while len(goalStates):
        closestGoalState = findClosestGoalState(startState, goalStates)
        # Update the problem defintion
        setattr(problem, 'goalToVisit', closestGoalState)
        setattr(problem, 'start', startState)
        # Find the best path
        currentPlan = findBestPath(startState, closestGoalState, problem, heuristic, backwardsHeuristic)
        # Update start state and goal states
        startState = closestGoalState
        # append the new segment to the plan
        bestPlan = bestPlan + currentPlan
        goalsVisited.append(closestGoalState)
        if len(goalStates) == 0:
            return bestPlan
        goalStates.remove(closestGoalState)
    return bestPlan


def findBestPath(startState, goalState, problem, heuristic=nullHeuristic, backwardsHeuristic=nullHeuristic):
    # The problem passed in going to be BidirectionalPositionSearchProblem    
    fPQ = util.PriorityQueue() # open list forward
    bPQ = util.PriorityQueue() # open list backward
    fVisited = set() # closed list forward
    bVisited = set() # closed list backward
    lowerBound = 0 # lower bound
    upperBound = INF # upper bound
    currentPlan = [] # path
    x = 0 # start forward - binary {0: 'forward', 1: ''backward'}
    
    # Initialize the open and closed lists
    startNode = (startState, '', 0, [])
    fPQ.push(startNode,heuristic(startState,problem))
    goalNode = (goalState, '', 0, [])
    bPQ.push(goalNode,backwardsHeuristic(goalState,problem))
    # helper function to check if directions meet
    nodesExpanded = []
    
    # Loop until the open lists (frontier) is empty
    while (not fPQ.isEmpty() and not bPQ.isEmpty()):
        # get min priority values
        bMinf = fPQ.getMinimumPriority()
        bMinb = bPQ.getMinimumPriority()
        # update lower bound
        lowerBound = (bMinf + bMinb) / 2
        currentNode = None

        # forward and backward expansion
        if x == 0: # forward
            # print("forward direction:")
            currentNode = fPQ.pop()
            fVisited.add(currentNode[0])
            # check if directions meet if so update plan and upper bound
            upperBound, currentPlan = checkMembership(currentNode, bPQ, upperBound, currentPlan, direction=x)
            # check if lower bound is greater than upper bound
            if lowerBound >= upperBound:
                # more then one goal state
                return currentPlan
        
            # expand node to get forward successors
            for succ in problem.getSuccessors(currentNode[0]):
                succState, succAction, succCost = succ
                if (succState not in fVisited):
                    # accumulated cost to reach n
                    accCost = currentNode[2] + succCost
                    # dfValue = accCost - backwardsHeuristic(succState,problem) # dx(n) = gx(n) - hx_hat(n)
                    # ffValue = accCost + heuristic(succState,problem) # fx(n) = gx(n) + hx(n)
                    # bfValue = ffValue + dfValue 
                    # 2gx(n) + hx(n) - hx_hat(n)
                    bfValue = 2*accCost + (heuristic(succState,problem) - backwardsHeuristic(succState,problem))
                    newNode = (succState, succAction, accCost, currentNode[3] + [succAction])
                    fPQ.push(newNode, bfValue)

        # backward iteration
        elif x==1: # backward
            # print("backward direction:")
            currentNode = bPQ.pop()
            bVisited.add(currentNode[0])
            # check if directions meet if so update plan and upper bound
            upperBound, currentPlan = checkMembership(currentNode, fPQ, upperBound, currentPlan, direction=x)
            # check if lower bound is greater than upper bound
            if lowerBound >= upperBound:
                # return the first plan found
                return currentPlan
            
            # expand node to get backward successors
            for succ in problem.getBackwardsSuccessors(currentNode[0]):
                succState, succAction, succCost = succ
                if (succState not in bVisited):
                    # accumulated cost to reach n
                    accCost = currentNode[2] + succCost
                    # dbValue = accCost - heuristic(succState,problem) # dx(n) = gx(n) - h(n)
                    # fbValue = accCost + backwardsHeuristic(succState,problem) # fx(n) = gx(n) + hx_hat(n)
                    # bbValue = fbValue + dbValue
                    # 2gx(n) + hx_hat(n) - hx(n)
                    bbValue = 2*accCost + (backwardsHeuristic(succState,problem) - heuristic(succState,problem))
                    newNode = (succState, succAction, accCost, currentNode[3] + [succAction])
                    bPQ.push(newNode, bbValue)
        # choose direction
        x = chooseDirection(x)
    util.raiseNotDefined()

def findClosestGoalState(currentState, goalStates):
    """Find the closest goal state"""
    closestGoalState = None
    closestGoalStateDistance = INF
    if len(goalStates) == 1:
        # only single goal state
        closestGoalState = goalStates.pop()
    for goalState in goalStates:
        # multiple goal states
        distance = util.manhattanDistance(currentState[0], goalState[0])
        if distance < closestGoalStateDistance:
            closestGoalStateDistance = distance
            closestGoalState = goalState
    return closestGoalState
    
def checkMembership(currentNode, oppositePQ, upperBound, bestPlan, direction=0):
    """Check if the frontiers have met"""
    oppositeOpenDict = createOpenListDict(oppositePQ)
    state, action, cost, path = currentNode
    # check if directions meet if so update plan and upper bound
    oppositeStateList = list(oppositeOpenDict.keys())
    if state in oppositeStateList:
        oppositeNode = oppositeOpenDict[state]
        totalCost = cost + oppositeNode.cost
        # check if total cost is less than best solution
        if totalCost < upperBound:
            upperBound = totalCost
            if direction == 0:
                # backwards path
                reversedPath = oppositeNode.path # oppositeNode.path[::-1]
                # forwards path
                path = path
            else:
                # backwards path
                reversedPath = path # path[::-1]
                # forwards path
                path = oppositeNode.path
            # only add them together with function construction
            bestPlan = path + reversedPath # extract plan from node
    return upperBound, bestPlan

def createOpenListDict(oppositePQ):
    """Create a dictionary of the opposite open list"""
    oppositeOpenDict = {}
    for state in oppositePQ.heap:
        newNode = Node(state[2][0], state[2][1], state[2][2], state[2][3])
        oppositeOpenDict[state[2][0]] = newNode
    return oppositeOpenDict

def chooseDirection(x): # TODO
    """Choose the direction of the search"""
    return 1 - x # swap 0 and 1

class Node(object):
    """Node class for the bidirectional search"""
    def __init__(self, state, action, cost, path) -> None:
        self.state = state
        self.action = action
        self.cost = cost
        self.path = path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

ehc = enforcedHillClimbing
bae = bidirectionalAStarEnhanced