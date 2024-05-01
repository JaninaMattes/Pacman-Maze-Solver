# searchAgents.py
# ---------------
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
This file contains all of the agents that can be selected to control Pacman.  To
select an agent, use the '-p' option when running pacman.py.  Arguments can be
passed to your agent using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run the following command:

> python pacman.py -p SearchAgent -a fn=depthFirstSearch

Commands to invoke other search strategies can be found in the project
description.

Please only change the parts of the file you are asked to.  Look for the lines
that say

"*** YOUR CODE HERE ***"


The parts you fill in start about 3/4 of the way down.  Follow the project
description for details.

Good luck and happy searching!
"""

import numpy as np
import time, search 

import utils.util as util
import search.search as search

from game import Directions
from game import Agent
from game import Actions
from game import Grid

class GoWestAgent(Agent):
    "An agent that goes West until it can't."

    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        if Directions.WEST in state.getLegalPacmanActions():
            return Directions.WEST
        else:
            return Directions.STOP

#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of search.py          #
#######################################################

class SearchAgent(Agent):
    """
    This very general search agent finds a path using a supplied search
    algorithm for a supplied search problem, then returns actions to follow that
    path.

    As a default, this agent runs DFS on a PositionSearchProblem to find
    location (1,1)

    Options for fn include:
      depthFirstSearch or dfs
      breadthFirstSearch or bfs


    Note: You should NOT change any code in SearchAgent
    """

    def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
        # Warning: some advanced Python magic is employed below to find the right functions and problems

        # Get the search function from the name and heuristic
        if fn not in dir(search):
            raise AttributeError(fn + ' is not a search function in search.py.')
        func = getattr(search, fn)
        if 'heuristic' not in func.__code__.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
                print('[SearchAgent] using heuristic ' + heuristic)
            elif heuristic in dir(search):
                heur = getattr(search, heuristic)
                print('[SearchAgent] using heuristic ' + heuristic)
            else:
                raise AttributeError(heuristic + ' is not a function in searchAgents.py or search.py.')
            print('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))
            # Note: this bit of Python trickery combines the search algorithm and the heuristic
            self.searchFunction = lambda x: func(x, heuristic=heur)

        # Get the search problem type from the name
        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError(prob + ' is not a search problem type in SearchAgents.py.')
        self.searchType = globals()[prob]
        print('[SearchAgent] using problem type ' + prob)

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game
        board. Here, we choose a path to the goal. In this phase, the agent
        should compute the path to the goal and store it in a local variable.
        All of the work is done in this method!

        state: a GameState object (pacman.py)
        """
        if self.searchFunction == None: raise Exception("No search function provided for SearchAgent")
        starttime = time.time()
        problem = self.searchType(state) # Makes a new search problem
        self.actions  = self.searchFunction(problem) # Find a path
        totalCost = problem.getCostOfActions(self.actions)
        print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
        if '_expanded' in dir(problem): print('Search nodes expanded: %d' % problem._expanded)

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in
        registerInitialState).  Return Directions.STOP if there is no further
        action to take.

        state: a GameState object (pacman.py)
        """
        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP

class PositionSearchProblem(search.SearchProblem):
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True, visualize=True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print('Warning: this does not look like a regular search maze')

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable

        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state
            dx, dy = Actions.directionToVector(action)
            next_x, next_y = int(x + dx), int(y + dy)
            if not self.walls[next_x][next_y]:
                nextState = (next_x, next_y)
                cost = self.costFn(nextState)
                successors.append( ( nextState, action, cost) )

        # Bookkeeping for display purposes
        self._expanded += 1 # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999.
        """
        if actions == None: return 999999
        x,y= self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x,y))
        return cost

class StayEastSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the West side of the board.

    The cost function for stepping into a position (x,y) is 1/2^x.
    """
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: .5 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn, (1, 1), None, False)

class StayWestSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the East side of the board.

    The cost function for stepping into a position (x,y) is 2^x.
    """
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: 2 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn)

