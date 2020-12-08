from board import *
from search import *
import util
from operator import itemgetter


class BlokusFillProblem(SearchProblem):
    """
    A one-player Blokus game as a search problem.
    This problem is implemented for you. You should NOT change it!
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        return not any(state.pieces[0])

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, 1) for move in
                state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################
class BlokusCornersProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board_w = board_w
        self.board_h = board_h
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        return not state.get_position(0, 0) and not state.get_position(
            0, self.board_h - 1) and not state.get_position \
            (self.board_w - 1, 0) and not state. \
            get_position(self.board_w - 1, self.board_h - 1)

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for
                move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """

        total_cost = 0
        for action in actions:
            total_cost += action.piece.get_num_tiles()
        return total_cost


def blokus_corners_heuristic(state, problem):
    """
    Your heuristic for the BlokusCornersProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
    """
    "*** YOUR CODE HERE ***"

    h = problem.board.board_h - 1
    w = problem.board.board_w - 1
    corners = [(0, 0), (0, h), (w, 0), (w, h)]
    free_corners = []
    for corner in corners:
        if state.get_position(corner[0], corner[1]) == -1:
            free_corners.append(corner)
    infinit_dist = problem.board.board_h * problem.board.board_w
    for corner in free_corners:
        if check_corner(h, w, corner) == "top_right":
            if state.get_position(corner[0] + 1, corner[1]) != -1 or\
                    state.get_position(corner[0], corner[1] - 1) != -1:
                return infinit_dist
        elif check_corner(h, w, corner) == "down_left":
            if state.get_position(corner[0] - 1, corner[1]) != -1 or \
                    state.get_position(corner[0], corner[1] + 1) != -1:
                return infinit_dist
        elif check_corner(h, w, corner) == "down_right":
            if state.get_position(corner[0], corner[1] - 1) != -1 or \
                    state.get_position(corner[0] - 1, corner[1]) != -1:
                return infinit_dist
        elif check_corner(h, w, corner) == "zero_point":
            if state.get_position(corner[0], corner[1] + 1) != -1 or \
                    state.get_position(corner[0] + 1, corner[1]) != -1:
                return infinit_dist
    return len(free_corners)


def lst_legal_moves(board_h, board_w, player, state):
    """
    This function finds all the legal moves on the board
    :param board_h: the board high
    :param board_w: the board width
    :param player: given player
    :param state: given state
    :return: list of all the legal moves
    """
    legal_moves = []
    for i in range(0, board_h):
        for j in range(0, board_w):
            if state.check_tile_legal(player, i,j) and \
                    state.check_tile_attached(player, i, j):
                if state.get_position(i, j) == -1:
                    legal_moves.append((i, j))
    return legal_moves


def sort_distance(legal_moves, target_point):
    """
    This function sort the distances from a given moves to the target in
    decreasing order
    :param legal_moves: all the legal moves to check distance from
    :param target_point: thr target point
    :return: sorted list of the distances from the legal moves to the target
             the list contain tupels of (distance, move)
    """
    sorted_lst = []
    for move in legal_moves:
        sorted_lst.append((util.manhattanDistance(move, target_point), move))
    sorted_lst = sorted(sorted_lst, key=itemgetter(0))
    return sorted_lst


def check_corner(h, w, corner):
    if corner[0] == 0 and corner[1] == h:
        return "top_right"
    if corner[0] == w and corner[1] == 0:
        return "down_left"
    if corner[0] == w and corner[1] == h:
        return "down_right"
    if corner[0] == 0 and corner[1] == 0:
        return "zero_point"

def check_target(h, w, target):
    if target[0] > 0:
        return "left"
    if target[0] < w-1:
        return "right"
    if target[1] > 0:
        return "down"
    if target[1] < h-1:
        return "up"
    return "cant_move"


class BlokusCoverProblem(SearchProblem):

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0),
                 targets=[(0, 0)]):
        self.targets = targets.copy()
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        "*** YOUR CODE HERE ***"

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        for target in self.targets:
            if not state.get_position(target[1], target[0]):
                continue
            else:
                return False
        return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for
                move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        "*** YOUR CODE HERE ***"
        total_cost = 0
        for action in actions:
            total_cost += action.piece.get_num_tiles()
        return total_cost


