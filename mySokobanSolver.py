
'''

    2020 CAB320 Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.
No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.


You are NOT allowed to change the defined interfaces.
That is, changing the formal parameters of a function will break the 
interface and results in a fail for the test of your code.
This is not negotiable! 


'''

# You have to make sure that your code works with
# the files provided (search.py and sokoban.py) as your code will be tested
# with these files
import search
import sokoban

# External library
import math
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)

    '''
    return [(10107321, 'Ho Fong', 'Law'), (10031014, 'Kiki', 'Mutiara')]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A cell inside a warehouse is 
    called 'taboo'  if whenever a box get pushed on such a cell then the puzzle 
    becomes unsolvable. Cells outside the warehouse should not be tagged as taboo.
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.

    @param warehouse: 
        a Warehouse object with a worker inside the warehouse

    @return
       A string representing the puzzle with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    X, Y = zip(*warehouse.walls)
    x_size, y_size = 1+max(X), 1+max(Y)
    
    
    x_sym_list = []
    x_sym = []
    targets = []
    left_walls = right_walls = up_walls =  down_walls = []
    str_puzzle = [[" "] * x_size for y in range(y_size)]

    first_row = 0
    first_col = 0
   
    for (x, y) in warehouse.walls:
        str_puzzle[y][x] = "#"

# find which side is the wall 
    for y in range(warehouse.nrows):
        first_col = True
        for x in range(warehouse.ncols):
            if (x, y) in warehouse.walls and first_col:
                first_col = False
                left_walls.append([x, y])
            if x == warehouse.ncols - 1:
                temp_col = x
                while True:
                    if (temp_col, y) in warehouse.walls:
                        break
                    temp_col = temp_col - 1
                right_walls.append([temp_col, y])

    for x in range(warehouse.ncols):
        first_row = True
        for y in range(warehouse.nrows):
            if (x, y) in warehouse.walls and first_row:
                first_row = False
                up_walls.append([x, y])
            if y == warehouse.nrows - 1:
                temp_row = y
                while True:
                    if (x, temp_row) in warehouse.walls:
                        break
                    temp_row = temp_row - 1
                down_walls.append([x, temp_row])

# Base on first rule  ,If two wall appear, coner will be set and taboo also
    for y in range(warehouse.nrows):
        for x in range(warehouse.ncols):
            if not (x, y) in warehouse.walls:
                if (x, y) in warehouse.targets:
                    targets.append((x, y))
                    continue
                for x_direction in (LEFT,RIGHT):
                    if x_direction.move_to((x,y)) in warehouse.walls and (x, y) not in warehouse.walls:
                        if (x, y-1) in warehouse.walls:
                            x_sym.append((x, y))
                            continue
                        if (x, y+1) in warehouse.walls:
                            x_sym.append((x, y))
                            continue
                for y_direction in (UP,DOWN):
                    if y_direction.move_to((x,y)) in warehouse.walls and (x, y) not in warehouse.walls:
                        if (x-1, y) in warehouse.walls:
                            x_sym.append((x, y))
                            continue
                        if (x+1, y) in warehouse.walls:
                            x_sym.append((x, y))
                            continue
                
    
# Creat a filter to determent outside or inside the wall
    for (col, row) in set(x_sym):
        for (left_col, left_row) in left_walls:
            if col > left_col and left_row == row:
                for(right_col, right_row) in right_walls:
                    if col < right_col and right_row == row:
                        for (top_col, top_row) in up_walls:
                            if row > top_row and top_col == col:
                                for (bottom_col, bottom_row) in down_walls:
                                    if row < bottom_row and bottom_col == col:
                                        x_sym_list.append((col, row))
# Base on second rule  ,add another taboo cell beside the wall
    taboo_list = list(set(x_sym_list))
    temp_taboo_list = []
    for (x, y) in list(set(x_sym_list)):
        stack = 1
        while (x+stack, y) not in warehouse.walls:
            # print(x+stack, y)
            if (x+stack, y+1) not in warehouse.walls and (x+stack, y-1) not in warehouse.walls:
                stack = 0
                temp_taboo_list = []
                break
            if (x+stack, y) in warehouse.targets:
                stack = 0
                temp_taboo_list = []
                break
            if (x+stack, y) in taboo_list:
                for temp in temp_taboo_list:
                    taboo_list.append(temp)
                stack = 0
                break
            temp_taboo_list.append((x+stack, y))
            stack = stack+1
        stack = 1
        while (x, y+stack) not in warehouse.walls:
            # print(x, y+stack)
            if (x+1, y+stack) not in warehouse.walls and (x-1, y+stack) not in warehouse.walls:
                stack = 0
                temp_taboo_list = []
            if (x, y+stack) in warehouse.targets and (x, y+stack) not in x_sym_list:
                stack = 0
                temp_taboo_list = []
            if (x, y+stack) in taboo_list:
                for temp in temp_taboo_list:
                    taboo_list.append(temp)
                stack = 0
            if stack == 0:
                break
            temp_taboo_list.append((x, y+stack))
            stack = stack+1
# Input taboo cell 
    for (x, y) in taboo_list:
        str_puzzle[y][x] = "X"
    return "\n".join(["".join(line) for line in str_puzzle])

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_reader(taboo_cells_str):
    #reference from from_lines
    lines = taboo_cells_str.split(sep='\n')
    first_row, first_col = None, None
    for row, line in enumerate(lines):
        brick_column = line.find('#')
        if brick_column >= 0:
            if first_row is None:
                first_row = row  
            if first_col is None:
                first_col = brick_column
            else:
                first_col = min(first_col, brick_column)
    if first_col is None:
        raise ValueError('Warehouse with no walls!')
    canonical_lines = [line[first_col:]
                       for line in lines[first_row:] if line.find('#') >= 0]
    return list(sokoban.find_2D_iterator(canonical_lines, "X"))


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 

    Each SokobanPuzzle instance should have at least the following attributes
    - self.allow_taboo_push
    - self.macro

    When self.allow_taboo_push is set to True, the 'actions' function should 
    return all possible legal moves including those that move a box on a taboo 
    cell. If self.allow_taboo_push is set to False, those moves should not be
    included in the returned list of actions.

    If self.macro is set True, the 'actions' function should return 
    macro actions. If self.macro is set False, the 'actions' function should 
    return elementary actions.        
    '''

    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to
    #     complete this class. For example, a 'result' function is needed
    #     to satisfy the interface of 'search.Problem'.

    def __init__(self, initial=None, allow_taboo_push=True, macro=False,
                 push_costs=None):
        # print('This is the initial state:\n' + self.initial)
        self.allow_taboo_push = allow_taboo_push
        self.macro = macro
        self.initial = initial.__str__()
        self.temp_sokoban = initial
        self.push_costs = push_costs
        self.goal = initial.copy(boxes=initial.targets).__str__()
        self.ListofLocation = initial.boxes
        
  
    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.

        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        self.temp_sokoban.extract_locations(state.split(sep="\n"))
        action_list = []
        taboo_cell = taboo_reader(taboo_cells( self.temp_sokoban))
        for direction in (UP, RIGHT, DOWN, LEFT):
            if self.macro:
                for box in  self.temp_sokoban.boxes:
                    newLoc = direction.move_to(box)
                    workerLoc = (box[1] - 1 * direction.heap[1], box[0] 
                                 - 1 * direction.heap[0])
                    if can_go_there( self.temp_sokoban, workerLoc) and newLoc not in  self.temp_sokoban.walls and newLoc not in  self.temp_sokoban.boxes:
                            if self.allow_taboo_push:
                                action_list.append((box, direction))
                            else:
                                if newLoc not in taboo_reader(taboo_cells
                                                                  ( self.temp_sokoban)):
                                    action_list.append((box, direction))
            else:
                loc_one = loc_two =  self.temp_sokoban.worker
                loc_one = direction.move_to(loc_one)
                loc_two = direction.move_to(loc_one)
                if loc_one in  self.temp_sokoban.boxes and loc_two not in  self.temp_sokoban.boxes and loc_two not in  self.temp_sokoban.walls:
                        if self.allow_taboo_push:
                            action_list.append(direction)
                        else:      
                            if loc_two not in taboo_cell:
                                action_list.append(direction)
                if loc_one not in  self.temp_sokoban.boxes and loc_one not in  self.temp_sokoban.walls:
                    action_list.append(direction)
        return action_list

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        # new_wh = sokoban.Warehouse()
        self.temp_sokoban.extract_locations(state.split(sep="\n"))
        if self.macro:
            location = action[0]
            if location in self.temp_sokoban.boxes:
                self.temp_sokoban.boxes.remove(location)
                self.temp_sokoban.worker = location
                new_location = action[1].move_to(location)
                self.temp_sokoban.boxes.append(new_location)
        else:
            loc_one = self.temp_sokoban.worker
            loc_two = self.temp_sokoban.worker
            loc_one = action.move_to(loc_one)
            loc_two = action.move_to(loc_one)
            if loc_one in self.temp_sokoban.boxes:
                if loc_two not in self.temp_sokoban.boxes and loc_two not in self.temp_sokoban.walls:
                    self.temp_sokoban.boxes.remove(loc_one)
                    self.temp_sokoban.boxes.append(loc_two)
            self.temp_sokoban.worker = loc_one
        return self.temp_sokoban.__str__()

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        new_wh1 = sokoban.Warehouse()
        new_wh1.extract_locations(state.split(sep="\n"))
        new_wh2 = sokoban.Warehouse()
        new_wh2.extract_locations(self.goal.split(sep="\n"))
        return set(new_wh1.boxes) == set(new_wh2.targets)

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        new_wh2 = sokoban.Warehouse()
        new_wh2.extract_locations(state2.split(sep="\n"))
        if self.push_costs == None:
            return c + 1
        else:
            for i in range(len(self.ListofLocation)):
                if self.ListofLocation[i] not in new_wh2.boxes:
                    push_cost = self.push_costs[i]
                    for box in new_wh2.boxes:
                        if box not in self.ListofLocation:
                            self.ListofLocation[i] = box
                            return c + push_cost
            return c + 1

    def h(self, n):
        heur = 0
        new_wh = sokoban.Warehouse()
        new_wh.extract_locations(n.state.split(sep="\n"))
        for box in new_wh.boxes:
            temp_target = new_wh.targets[0]
            for target in new_wh.targets:
                if(manhattan_distance(target, box) < manhattan_distance(temp_target, box)):
                    temp_target = target
            heur = heur + manhattan_distance(temp_target, box)

        return heur

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