def manhattanHeuristic(position, problem, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def euclideanHeuristic(position, problem, info={}):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################

class CornersProblem(search.SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.
    You must select a suitable state space and successor function
    """

    def __init__(self, startingGameState):
        """
        Stores the walls, pacman's starting position and corners.
        """
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top, right = self.walls.height-2, self.walls.width-2
        self.corners = ((1,1), (1,top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print('Warning: no food in corner ' + str(corner))
        # Please add any code here which you would like to use
        # in initializing the problem
        "*** YOUR CODE HERE ***"
        self.cost = 1 # Cost per step is 1
        self.start = (self.startingPosition, ())
        self._visited, self._vistiedState, self._expanded = [], {}, 0 # DO NOT CHANGE; Number of search nodes expanded
        
    def getStartState(self):
        """
        Returns the start state (in your state space, not the full Pacman state
        space)
        """
        "*** YOUR CODE HERE ***"
        return self.start

    def isGoalState(self, state):
        """
        Returns whether this search state is a goal state of the problem.
        """
        "*** YOUR CODE HERE ***"
        _, cornersToVisit = state
        return len(cornersToVisit) == len(self.corners)

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
            For a given state, this should return a list of triples, (successor,
            action, stepCost), where 'successor' is a successor to the current
            state, 'action' is the action required to get there, and 'stepCost'
            is the incremental cost of expanding to that successor
        """
        "*** YOUR CODE HERE ***"
        successors = []
        self._expanded += 1 # DO NOT CHANGE
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            # Add a successor state to the successor list if the action is legal
            # Here's a code snippet for figuring out whether a new position hits a wall:
            currentPosition, cornersVisited = state
            dx, dy = Actions.directionToVector(action)
            x,y = currentPosition
            next_x, next_y = int(x + dx), int(y + dy)
            hitsWall = self.walls[next_x][next_y]
            if not hitsWall:
                nextPosition = (next_x, next_y)
                if nextPosition in self.corners:
                    if nextPosition not in cornersVisited:
                        print("Corners visited: ", cornersVisited)
                        cornersVisited = cornersVisited + (nextPosition,)
                nextState = (nextPosition, cornersVisited)
                successors.append((nextState, action, self.cost))
        return successors

    
    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999.  This is implemented for you.
        """
        if actions == None: return 999999
        x,y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)


def cornersHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

      state:   The current search state
               (a data structure you chose in your search problem)

      problem: The CornersProblem instance for this layout.

    This function should always return a number that is a lower bound on the
    shortest path from the state to a goal of the problem; i.e.  it should be
    admissible (as well as consistent).
    """
    corners = problem.corners # These are the corner coordinates
    walls = problem.walls # These are the walls of the maze, as a Grid (game.py)
    distance = []
    "*** YOUR CODE HERE ***"
    currentPosition, cornersToVisit = state
    unVisitedCorners = [corner for corner in corners if corner not in cornersToVisit]
    for corner in unVisitedCorners:
        distance.append(util.manhattanDistance(currentPosition, corner))
    
    return min(distance) if unVisitedCorners else 0 # Default to trivial solution

class AStarCornersAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, cornersHeuristic)
        self.searchType = CornersProblem

class FoodSearchProblem:
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """
    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0 # DO NOT CHANGE
        self.heuristicInfo = {} # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        self._expanded += 1 # DO NOT CHANGE
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state[0]
            dx, dy = Actions.directionToVector(direction)
            next_x, next_y = int(x + dx), int(y + dy)
            if not self.walls[next_x][next_y]:
                nextFood = state[1].copy()
                nextFood[next_x][next_y] = False
                successors.append( ( ((next_x, next_y), nextFood), direction, 1) )
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x,y= self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost

class AStarFoodSearchAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, foodHeuristic)
        self.searchType = FoodSearchProblem

def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come
    up with an admissible heuristic; almost all admissible heuristics will be
    consistent as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the
    other hand, inadmissible or inconsistent heuristics may find optimal
    solutions, so be careful.

    The state is a tuple (pacmanPosition, foodGrid) where foodGrid is a Grid
    (see game.py) of either True or False. You can call foodGrid.asList() to get
    a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the
    problem. For example, problem.walls gives you a Grid of where the walls
    are.

    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access
    problem.heuristicInfo['wallCount']

    ** You code here"**
    """
    position, foodGrid = state
    walls = problem.walls

    foodItems = foodGrid.asList()
    currentPosition, goalsVisited = state
    distance = []

    unvisitedGoals = [item for item in foodItems if item not in goalsVisited]
    for item in unvisitedGoals:
        distance.append(util.manhattanDistance(currentPosition, item))

    # admissible heuristic - never overestimates the cost to reach the goal
    # Return the sum of distances to each unvisited food item
    return sum(distance) if len(distance) else 0


class ClosestDotSearchAgent(SearchAgent):
    "Search for all food using a sequence of searches"
    def registerInitialState(self, state):
        self.actions = []
        currentState = state
        while(currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState) # The missing piece
            self.actions += nextPathSegment
            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    t = (str(action), str(currentState))
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' % t)
                currentState = currentState.generateSuccessor(0, action)
        self.actionIndex = 0
        print('Path found with cost %d.' % len(self.actions))

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition()
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState)

        "*** YOUR CODE HERE ***"
        return search.breadthFirstSearch(problem)

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state
        "*** YOUR CODE HERE ***"
        return self.food[x][y]

