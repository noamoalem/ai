import numpy as np
import abc
import util
from game import Agent, Action
from operator import itemgetter
import math

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def get_action(self, game_state):
        """
        You do not need to change this method, but you're welcome to.

        get_action chooses among the best options according to the evaluation function.

        get_action takes a game_state and returns some Action.X for some X in the set {UP, DOWN, LEFT, RIGHT, STOP}
        """

        # Collect legal moves and successor states
        legal_moves = game_state.get_agent_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = np.random.choice(best_indices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (GameState.py) and returns a number, where higher numbers are better.

        """

        # Useful information you can extract from a GameState (game_state.py)

        successor_game_state = current_game_state.generate_successor(
            action=action)
        board = successor_game_state.board
        max_tile = successor_game_state.max_tile
        score = successor_game_state.score

        "* YOUR CODE HERE *"
        counter = 0
        for i in range(len(board) - 1):
            for j in range(len(board[i]) - 1):
                if board[i][j] > 0:
                    if board[i][j] == board[i + 1][j] or board[i][j] == \
                            board[i][j + 1]:
                        counter += 1
        return score + counter



def score_evaluation_function(current_game_state):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return current_game_state.score


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evaluation_function='scoreEvaluationFunction', depth=2):
        self.evaluation_function = util.lookup(evaluation_function, globals())
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class MinmaxAgent(MultiAgentSearchAgent):
    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means our agent, the opponent is agent_index=1

        Action.STOP:
            The stop direction, which is always legal

        game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action
        """
        """*** YOUR CODE HERE ***"""

        return self.min_max_helper(0, game_state, 0)[1]



    def min_max_helper(self, current_depth, state, player):
        successors = []
        if current_depth == self.depth:
            return self.evaluation_function(state), Action.STOP
        if player == 0:
            legal_actions = state.get_legal_actions(player)
            for action in legal_actions:
                successors.append((state.generate_successor(player, action), action))
            lst = [(self.min_max_helper(current_depth, successor[0], 1)[0],
                    successor[1]) for
                   successor in successors]
            lst = sorted(lst, key=itemgetter(0), reverse=True)
            if len(lst) == 0:
                return self.evaluation_function(state), Action.STOP
            return lst[0]
        else:
            legal_actions = state.get_legal_actions(1)
            for action in legal_actions:
                successors.append(
                    (state.generate_successor(1, action), action))
            lst = [(self.min_max_helper(current_depth + 1, successor[0], 0)[0],
                    successor[1]) for
                   successor in successors]
            lst = sorted(lst, key=itemgetter(0))
            if len(lst) == 0:
                return self.evaluation_function(state), Action.STOP
            return lst[0]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        return self.alpha_beta_helper(game_state, 0, -math.inf, math.inf, 0)[1]




    def alpha_beta_helper(self, state, depth, alpha, beta, player):
        successors = []

        if depth == self.depth or state._done:
            return self.evaluation_function(state), Action.STOP

        if player == 0:
            legal_actions = state.get_legal_actions(player)
            for action in legal_actions:
                successors.append((state.generate_successor(player, action),
                                   action))
            value = -math.inf, Action.STOP
            for child in successors:
                lst = sorted([value, (self.alpha_beta_helper(child[0], depth,
                alpha, beta, 1)[0],child[1])], key=itemgetter(0), reverse=True)
                value = lst[0]
                alpha = max(alpha, value[0])
                if beta <= alpha:
                    break

            return value
        else:
            legal_actions = state.get_legal_actions(player)
            for action in legal_actions:
                successors.append(
                    (state.generate_successor(player, action), action))
            value = math.inf, Action.STOP
            for child in successors:
                lst = sorted([value, (self.alpha_beta_helper(child[0], depth+1,
                        alpha, beta, 0)[0],child[1])], key=itemgetter(0))
                value = lst[0]
                beta = min(beta, value[0])
                if beta <= alpha:
                    break
            return value



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """
        """*** YOUR CODE HERE ***"""
        return self.expectimax_helper(0, game_state, 0)[1]


    def expectimax_helper(self, current_depth, state, player):
        successors = []
        if current_depth == self.depth or state._done:
            return self.evaluation_function(state), Action.STOP
        if player == 0:
            legal_actions = state.get_legal_actions(0)
            for action in legal_actions:
                successors.append((state.generate_successor(0, action), action))
            lst = [(self.expectimax_helper(current_depth, successor[0], 1)[0],
                    successor[1]) for successor in successors]
            # print(lst)
            lst = sorted(lst, key=itemgetter(0), reverse=True)
            return lst[0]
        else:
            legal_actions = state.get_legal_actions(1)
            for action in legal_actions:
                successors.append((state.generate_successor(1, action), action))
            lst = [(self.expectimax_helper(current_depth + 1, successor[0], 0)[0],
                 successor[1]) for successor in successors]
            sum_of_sons = sum(child[0] for child in lst)
            avg = sum_of_sons / len(lst)
            return avg, Action.STOP


def better_evaluation_function(current_game_state):
    """
    Your extreme 2048 evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    "" we took into account a number of variables such as distance from corner,
    max tile on board, number of possible connections and empty tiles and
    then we played with the combinations of these variables"""
    "* YOUR CODE HERE *"
    board = current_game_state.board
    max_tile = current_game_state.max_tile
    counter = 0
    empty_counter = 0
    distance = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == max_tile:
                distance = math.sqrt(i * i + j * j)
            if board[i][j] == 0:
                empty_counter += 1
            k = j + 1
            t = i + 1
            while (k < len(board) and (
                    board[i][j] == board[i][k] or board[i][k] == 0)):
                if board[i][j] == board[i][k] and board[i][j] != 0:
                    counter += 1
                    break
                k += 1
            while (t < len(board) and (
                    board[i][j] == board[t][j] or board[t][j] == 0)):
                if board[i][j] == board[t][j] and board[i][j] != 0:
                    counter += 1
                    break
                t += 1

    return 120 * counter + 128 * empty_counter + max_tile * 12 + 6 * distance

# Abbreviation
better = better_evaluation_function