def blokus_cover_heuristic(state, problem):
    """
    :param state: given state.
    :param problem: given search problem.
    :return: the estimated cost from the given state to thr goal.
    """
    "*** YOUR CODE HERE ***"

    h = problem.board.board_h - 1
    w = problem.board.board_w - 1
    targets = problem.targets
    free_targets = []

    for target in targets:
        if state.get_position(target[1], target[0]) == -1:
            free_targets.append(target)
    infinit_dist = problem.board.board_h * problem.board.board_w

    for target in free_targets:
        if check_corner(h, w, target) == "top_right":
            if state.get_position(target[0] + 1, target[1]) != -1 or \
                    state.get_position(target[0], target[1] - 1) != -1:
                return infinit_dist
        if check_corner(h, w, target) == "down_left":
            if state.get_position(target[0] - 1, target[1]) != -1 or \
                    state.get_position(target[0], target[1] + 1) != -1:
                return infinit_dist
        if check_corner(h, w, target) == "down_right":
            if state.get_position(target[0], target[1] - 1) != -1 or \
                    state.get_position(target[0] - 1, target[1]) != -1:
                return infinit_dist
        if check_corner(h, w, target) == "zero_point":
            if state.get_position(target[0], target[1] + 1) != -1 or \
                    state.get_position(target[0] + 1, target[1]) != -1:
                return infinit_dist
        if target[0] > 0:
            if state.get_position(target[1], target[0]-1) != -1:
                return infinit_dist
        if target[0] < h:
            if state.get_position(target[1], target[0]+1) != -1:
                return infinit_dist
        if target[1] < w:
            if state.get_position(target[1] + 1, target[0]) != -1:
                return infinit_dist
        if target[1] > 0:
            if state.get_position(target[1] - 1, target[0]) != -1:
                return infinit_dist
    length_free_targets = len(free_targets)

    return length_free_targets



class ClosestLocationSearch:
    """
    In this problem you have to cover all given positions on the board,
    but the objective is speed, not optimality.
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0),
                 targets=(0, 0)):
        self.expanded = 0
        self.targets = targets.copy()
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.starting_point = starting_point

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        if state.get_position(self.targets[0][1], self.targets[0][0]) != -1:
            return True
        return False
        # for target in self.targets:
        #    if state.get_position(target[1], target[0]) == -1:
        #        return False
        #    else:
        #        self.targets.remove(target)
        # return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for
                move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        total_cost = 0
        for action in actions:
            total_cost += action.piece.get_num_tiles()
        return total_cost

    def solve(self):
        """
        This method should return a sequence of actions that covers all target locations on the board.
        This time we trade optimality for speed.
        Therefore, your agent should try and cover one target location at a time. Each time, aiming for the closest uncovered location.
        You may define helpful functions as you wish.

        Probably a good way to start, would be something like this --

        current_state = self.board._copy_()
        backtrace = []

        while ....

            actions = set of actions that covers the closets uncovered target location
            add actions to backtrace

        return backtrace
        """

        current_state = self.board.__copy__()
        actions_to_goal = []
        # get closest targets by order
        sorted_start_to_goal = sort_distance(self.targets, self.starting_point)
        temp = []
        for i in sorted_start_to_goal:
            temp.append(i[1])
        self.targets = temp
        action_to_goal = a_star(self, blokus_cover_heuristic)
        actions_to_goal += action_to_goal
        for i in range(len(action_to_goal)):
            self.board = self.board.do_move(0, action_to_goal[i])
        self.targets = self.targets[1:]
        while len(self.targets) > 0:
            current_legal_moves = lst_legal_moves(current_state.board_h,
                                        current_state.board_w, 0, self.board)
            sorted_distances = sort_distance2(current_legal_moves,self.targets)
            self.starting_point = sorted_distances[0][1]
            target = sorted_distances[0][2]
            index = self.targets.index(target)  # swipe targets place
            self.targets[index] = self.targets[0]
            self.targets[0] = target

            action_to_goal = a_star(self, blokus_cover_heuristic)
            actions_to_goal += action_to_goal
            for i in range(len(action_to_goal)):
                self.board = self.board.do_move(0, action_to_goal[i])
            if len(self.targets) > 1:
                self.targets = self.targets[1:]
            else:
                self.targets = []
        self.board = current_state
        return actions_to_goal


        # current_state = self.board.__copy__()
        # actions_to_goal = []
        # # get closest targets by order
        # sorted_start_to_goal = sort_distance(self.targets, self.starting_point)
        # temp = []
        # for i in sorted_start_to_goal:
        #     temp.append(i[1])
        # self.targets = temp
        # queue = util.PriorityQueue()
        # visited = set()
        # wrapper = Wrapper((current_state, []))
        # queue.push(wrapper,0)
        # while queue:
        #     while self.targets:
        #         temp = queue.pop()
        #         current_state = temp.state
        #         temp_action = temp.lst_of_action
        #         print(current_state)
        #         if self.is_goal_state(current_state):
        #             return temp_action
        #             # if len(self.targets) > 1:
        #             #     self.targets = self.targets[1:]
        #             # else:
        #             #     self.targets = []
        #             #     break
        #         if current_state in visited:
        #             continue
        #         else:
        #             visited.add(current_state)
        #             sorted_distances = sort_distance4(self.get_successors(current_state), self.targets)
        #             #sorted_distances = sort_distance2(lst_legal_moves(self.board.board_h,self.board.board_w,0,current_state), self.targets)
        #             if len(sorted_distances) > 0:
        #                 for i in reversed(sorted_distances):
        #                     wrapper = Wrapper((i[3], temp_action + [i[1]]))
        #                     queue.push(wrapper, i[0]+i[4])
        #                 target = sorted_distances[0][2]
        #                 index = self.targets.index(target)  # swipe targets place
        #                 self.targets[index] = self.targets[0]
        #                 self.targets[0] = target
        #
        #     return actions_to_goal


def a_star(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    we use this a* for the closest point problem.
    """
    "*** YOUR CODE HERE ***"
    visited = set()
    state_to_action_list = dict()
    queue = util.PriorityQueue()
    current_state = problem.get_start_state()
    queue.push(current_state, 1)
    visited.add(current_state)
    state_to_action_list[current_state] = []
    while queue:
        current_state = queue.pop()
        lst_action_to_goal = state_to_action_list[current_state]
        if problem.is_goal_state(current_state):
            return lst_action_to_goal
        for neighbor in problem.get_successors(current_state):
            if neighbor[0] not in visited:
                if problem.is_goal_state(neighbor[0]):
                    return lst_action_to_goal + [neighbor[1]]
                sum_cost = problem.get_cost_of_actions(
                    lst_action_to_goal + [neighbor[1]]) + \
                           heuristic(neighbor[0], problem)
                visited.add(neighbor[0])
                queue.push(neighbor[0], sum_cost)
                state_to_action_list[neighbor[0]] = lst_action_to_goal + [
                    neighbor[1]]


