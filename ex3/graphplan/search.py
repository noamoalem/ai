"""
In search.py, you will implement generic search algorithms
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

	print("Start:", problem.get_start_state().state)
    print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
    print("Start's successors:", problem.get_successors(problem.get_start_state()))
    """
    "*** YOUR CODE HERE ***"
    state_set = set()
    list_of_actions = list()
    state, start_state = problem.get_start_state(), problem.get_start_state()
    list_of_actions = explore(problem, state, start_state, state_set,
                              list_of_actions)
    return list_of_actions


def explore(problem, state, start_state, state_set, list_of_actions):
    """
    helper to the dfs algorithm.
    :param problem: search problem
    :param state: the current state
    :param start_state: the start state
    :param state_set: the state that the algorithm already done
    :param list_of_actions: action that already done
    :return: list of action to the goal state
    """
    state_set.add(state)
    lst = []
    for neighbor in reversed(problem.get_successors(start_state)):
        state = neighbor[0]
        action = neighbor[1]
        if problem.is_goal_state(state):
            list_of_actions.append(action)
            return list_of_actions
        if state not in state_set:
            state_set.add(state)
            list_of_actions.append(action)
            lst = explore(problem, state, state, state_set, list_of_actions)
            if len(lst) > 0:
                break
            list_of_actions.pop()
    return lst


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    visited = set()
    action_to_goal = util.Queue()
    queue = util.Queue()
    queue.push(problem.get_start_state())
    action_to_goal.push([])
    visited.add(problem.get_start_state())

    while queue:
        current_state = queue.pop()

        lst_action_to_goal = action_to_goal.pop()

        if problem.is_goal_state(current_state):
            return lst_action_to_goal

        for neighbor in problem.get_successors(current_state):
            if neighbor[0] not in visited:
                queue.push(neighbor[0])
                action_to_goal.push(lst_action_to_goal + [neighbor[1]])
                visited.add(neighbor[0])


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    "*** YOUR CODE HERE ***"
    visited = set()
    queue = util.PriorityQueue()
    current_state = problem.get_start_state()
    wrapper = Wrapper((current_state, []))
    queue.push(wrapper, 0)
    visited.add(current_state)

    while queue:
        temp = queue.pop()
        current_state = temp.state
        lst_action_to_goal = temp.lst_of_action
        if problem.is_goal_state(current_state):
            return lst_action_to_goal

        for neighbor in problem.get_successors(current_state):
            if neighbor[0] not in visited:
                sum_cost = problem.get_cost_of_actions(lst_action_to_goal + [
                    neighbor[1]])
                visited.add(neighbor[0])
                wrapper = Wrapper((neighbor[0], lst_action_to_goal+[neighbor[1]]))
                queue.push(wrapper, sum_cost)



def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    "*** YOUR CODE HERE ***"

    visited = set()
    queue = util.PriorityQueue()
    current_state = problem.get_start_state()
    wrapper = Wrapper((current_state, []))
    queue.push(wrapper, 0)
    visited.add(current_state)
    while queue:
        temp = queue.pop()
        current_state = temp.state
        lst_action_to_goal = temp.lst_of_action
        if problem.is_goal_state(current_state):
            return lst_action_to_goal
        for neighbor in problem.get_successors(current_state):
            if neighbor[0] not in visited:
                sum_cost = problem.get_cost_of_actions(lst_action_to_goal +
                            [neighbor[1]]) + heuristic(neighbor[0], problem)
                # print(current_state)
                # print(neighbor[0])
                # print(heuristic(neighbor[0], problem))
                visited.add(neighbor[0])
                wrapper = Wrapper((neighbor[0], lst_action_to_goal+[neighbor[1]]))
                queue.push(wrapper, sum_cost)


class Wrapper:
    def __init__(self, inside):
        self.state = inside[0]
        self.lst_of_action = inside[1]


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
