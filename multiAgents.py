# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util
import random
from game import Agent
from pacman import GhostRules

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        "Add more of your code here if you want to"
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        now = currentGameState.getPacmanPosition()
        next = successorGameState.getPacmanPosition()
        s = newScaredTimes[0]
        t = 100
        target=now
        ghostcount=currentGameState.getNumAgents()-1
        if (ghostcount>1):
            con=4
        else:
            con=3
        for i in range(ghostcount):
            ghost = successorGameState.getGhostPosition(i+1)
            if (abs(now[0] - ghost[0]) + abs(now[1] - ghost[1])<=con):               #if ghost comes close, run
                if ((abs(next[0] - ghost[0]) + abs(next[1] - ghost[1])) > (abs(now[0] - ghost[0]) + abs(now[1] - ghost[1]))):
                    return successorGameState.getScore()*100
                else:
                    return 0
        for i in newFood.asList():
            if (next == i):                                                     #if successor has food, go there
                print("\n\n\n")
                return successorGameState.getScore()*10
            dist = abs(now[0] - i[0]) + abs(now[1] - i[1])
            if (dist < t):
                t = dist
                target = i
        if ((abs(next[0] - target[0]) + abs(next[1] - target[1])) < (abs(now[0] - target[0]) + abs(now[1] - target[1]))): #if successor is closer to food than current, go there
            return successorGameState.getScore()+10
        if(action=='Stop'):
            return 0
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.capsules = []
        self.food = []
        self.previousGameState = 0

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    depth=0
    minply=1
    def minimaxDecision(self,gameState):
        """
        function MINIMAX DECISION (𝑠𝑡𝑎𝑡𝑒) returns an action
        return argmax𝑎∈ACTIONS(𝑠𝑡𝑎𝑡𝑒) MIN-VALUE(RESULT(𝑠𝑡𝑎𝑡𝑒,𝑎))
        """
        (state,v)=self.maxValue(gameState,0)

        #print("action=",state,v)
        return state
        util.raiseNotDefined()

    def CutOffTest(self, gameState, depth):
        """
        return true if depth>=d
        """
        if (depth>=self.depth):
            return 1
        else:
            return 0

    def maxValue(self, gameState,depth):
        """
        function MAX-VALUE(𝑠𝑡𝑎𝑡𝑒) returns a utility value
        ###if TERMINAL-TEST(𝑠𝑡𝑎𝑡𝑒) then return UTILITY(𝑠𝑡𝑎𝑡𝑒)###
        If CUTOFF-TEST(𝑠𝑡𝑎𝑡𝑒,𝑑𝑒𝑝𝑡ℎ) then return EVAL(𝑠𝑡𝑎𝑡𝑒)
         v←−∞
         for each a in ACTIONS(𝑠𝑡𝑎𝑡𝑒):
             v←MAX(v, MIN-VALUE(RESULT(𝑠𝑡𝑎𝑡𝑒,𝑎)))
         return v
        """
        legalMoves = []
        if(self.CutOffTest(gameState,depth))or(gameState.isWin())or(gameState.isLose()):
            return (0,self.evaluationFunction(gameState))
        (mpos,v)=(0,float('-inf'))
        legalMoves.extend(gameState.getLegalActions(0))
        for a in range(len(legalMoves)):
            _, u = self.minValue(gameState.generateSuccessor(self.index, legalMoves[a]), 1, depth)
            # if (u > v):
            #    (mpos, v) = (legalMoves[a], u)
            v = max(u, v)
            if (u == v):
                mpos = legalMoves[a]
        return (mpos,v)
        util.raiseNotDefined()

    def minValue(self, gameState, minply, depth):
        """
        function MIN-VALUE(𝑠𝑡𝑎𝑡𝑒) returns a utility value
        ###if TERMINAL-TEST(𝑠𝑡𝑎𝑡𝑒) then return UTILITY(𝑠𝑡𝑎𝑡𝑒)###
        If CUTOFF-TEST(𝑠𝑡𝑎𝑡𝑒,𝑑𝑒𝑝𝑡ℎ) then return EVAL(𝑠𝑡𝑎𝑡𝑒)
         v← +∞
         for each a in ACTIONS(𝑠𝑡𝑎𝑡𝑒) do
            v ←MIN(v,MAX-VALUE(RESULT(𝑠𝑡𝑎𝑡𝑒, 𝑎)))
         return v
        """
        legalMoves = []
        agnum=gameState.getNumAgents()
        if(self.CutOffTest(gameState,depth))or(gameState.isWin())or(gameState.isLose()):
            return (0,self.evaluationFunction(gameState))
        if(minply<agnum-1):
            (mpos, v) = (0, float('-inf'))
            legalMoves.extend(gameState.getLegalActions(minply))
            for a in range(len(legalMoves)):
                _, u = self.minValue(gameState.generateSuccessor(minply, legalMoves[a]),minply+1,depth)
                #if (u > v):
                #    (mpos, v) = (legalMoves[a], u)
                v=max(u,v)
                if(u==v):
                    mpos=legalMoves[a]
        elif(minply==agnum-1):
            (mpos, v) = (0, float('inf'))
            legalMoves.extend(gameState.getLegalActions(minply))
            for a in range(len(legalMoves)):
                _, u = self.maxValue(gameState.generateSuccessor(minply, legalMoves[a]),depth+1)
                #if (u < v):
                #    (mpos, v) = (legalMoves[a], u)
                v = min(u, v)
                if (u == v):
                    mpos = legalMoves[a]
        return (mpos, v)
        util.raiseNotDefined()

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        global depth
        depth=0
        return self.minimaxDecision(gameState)
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    depth = 0
    minply = 1

    def alphabetaDecision(self, gameState):
        (state, v) = self.abMaxValue(gameState, 0, -9999, +9999)

        # print("action=",state,v)
        return state
        util.raiseNotDefined()

    def CutOffTest(self, gameState, depth):
        """
        return true if depth>=d
        """
        if (depth >= self.depth):
            return 1
        else:
            return 0

    def abMaxValue(self, gameState, depth, alpha, beta):
        """
        function MAX-VALUE(𝑠𝑡𝑎𝑡𝑒) returns a utility value
        ###if TERMINAL-TEST(𝑠𝑡𝑎𝑡𝑒) then return UTILITY(𝑠𝑡𝑎𝑡𝑒)###
        If CUTOFF-TEST(𝑠𝑡𝑎𝑡𝑒,𝑑𝑒𝑝𝑡ℎ) then return EVAL(𝑠𝑡𝑎𝑡𝑒)
         v←−∞
         for each a in ACTIONS(𝑠𝑡𝑎𝑡𝑒):
             v←MAX(v, MIN-VALUE(RESULT(𝑠𝑡𝑎𝑡𝑒,𝑎)))
             if v>beta:
                return v
             alpha = max(alpha,v)
         return v
        """
        legalMoves = []
        if (self.CutOffTest(gameState, depth)) or (gameState.isWin()) or (gameState.isLose()):
            return (0, self.evaluationFunction(gameState))
        (mpos, v) = (0, -9999.0)
        legalMoves.extend(gameState.getLegalActions(0))
        for a in range(len(legalMoves)):
            _, u = self.abMinValue(gameState.generateSuccessor(self.index, legalMoves[a]), 1, depth, alpha, beta)
            if (u > v):
                (mpos, v) = (legalMoves[a], u)
            if (v>beta):
                return (mpos, v)
            if(v>alpha):
                alpha=v
            #alpha = max(alpha, v)
        return (mpos, v)
        util.raiseNotDefined()

    def abMinValue(self, gameState, minply, depth, alpha, beta):
        """
        function MIN-VALUE(𝑠𝑡𝑎𝑡𝑒) returns a utility value
        ###if TERMINAL-TEST(𝑠𝑡𝑎𝑡𝑒) then return UTILITY(𝑠𝑡𝑎𝑡𝑒)###
        If CUTOFF-TEST(𝑠𝑡𝑎𝑡𝑒,𝑑𝑒𝑝𝑡ℎ) then return EVAL(𝑠𝑡𝑎𝑡𝑒)
         v← +∞
         for each a in ACTIONS(𝑠𝑡𝑎𝑡𝑒) do
            v ←MIN(v,MAX-VALUE(RESULT(𝑠𝑡𝑎𝑡𝑒, α)))
            if v<alpha:
                return v
             beta = min(beta,v)
         return v
        """
        legalMoves = []
        agnum = gameState.getNumAgents()

        if (self.CutOffTest(gameState, depth)) or (gameState.isWin()) or (gameState.isLose()):
            return (0, self.evaluationFunction(gameState))

        if (minply < agnum - 1):
            (mpos, v) = (0, -9999.0)
            legalMoves.extend(gameState.getLegalActions(minply))
            for a in range(len(legalMoves)):
                _, u = self.abMinValue(gameState.generateSuccessor(minply, legalMoves[a]), minply + 1, depth, alpha, beta)
                if (u > v):
                    (mpos, v) = (legalMoves[a], u)
                if (v>beta):
                    return (mpos, v)
                if(v>alpha):
                    alpha=v
                #alpha = max(alpha, v)

        elif (minply == agnum - 1):
            (mpos, v) = (0, 9999.0)
            legalMoves.extend(gameState.getLegalActions(minply))
            for a in range(len(legalMoves)):
                _, u = self.abMaxValue(gameState.generateSuccessor(minply, legalMoves[a]), depth + 1, alpha, beta)
                if (u < v):
                    (mpos, v) = (legalMoves[a], u)
                if (v<alpha):
                    return (mpos,v)
                if (v<beta):
                    beta = v
                #beta = min(beta, v)

        return (mpos, v)
        util.raiseNotDefined()

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        global depth
        depth = 0
        return self.alphabetaDecision(gameState)
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    depth = 0
    minply = 1

    def expectimaxDecision(self, gameState):
        """
        function MINIMAX DECISION (𝑠𝑡𝑎𝑡𝑒) returns an action
        return argmax𝑎∈ACTIONS(𝑠𝑡𝑎𝑡𝑒) MIN-VALUE(RESULT(𝑠𝑡𝑎𝑡𝑒,𝑎))
        """
        (state, v) = self.expmaxValue(gameState, 0)

        #print("action=",state,v)
        return state
        util.raiseNotDefined()

    def CutOffTest(self, gameState, depth):
        """
        return true if depth>=d
        """
        if (depth >= self.depth):
            return 1
        else:
            return 0

    def expmaxValue(self, gameState, depth):
        """
        function MAX-VALUE(𝑠𝑡𝑎𝑡𝑒) returns a utility value
        ###if TERMINAL-TEST(𝑠𝑡𝑎𝑡𝑒) then return UTILITY(𝑠𝑡𝑎𝑡𝑒)###
        If CUTOFF-TEST(𝑠𝑡𝑎𝑡𝑒,𝑑𝑒𝑝𝑡ℎ) then return EVAL(𝑠𝑡𝑎𝑡𝑒)
         v←−∞
         for each a in ACTIONS(𝑠𝑡𝑎𝑡𝑒):
             v←MAX(v, CHANCE-VALUE(RESULT(state,a)))
         return v
        """
        legalMoves = []
        if (self.CutOffTest(gameState, depth)) or (gameState.isWin()) or (gameState.isLose()):
            return (0, self.evaluationFunction(gameState))
        legalMoves.extend(gameState.getLegalActions(0))
        (mpos, v) = (0, float('-inf'))
        #if (depth==0):
        #    print("\n\n\nnew",gameState.getPacmanPosition())
        for a in range(len(legalMoves)):
            _, u = self.chanceValue(gameState.generateSuccessor(self.index, legalMoves[a]), 1, depth)
            #if(depth==0):
            #    print(legalMoves[a],u)
            #v = max(u, v)
            #if (u == v):
            #    mpos = legalMoves[a]
            if (u > v):
                (mpos, v) = (legalMoves[a], u)
        return (mpos, v)
        util.raiseNotDefined()

    def chanceValue(self, gameState, minply, depth):
        """
        returns chance of each max action
        """
        legalMoves = []
        agnum = gameState.getNumAgents()
        if (self.CutOffTest(gameState, depth)) or (gameState.isWin()) or (gameState.isLose()):
            return (0, self.evaluationFunction(gameState))
        if (minply < agnum - 1):
            (mpos, v) = (0, 0)
            legalMoves.extend(gameState.getLegalActions(minply))
            for a in range(len(legalMoves)):
                _, u = self.chanceValue(gameState.generateSuccessor(minply, legalMoves[a]), minply + 1, depth)
                v = v + (1/len(legalMoves))*u
        elif (minply == agnum - 1):
            (mpos, v) = (0, 0)
            legalMoves.extend(gameState.getLegalActions(minply))
            for a in range(len(legalMoves)):
                _, u = self.expmaxValue(gameState.generateSuccessor(minply, legalMoves[a]), depth + 1)
                v = v + (1/len(legalMoves))*u
        mpos=0
        return (mpos, v)
        util.raiseNotDefined()


    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        global depth
        depth = 0
        MultiAgentSearchAgent.previousGameState=gameState

        #print("\n\n\n\n",gameState.getScore(), gameState.getPacmanState())
        return self.expectimaxDecision(gameState)
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    MultiAgentSearchAgent.capsules = MultiAgentSearchAgent.previousGameState.getCapsules()
    grid = MultiAgentSearchAgent.previousGameState.getFood()
    MultiAgentSearchAgent.food = grid.asList()
    score = currentGameState.getScore()
    position=currentGameState.getPacmanPosition()
    ghostpos = currentGameState.getGhostPosition(1)

    if ((abs(position[0] - ghostpos[0]) + abs(position[1] - ghostpos[1])) < 2):   #if ghost is close, run away
        score=score/10
    if position in MultiAgentSearchAgent.capsules:          #if there is a capsule go there
        score = score *10000

    distance = 7                                                                  #seach for food in your neighbourhood
    c = False
    for i in MultiAgentSearchAgent.food:
        if ((abs(position[0] - i[0]) + abs(position[1] - i[1])) < distance):
            distance = abs(position[0] - i[0]) + abs(position[1] - i[1])
            c = True
    if (c == True):
        score = score * 100 * (1 / (distance+1)) + random.uniform(0,1)
    if (c==False):                                    #if there is no food in your neighbourhood, search the whole grid
        distance = 30
        c = False
        for i in MultiAgentSearchAgent.food:
            #   print(i,abs(position[0] - i[0]) + abs(position[1] - i[1]))
            if ((abs(position[0] - i[0]) + abs(position[1] - i[1])) < distance):
                distance = abs(position[0] - i[0]) + abs(position[1] - i[1])
                c = True
        if (c == True):
            score = score * 100 * (1 / (distance + 1)) + random.uniform(0, 1)

    newGhostStates = currentGameState.getGhostStates()     #if ghost is scared hurry up, eat as much as possible
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    if (newScaredTimes[0]>0):
        if position in MultiAgentSearchAgent.food: #if node has food, get pacman to eat it
            score = score *100
        if position not in MultiAgentSearchAgent.food: #if node dont have food, move closer to food
            score = score/10

    return score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