def check_elem_action_seq(warehouse, action_seq):
    '''

    Determine if the sequence of actions listed in 'action_seq' is legal or not.

    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.

    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']

    @return
        The string 'Impossible', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    # print(warehouse)
    loc_one = loc_two = warehouse.worker
    for step in action_seq:
        if step == 'Left':
            way = LEFT
        if step == 'Up':
            way = UP
        if step == 'Right':
            way = RIGHT
        if step == 'Down':
            way = DOWN
        loc_one = way.move_to(loc_one)
        loc_two = way.move_to(loc_one)
        # print(loc_two)
        if loc_one in warehouse.walls:
            return 'Impossible'
        if loc_one in warehouse.boxes:
            if loc_two in warehouse.boxes or loc_two in warehouse.walls:
                print('b')
                return 'Impossible'
            warehouse.boxes.remove(loc_one)
            warehouse.boxes.append(loc_two)
        warehouse.worker = loc_one
    return warehouse.__str__()


def solve_sokoban_elem(warehouse):
    '''    
    This function should solve using A* algorithm and elementary actions
    the puzzle defined in the parameter 'warehouse'.

    In this scenario, the cost of all (elementary) actions is one unit.

    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    puzzle = SokobanPuzzle(warehouse, True, False)
    temp_warehouse = warehouse.copy()
    if (set(temp_warehouse.boxes) == set(temp_warehouse.targets)):
        return []
    puzzle_ans = search.astar_graph_search(puzzle)
    step_move = []
    if (puzzle_ans is None):
        return 'Impossible'
    else:
        for node in puzzle_ans.path():
            step_move.append(node.action.__str__())
        action_seq = step_move[1:]
        if check_elem_action_seq(temp_warehouse, action_seq) == 'Impossible':
            return 'Impossible'
        else:
            return action_seq