def sort_distance2(legal_moves, target_to_check):
    """
    This function sort the distances from a given moves to the given targets in
    decreasing order.
    :param legal_moves: list of all the legal moves to check distance from.
    :param target_to_check: list of all the targets to check distance from.
    :return: sorted list of the distances from the legal moves to the target
        the list contain tupels (distance, move, closest target to this move).
    """
    sorted_lst = []
    for move in legal_moves:
        temp = []
        for target in target_to_check:
            temp.append((util.manhattanDistance(move, target), move, target))
        temp = sorted(temp, key=itemgetter(0))

        sorted_lst.append(temp[0])
        # temp[0] is tuple (distance, move,closest target to this move)
    sorted_lst = sorted(sorted_lst, key=itemgetter(0))
    return sorted_lst

def sort_distance3(legal_moves, target_point):
    """
    This function sort the distances from a given moves to the given targets in
    decreasing order.
    :param legal_moves: list of all the legal moves to check distance from.
    :param target_to_check: list of all the targets to check distance from.
    :return: sorted list of the distances from the legal moves to the target
        the list contain tupels (distance, move, closest target to this move).
    """
    sorted_lst = []
    for move in legal_moves:
        sorted_lst.append((max(abs(move[0] - target_point[0]),
                               abs(move[1] - target_point[1]))))
    if len(sorted_lst) > 0:
        return min(sorted_lst)
    return 0


def sort_distance4(get_succesor, target_to_check):
    """
    This function sort the distances from a given moves to the given targets in
    decreasing order.
    :param get_succesor: list of all the legal moves to check distance from.
    :param target_to_check: list of all the targets to check distance from.
    :return: sorted list of the distances from the legal moves to the target
        the list contain tupels (distance, move, closest target to this move, state).
    """
    sorted_lst = []
    for move in get_succesor:
        temp = []
        for target in target_to_check:
            temp.append((util.manhattanDistance((move[1].x,move[1].y), target), move[1], target, move[0], move[2]))
        temp = sorted(temp, key=itemgetter(0))

        sorted_lst.append(temp[0])
        # temp[0] is tuple (distance, move,closest target to this move, state)
    sorted_lst = sorted(sorted_lst, key=itemgetter(0))
    return sorted_lst

class Wrapper:
    def __init__(self, inside):
        self.state = inside[0]
        self.lst_of_action = inside[1]


class MiniContestSearch:
    """
    Implement your contest entry here
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0),
                 targets=(0, 0)):
        self.targets = targets.copy()
        "*** YOUR CODE HERE ***"

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def solve(self):
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
