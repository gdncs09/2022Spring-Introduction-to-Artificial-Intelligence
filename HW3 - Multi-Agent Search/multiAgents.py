from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

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
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


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


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (Part 1)
    """
    
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)   
        best_score = float('-inf') #init
        best_action = None #will be save the result
        pacman_legal_actions = gameState.getLegalActions(0) #list of legal acions for an pacman
        for action in pacman_legal_actions: #get the max value of from all actions next states
            score = self.min_value(gameState.getNextState(0, action), 1, 0) 
            if score > best_score: #find the max value of all actions, save the action of best value
                best_score = score
                best_action = action #update
        return best_action #final action
    
    def max_value(self, gameState, agentIndex, depth): #max player pacman
        actions = gameState.getLegalActions(agentIndex) #list of legal acions for an pacman
        if depth == self.depth or len(actions) == 0 or gameState.isWin() or gameState.isLose(): 
            return self.evaluationFunction(gameState)
        
        return max([self.min_value(gameState.getNextState(agentIndex, action), 1, depth) for action in actions])
    
    def min_value(self, gameState, agentIndex, depth): #min players or agents
        actions = gameState.getLegalActions(agentIndex) #list of legal acions for an agent
        if len(actions) == 0 or gameState.isWin() or gameState.isLose(): 
            return self.evaluationFunction(gameState)
        
        if (agentIndex < gameState.getNumAgents()-1): #do not last ghost
            return min([self.min_value(gameState.getNextState(agentIndex, action), agentIndex+1, depth) for action in actions])
        else: #last ghost             
            return min([self.max_value(gameState.getNextState(agentIndex, action), 0, depth+1) for action in actions]) #pacman
        
        #use recursion to find value of action
        #compare to find the max value of all actions and return action of best value
        #depth "d" search will involve pacman and all ghosts taking d steps
        #python autograder.py -q part1 --no-graphics
        #raise NotImplementedError("To be implemented")
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        alpha = float('-inf') #max best option
        beta = float('inf') #min best option
        
        best_action = None
        pacman_legal_actions = gameState.getLegalActions(0) #list of legal acions for an pacman
        for action in pacman_legal_actions:
            score = self.min_value(gameState.getNextState(0, action), 1, 0, alpha, beta)    
            if score > alpha: #find the max value of all actions, save the action of best value
                alpha = score
                best_action = action
        return best_action #final action
    
    def max_value(self, gameState, agentIndex, depth, alpha, beta): #max agents best move
        actions = gameState.getLegalActions(agentIndex)
        if depth == self.depth or len(actions)==0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        score = float('-inf') 
        for action in actions:
            score = max(score, self.min_value(gameState.getNextState(agentIndex, action), 1, depth, alpha, beta))
            if score > beta:
                return score
            alpha = max(alpha, score)        
        return score            
    
    def min_value(self, gameState, agentIndex, depth, alpha, beta): #min agents best move
        actions = gameState.getLegalActions(agentIndex) #list of legal acions for an agent
        if len(actions) == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
       
        score = float('inf')
        for action in actions: 
            if agentIndex < gameState.getNumAgents()-1: #do not last ghost
                score = min(score, self.min_value(gameState.getNextState(agentIndex, action), agentIndex+1, depth, alpha, beta))
            else: #last ghost
                score = min(score, self.max_value(gameState.getNextState(agentIndex, action), 0, depth+1, alpha, beta))
            if score < alpha: 
                return score   
            beta = min(beta, score)
        return score
        #use recursion to find value of action
        #depth "d" search will involve pacman and all ghosts taking d steps
        #python autograder.py -q part2 --no-graphics
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        best_score = float('-inf')
        best_action = None
        pacman_legal_actions = gameState.getLegalActions(0) #list of legal acions for an pacman
        for action in pacman_legal_actions:
            score = self.min_value(gameState.getNextState(0, action), 1, 0)
            if score > best_score: #find max score to get action result
                best_score = score
                best_action = action
        return best_action #final action
    
    def max_value(self, gameState, agentIndex, depth): #max player pacman
        if (depth == self.depth) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        actions = gameState.getLegalActions(agentIndex) #list of legal acions for an pacman
        return max([self.min_value(gameState.getNextState(agentIndex, action), 1, depth) for action in actions]) 
    
    def min_value(self, gameState, agentIndex, depth): #min players or agents
        actions = gameState.getLegalActions(agentIndex)
        num_actions = len(actions)
        if num_actions == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        if agentIndex < gameState.getNumAgents()-1: #do not last ghost
            total = sum([self.min_value(gameState.getNextState(agentIndex, action), agentIndex+1, depth) for action in actions])
            return total/float(num_actions)
        else: #last ghost
            total = sum([self.max_value(gameState.getNextState(agentIndex, action), 0, depth+1) for action in actions])
            return total/float(num_actions)
        #use recursion to find value of action
        #depth "d" search will involve pacman and all ghosts taking d steps
        #python autograder.py -q part3 --no-graphics
        #raise NotImplementedError("To be implemented")
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)   
    pacman_position = currentGameState.getPacmanPosition() #pacman position
    state_score = 200*currentGameState.getScore() #score of game
    
    #distances from ghosts to pacman
    ghost_states = currentGameState.getGhostStates()
    if currentGameState.getNumAgents() > 1: #if ghost exist
        ghost_distance = min([manhattanDistance(pacman_position, ghost.getPosition()) for ghost in ghost_states]) #calculate ghost distance 
        if ghost_distance < 2: #too close distance
            return float('-inf')
        state_score -= 1.0/ghost_distance #update score
            
    #foods positions
    foods = (currentGameState.getFood()).asList() #list of foods positions
    num_foods = len(foods) #quantity of food
    
    current_food = pacman_position #set current postion is pacman position
    for food in foods:
        closest_food = min(foods, key=lambda x: manhattanDistance(x, current_food)) #find closest food from current postion
        food_distance = manhattanDistance(current_food, closest_food) #calculate food distance
        state_score += 1.0/food_distance #update score
        current_food = closest_food #update current position
        foods.remove(closest_food) #remove
    
    #capsules postions     
    capsules = currentGameState.getCapsules() #list of foods positions
    num_capsules = len(capsules)
    
    current_capsule = pacman_position #set current postion is pacman position
    for capsule in capsules:
        closest_capsule = min(capsules, key=lambda x: manhattanDistance(x, current_capsule)) #find closest pellet from current postion
        capsule_distance = manhattanDistance(current_capsule, closest_capsule) #calculate pellet distance
        state_score += 1.0/capsule_distance #update score
        current_capsule = closest_capsule #update current position
        capsules.remove(closest_capsule) #remove
    
    state_score -= 10*num_foods + 50*num_capsules #remaining food and capsule
    return state_score
    #set game score 200, food 10, pellet 50
    #calculate min distance of food from pacman position and add inverse of it to state score and above same for capsules
    #if min ghost distance is 1 or less then return infinity value as state score, other subtract it's inverse from state score
    #python autograder.py -q part4 --no-graphics
    #raise NotImplementedError("To be implemented")
    # End your code (Part 4)
    
# Abbreviation
better = betterEvaluationFunction