def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.

    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''
    destination = (dst[1], dst[0])
    path = search.astar_graph_search(
        TempSokuban(warehouse.worker, destination, warehouse))
    if path is None:
        return False
    else:
        return True


def solve_sokoban_macro(warehouse):
    '''    
    Solve using using A* algorithm and macro actions the puzzle defined in 
    the parameter 'warehouse'. 

    A sequence of macro actions should be 
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ] 
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes to the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.

    In this scenario, the cost of all (macro) actions is one unit. 

    @param warehouse: a valid Warehouse object

    @return
        If the puzzle cannot be solved return the string 'Impossible'
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''

    puzzle = SokobanPuzzle(warehouse, True, True)
    temp_warehouse = warehouse.copy()
    if (temp_warehouse.boxes == temp_warehouse.targets):
        return []
    puzzle_ans = search.astar_graph_search(puzzle)
    step_move = []
    if (puzzle_ans is None):
        return 'Impossible'
    else:
        for node in puzzle_ans.path():
            action = node.action
            if action is None:
                continue
            step_move.append(
                ((action[0][1], action[0][0]), action[1].__str__()))
        action_seq = step_move[:]
        return action_seq


def solve_weighted_sokoban_elem(warehouse, push_costs):
    '''
    In this scenario, we assign a pushing cost to each box, whereas for the
    functions 'solve_sokoban_elem' and 'solve_sokoban_macro', we were 
    simply counting the number of actions (either elementary or macro) executed.

    When the worker is moving without pushing a box, we incur a
    cost of one unit per step. Pushing the ith box to an adjacent cell 
    now costs 'push_costs[i]'.

    The ith box is initially at position 'warehouse.boxes[i]'.

    This function should solve using A* algorithm and elementary actions
    the puzzle 'warehouse' while minimizing the total cost described above.

    @param 
     warehouse: a valid Warehouse object
     push_costs: list of the weights of the boxes (pushing cost)

    @return
        If puzzle cannot be solved return 'Impossible'
        If a solution exists, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    
    puzzle = SokobanPuzzle(warehouse, True, False, push_costs)

    temp_warehouse = warehouse.copy()
    if (temp_warehouse.boxes == temp_warehouse.targets):
        return []
    puzzle_ans = search.astar_graph_search(puzzle)
    # print(warehouse)
    step_move = []
    if (puzzle_ans is None):
        return 'Impossible'
    else:
        for node in puzzle_ans.path():
            step_move.append(node.action.__str__())
        action_seq = step_move[1:]
    
        if check_elem_action_seq(temp_warehouse, action_seq) == 'Impossible':
            return 'Impossible'
        else:
            return action_seq