def mazeDistance(point1, point2, gameState):
    """
    Returns the maze distance between any two points, using the search functions
    you have already built. The gameState can be any game state -- Pacman's
    position in that state is ignored.

    Example usage: mazeDistance( (2,4), (5,6), gameState)

    This might be a useful helper function for your ApproximateSearchAgent.
    """
    x1, y1 = point1
    x2, y2 = point2
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
    return len(search.bfs(prob))

class BidirectionalSearchAgent(Agent):
    """
    This very general search agent finds a path using a supplied search
    algorithm for a supplied search problem, then returns actions to follow that
    path.

    As a default, this agent runs DFS on a PositionSearchProblem to find
    location (1,1)

    Options for fn include:
      depthFirstSearch or dfs
      breadthFirstSearch or bfs


    Note: You should NOT change any code in SearchAgent
    """

    def __init__(self, fn='depthFirstSearch', prob='BidirectionalPositionSearchProblem', heuristic='nullHeuristic', backwardsHeuristic = 'nullHeuristic'):
        # Warning: some advanced Python magic is employed below to find the right functions and problems

        # Get the search function from the name and heuristic
        if fn not in dir(search):
            raise AttributeError(fn + ' is not a search function in search.py.')
        func = getattr(search, fn)
        if 'heuristic' not in func.__code__.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        elif 'backwardsHeuristic' not in func.__code__.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
                print('[SearchAgent] using forward heuristic ' + heuristic)
            elif heuristic in dir(search):
                heur = getattr(search, heuristic)
                print('[SearchAgent] using forward heuristic ' + heuristic)
            else:
                raise AttributeError(heuristic + ' is not a function in searchAgents.py or search.py.')
            if backwardsHeuristic in globals().keys():
                revheur = globals()[backwardsHeuristic]
                print('[SearchAgent] using backward heuristic ' + backwardsHeuristic)
            elif backwardsHeuristic in dir(search):
                revheur = getattr(search, backwardsHeuristic)
                print('[SearchAgent] using backward heuristic ' + backwardsHeuristic)
            else:
                raise AttributeError(backwardsHeuristic + ' is not a function in searchAgents.py or search.py.')
            
            print('[BidirectionalSearchAgent] using function %s, heuristic %s and backwardsHeuristic %s' % (fn, heuristic, backwardsHeuristic))
            # Note: this bit of Python trickery combines the search algorithm and the heuristic
            self.searchFunction = lambda x: func(x, heuristic=heur, backwardsHeuristic=revheur)

        # Get the search problem type from the name
        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError(prob + ' is not a search problem type in SearchAgents.py.')
        self.searchType = globals()[prob]
        print('[SearchAgent] using problem type ' + prob)

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game
        board. Here, we choose a path to the goal. In this phase, the agent
        should compute the path to the goal and store it in a local variable.
        All of the work is done in this method!

        state: a GameState object (pacman.py)
        """
        if self.searchFunction == None: raise Exception("No search function provided for SearchAgent")
        starttime = time.time()
        problem = self.searchType(state) # Makes a new search problem
        self.actions  = self.searchFunction(problem) # Find a path
        totalCost = problem.getCostOfActions(self.actions)
        print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
        if '_expanded' in dir(problem): print('Search nodes expanded: %d' % problem._expanded)

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in
        registerInitialState).  Return Directions.STOP if there is no further
        action to take.

        state: a GameState object (pacman.py)
        """
        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP

class BidirectionalPositionSearchProblem(search.SearchProblem):
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True, visualize=True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print('Warning: this does not look like a regular search maze')

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def getGoalStates(self):
        return [self.goal]
    
    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable

        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """
        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state
            dx, dy = Actions.directionToVector(action)
            next_x, next_y = int(x + dx), int(y + dy)
            if not self.walls[next_x][next_y]:
                nextState = (next_x, next_y)
                cost = self.costFn(nextState)
                successors.append( ( nextState, action, cost) )

        # Bookkeeping for display purposes
        self._expanded += 1 # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)
        return successors

    # def getBackwardsSuccessors(self, state):
    #     return self.getSuccessors(state)

    def getBackwardsSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """
        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state
            dx, dy = Actions.directionToVector(action)
            next_x, next_y = int(x + dx), int(y + dy)
            if not self.walls[next_x][next_y]:
                nextState = (next_x, next_y)
                cost = self.costFn(nextState)
                rev_action = Actions.reverseDirection(action)
                successors.append( ( nextState, rev_action, cost) )

        # Bookkeeping for display purposes
        self._expanded += 1 # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)
        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999.
        """
        if actions == None: return 999999
        x,y= self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x,y))
        return cost

class BidirectionalFoodSearchAgent(BidirectionalSearchAgent):
    "A BidirectionalSearchAgent for BidirectionalFoodSearchProblem using your Heuristic"
    def __init__(self, fn='depthFirstSearch', prob='BidirectionalFoodSearchProblem', heuristic='nullHeuristic', backwardsHeuristic = 'nullHeuristic'):
        super().__init__(fn, prob, heuristic, backwardsHeuristic)
        return

class BidirectionalFoodSearchProblem:
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    # Heuristic: charge more for dangerous steps in ghost-ridden areas or less for steps in food-rich areas

    startingGameState contains:
    getPacmanPosition() : a tuple (x,y) of integers specifying Pacman's position
    getFood()           : a Grid (see game.py) of either True or False, indicating food
    getWalls()          : a Grid (see game.py) of either True or False, indicating wall
    """
    def __init__(self, startingGameState):
        self.startingGameState = startingGameState
        # You might need to use the following variables
        self.init_pos = startingGameState.getPacmanPosition()
        self.foodGrid = startingGameState.getFood()
        self.walls = startingGameState.getWalls()
        # goal state is when all food is eaten
        self.emptyFoodGrid = Grid(self.foodGrid.width, self.foodGrid.height)
        
        """You code here for Task 3:"""
        # Define your initial state
        # 1: idea - search state is a tuple ( pacmanPosition, (visitedGoalStates) )
        self.start = (self.init_pos, ())
        # self.start = (self.init_pos, self.foodGrid) # initial state foodGrid = False
        # And if you have anything else want to initialize:
        self.cost = 1 # unform cost - every step costs 1
        self.goalToVisit = () # helper
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE  

    def getStartState(self):
        """You code here for Task 3:"""
        # You MUST implement this function to return the initial state
        return self.start
    
    def getGoalToVisit(self):
        return self.goalToVisit
        
    def getGoalStates(self):
        goal_states = []
        """You code here for Task 3:"""
        # You must generate all goal states
        goalStatesList = self.foodGrid.asList()
        for goal in goalStatesList:
            goal_states.append((goal, tuple(goalStatesList))) # fix goal definition
        return goal_states

    def isGoalState(self, state):
        """You code here for Task 3:"""
        # You MUST implement this function to return True or False
        # to indicate whether the given state is one of the goal state or not
        # we can check if we have visited all goal states
        return len(state[1]) == len(self.foodGrid.asList())
        # return state[1].count() == 0

    def getSuccessors(self, state):
        # You MUST implement this function to return a list of successors
        successors = []
        self._expanded += 1 # DO NOT CHANGE
        """You code here for Task 3:"""
        # There are four actions might be available:
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            currentPosition, goalsVisited = state
            x,y = currentPosition
            dx, dy = Actions.directionToVector(direction)
            next_x, next_y = int(x + dx), int(y + dy)
            hitsWall = self.walls[next_x][next_y]
            if not hitsWall:
                nextPosition = (next_x, next_y)
                if nextPosition in self.foodGrid.asList():
                    if nextPosition not in goalsVisited:
                        goalsVisited = goalsVisited + (nextPosition,)
                nextState = (nextPosition, goalsVisited)

                # alternatively use the grid to represnt the food
                # nextFood = state[1].copy()
                # nextFood[next_x][next_y] = False
                # successors.append( ( (nextPosition, nextFood), direction, cost) )

                successors.append((nextState, direction, self.cost))
        return successors
    
    def getBackwardsSuccessors(self, state):
        # You MUST implement this function to return a list of backwards successors
        # A successor is in the format of (next_state, action, cost)
        # DO reverse your action before you return it
        successors = []
        self._expanded += 1 # DO NOT CHANGE
        """You code here for Task 3:"""
        # There are four actions might be available:
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            currentPosition, goalsVisited = state
            x,y = currentPosition
            dx, dy = Actions.directionToVector(direction)
            next_x, next_y = int(x + dx), int(y + dy)
            hitsWall = self.walls[next_x][next_y]
            if not hitsWall:
                nextPosition = (next_x, next_y)
                if nextPosition in self.foodGrid.asList():
                    if nextPosition in goalsVisited:
                        helperVisited = list(goalsVisited)
                        helperVisited.remove(nextPosition)
                        goalsVisited = tuple(helperVisited)
                nextState = (nextPosition, goalsVisited)

                # alternatively use the grid to represnt the food
                # nextFood = state[1].copy()
                # nextFood[next_x][next_y] = True
                # successors.append( ( (nextPosition, nextFood), direction, cost) )

                # reverse the direction
                rev_direction = Actions.reverseDirection(direction)
                successors.append((nextState, rev_direction, self.cost))

        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        # this function will return the cost only for display purpose when you run your own test.
        "*** YOUR CODE HERE for Task 3 (optional) ***"
        if actions == None: return 999999
        x,y = self.init_pos
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)

def bidirectionalFoodProblemHeuristic(state, problem):
    "*** YOUR CODE HERE for Task 3 ***"
    #return calculatePermutation(state, problem)
    #return calculateRealMaxDistance(state, problem)
    #return calculateRealForwardsDistance(state, problem)
    # return calculatePermutation(state, problem)
    return calculateMinDistance(state, problem)

def bidirectionalFoodProblemBackwardsHeuristic(state, problem):
    "*** YOUR CODE HERE for Task 3 ***"
    # return calculateMinDistance(state, problem)
    return calculateDistanceToStart(state, problem)

# TODO: None of the heuristic functions are called with AStar search - check why
def calculateDistanceToStart(state, problem):
    currentPosition, goalsToVisit = state
    startState = problem.getStartState()[0]
    return util.manhattanDistance(currentPosition, startState)

def calculateRealForwardsDistance(state, problem):
    """Baseline heuristic: distance to single goal state"""
    currentPosition, goalsToVisit = state
    goalState = problem.getGoalToVisit()[0]
    return mazeDistance(currentPosition, goalState, problem.startingGameState)

def calculateRealBackwardsDistance(state, problem):
    """Baseline heuristic: distance to start state"""
    currentPosition, goalsToVisit = state
    startState = problem.getStartState()[0]
    return mazeDistance(currentPosition, startState, problem.startingGameState)