#------------------other functions-------------------
class Pointer:

    def __init__(self, pointer_name, heap):

        self.pointer_name = pointer_name
        self.heap = heap
        
    def move_to(self, position):

        return (position[0] + self.heap[0], position[1] + self.heap[1])

    def heap(self):

        return self.heap

    def __str__(self):

        return str(self.pointer_name)


UP = Pointer("Up", (0, -1))
RIGHT = Pointer("Right", (1, 0))
DOWN = Pointer("Down", (0, 1))
LEFT = Pointer("Left", (-1, 0))


class TempSokuban(search.Problem):

    def __init__(self, initial, goal, warehouse):
        self.initial = initial
        self.goal = goal
        self.warehouse = warehouse

    def actions(self, state):
        listOfActions = []
        for direct in (UP, RIGHT, DOWN, LEFT):
            nextStep = direct.move_to(state)
            if nextStep not in self.warehouse.walls and nextStep not in self.warehouse.boxes:
                listOfActions.append(direct)
        return listOfActions

    def result(self, state, step):
        position = state
        position = step.move_to(position)
        return position

    def h(self, n):
        state = n.state
        curGoal = self.goal
        return math.sqrt((state[0]-curGoal[0])**2+(state[1]-curGoal[1])**2)


def manhattan_distance (loca_a, loca_b):
    # return xy distance between two points
    return abs((loca_a[0] - loca_b[0])) + abs((loca_a[1] - loca_b[1]))