def calculateTotalDistance(state, problem):
    foodItems = problem.foodGrid.asList()
    currentPosition, goalsVisited = state
    unvisitedGoals = createNotInList(foodItems, goalsVisited)
    distance = 0
    for food in unvisitedGoals:
        distance += util.manhattanDistance(currentPosition, food) # Default to trivial solution
    return distance

def calculateMinDistance(state, problem):
    """Charges less if closer to goal and less goals to visit"""
    foodItems = problem.foodGrid.asList()
    currentPosition, goalsVisited = state
    distance = []
    unvisitedGoals = createNotInList(foodItems, goalsVisited)
    for item in unvisitedGoals:
        distance.append(util.manhattanDistance(currentPosition, item)) # Default to trivial solution
    return min(distance) if distance else 0

def calculateRealMaxDistance(state, problem):
    foodItems = problem.foodGrid.asList()
    currentPosition, goalsVisited = state
    distance = []
    unvisitedGoals = createNotInList(foodItems, goalsVisited)
    for item in unvisitedGoals:
        distance.append(mazeDistance(currentPosition, item, problem.startingGameState)) # Default to trivial solution
    return min(distance) if distance else 0

def calculateMaxDistance(state, problem):
    foodItems = problem.foodGrid.asList()
    currentPosition, goalsVisited = state
    distance = []
    unvisitedGoals = [item for item in foodItems if item not in goalsVisited]
    for item in unvisitedGoals:
        distance.append(util.manhattanDistance(currentPosition, item)) # Default to trivial solution
    return max(distance)

def calculateRealMinDistance(state, problem):
    foodItems = problem.foodGrid.asList()
    currentPosition, goalsVisited = state
    distance = []
    unvisitedGoals = createNotInList(foodItems, goalsVisited)
    for item in unvisitedGoals:
        distance.append(mazeDistance(currentPosition, item, problem.startingGameState)) # Default to trivial solution
    return max(distance) if distance else 0

def calculatePermutation(state, problem):
    foodItems = problem.foodGrid.asList()
    currentPosition, goalsVisited = state
    distance = []
    distanceBetween = []
    unvisitedGoals = [item for item in foodItems if item not in goalsVisited]
    for item in unvisitedGoals:
        distance.append(util.manhattanDistance(currentPosition, item)) # Default to trivial solution
        for item2 in unvisitedGoals:
            distanceBetween.append(util.manhattanDistance(item, item2))
    # distance between smallest and furthest away point
    minDist = min(distance) if len(distance) else 0
    maxDist = max(distanceBetween) if len(distanceBetween) else 0
    return minDist + maxDist

def calculateRealPermutation(state, problem):
    foodItems = problem.foodGrid.asList()
    currentPosition, goalsVisited = state
    distance = []
    distanceBetween = []
    unvisitedGoals = createNotInList(foodItems, goalsVisited)
    for item in unvisitedGoals:
        distance.append(mazeDistance(currentPosition, item, problem.startingGameState)) # Default to trivial solution
        for item2 in unvisitedGoals:
            distanceBetween.append(mazeDistance(item, item2, problem.startingGameState))
    # distance between smallest and furthest away point
    minDist = min(distance) if len(distance) else 0
    maxDist = max(distanceBetween) if len(distanceBetween) else 0
    return minDist + maxDist

def createNotInList(listOne, listTwo):
    """Returns a list of items in listOne that are not in listTwo"""
    return [item for item in listOne if item not in listTwo]

def manhattanHeuristic(state,problem=None):
    dist = util.manhattanDistance(state,problem.goal)
    return dist

def backwardsManhattanHeuristic(state,problem=None):
    dist = util.manhattanDistance(state,problem.getStartState())
    return dist