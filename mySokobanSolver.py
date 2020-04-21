
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
import random, time
import direction

#External library
import math
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (10107321, 'Ho Fong', 'Law'), (1234568, 'Kiki', 'Mutiara'), (1234569, 'Vincentius', 'Herdian Sungkono') ]

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
    X,Y = zip(*warehouse.walls) # pythonic version of the above
    x_size, y_size = 1+max(X), 1+max(Y)
    
    xSymbolList = []
    strPuzzle = [[" "] * x_size for y in range(y_size)]
    first_row_wall = 0
    first_col_wall = 0
    left_walls = []
    right_walls = []
    top_walls = []
    bottom_walls = []
    
    
    for (x,y) in warehouse.walls:
            strPuzzle[y][x] = "#"
            
    for y in range(warehouse.nrows):
        first_col_wall = True
        for x in range(warehouse.ncols):
            if (x,y) in warehouse.walls and first_col_wall:
                first_col_wall = False
                left_walls.append([x,y])
            if x == warehouse.ncols - 1:
                temp_col = x
                # for col in range(warehouse.ncols):
                while True:
                    if (temp_col,y) in warehouse.walls:
                        break
                    temp_col = temp_col - 1
                right_walls.append([temp_col,y])
                
    
    for x in range(warehouse.ncols):
        first_row_wall = True
        for y in range(warehouse.nrows):
            if (x,y) in warehouse.walls and first_row_wall:
                first_row_wall = False
                top_walls.append([x,y])
            if y == warehouse.nrows - 1:
                temp_row = y
                # for row in range(warehouse.nrows):   
                while True:
                    if (x,temp_row) in warehouse.walls:
                        break
                    temp_row = temp_row - 1
                bottom_walls.append([x,temp_row])
            
    for y in range(warehouse.nrows):
        for x in range(warehouse.ncols):  
            if not (x,y) in warehouse.walls and not (x,y) in warehouse.targets:
                if (x-1,y) in warehouse.walls or (x-1,y) in xSymbolList:
                    if (x,y-1) in warehouse.walls or (x,y-1) in xSymbolList:
                            xSymbolList.append([x,y])
                            continue
                    if (x,y+1) in warehouse.walls or (x,y+1) in xSymbolList:
                            xSymbolList.append([x,y])  
                            continue
                if (x+1,y) in warehouse.walls or (x+1,y) in xSymbolList:
                    if (x,y-1) in warehouse.walls or (x,y-1) in xSymbolList:  
                            xSymbolList.append([x,y]) 
                            continue
                    if (x,y+1) in warehouse.walls or (x,y+1) in xSymbolList:
                            xSymbolList.append([x,y])  
                            continue
                        
                        
    # for (x,y) in xSymbolList:
    #       strPuzzle[y][x] = "X"
                        
                        
    for (x,y) in xSymbolList:
        for (left_col,left_row) in left_walls:
            if x > left_col and left_row == y:
                for(right_col,right_row) in right_walls:
                    if x < right_col and right_row == y:
                        for (top_col,top_row) in top_walls:
                            if y > top_row and top_col == x:
                                for (bottom_col,bottom_row) in bottom_walls:
                                    if y < bottom_row and bottom_col == x:
                                        strPuzzle[y][x] = "X"
                    
    return "\n".join(["".join(line) for line in strPuzzle])

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def read_taboo_cells(taboo_cells_str):
    '''
    Parameters
    ----------
    taboo_cells_str : string
        A warehouse string version onyl with taboo and walls.

    Raises
    ------
    ValueError
        When wall is empty raise error.

    Returns
    -------
    list
        A list that represent taboo position exmaple :[[x,y]...[xn,yn]].

    '''
    lines = taboo_cells_str.split(sep='\n')    
    first_row_brick, first_column_brick = None, None
    for row, line in enumerate(lines):
        brick_column = line.find('#')
        if brick_column>=0: 
            if  first_row_brick is None:
                first_row_brick = row # found first row with a brick
            if first_column_brick is None:
                first_column_brick = brick_column
            else:
                first_column_brick = min(first_column_brick, brick_column)
    if first_row_brick is None:
        raise ValueError('Warehouse with no walls!')
    # compute the canonical representation
    # keep only the lines that contain walls
    canonical_lines = [line[first_column_brick:] 
                       for line in lines[first_row_brick:] if line.find('#')>=0]
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

    
    def __init__(self, initial=None, goal=None, allow_taboo_push=False, macro=False):
     
    
        self.initial = initial.copy()
        if goal is None:
        
            self.goal = self.initial.targets
#            self.goal.boxes = self.goal.targets
        else:
            self.goal = goal #assumen it represent warehouse class
#        self.initial = initial #assumen it also represent warehouse class
        if allow_taboo_push is None:
            self.allow_taboo_push = True
        else: 
            self.allow_taboo_push = allow_taboo_push
        if macro is None:
            self.macro = False
        else:
            self.macro = macro

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        listOfActions = []
        if self.allow_taboo_push:
            for direct in (UP, RIGHT, DOWN, LEFT):
                for (x,y) in state.boxes:
                    if direct == UP:
                        if not (x,y+1) in state.worker:
                            continue
                        if not direct.go(x,y) in state.walls:
                            continue
                        if not direct.go(x,y) in state.boxes:
                            continue
                    if direct == RIGHT:
                        if not (x-1,y) in state.worker:
                            continue
                        if not direct.go(x,y) in state.walls:
                            continue
                        if not direct.go(x,y) in state.boxes:
                            continue
                    if direct == DOWN:
                        if not (x,y-1) in state.worker:
                            continue
                        if not direct.go(x,y) in state.walls:
                            continue
                        if not direct.go(x,y) in state.boxes:
                            continue
                    if direct == LEFT:
                        if not (x+1,y) in state.worker:
                            continue
                        if not direct.go(x,y) in state.walls:
                            continue
                        if not direct.go(x,y) in state.boxes:
                            continue
                    listOfActions.append((x,y),direct.__str__())

            return listOfActions
            
        else:    
            for direct in (UP, RIGHT, DOWN, LEFT):
                new_position = direct.go(list(state.worker))
                
                
                if new_position in state.walls:
                    continue
                if new_position in state.boxes:
                    new_box_position = direct.go(new_position)
                    if new_box_position in state.walls:
                        continue
                    if new_box_position in state.boxes:
                        continue
                    if not state.allow_taboo_push:
                        if new_box_position in read_taboo_cells(taboo_cells(state)):
                            continue

                # new_state = state.copy(tuple(new_position),new_box_position)
                listOfActions.append(direct.__str__())
        
#        if self.macro:
#            for direct in (UP, RIGHT, DOWN, LEFT):
#                for (x,y) in state.boxes:
#                    if direct == UP:
#                        if not (x,y+1) in state.worker:
#                            continue
#                        if not direct.go(x,y) in state.walls:
#                            continue
#                        if not direct.go(x,y) in state.boxes:
#                            continue
#                    if direct == RIGHT:
#                        if not (x-1,y) in state.worker:
#                            continue
#                        if not direct.go(x,y) in state.walls:
#                            continue
#                        if not direct.go(x,y) in state.boxes:
#                            continue
#                    if direct == DOWN:
#                        if not (x,y-1) in state.worker:
#                            continue
#                        if not direct.go(x,y) in state.walls:
#                            continue
#                        if not direct.go(x,y) in state.boxes:
#                            continue
#                    if direct == LEFT:
#                        if not (x+1,y) in state.worker:
#                            continue
#                        if not direct.go(x,y) in state.walls:
#                            continue
#                        if not direct.go(x,y) in state.boxes:
#                            continue
#                    listOfActions.append((x,y),direct.__str__())
#
#            return listOfActions
#            
#        else:    
#            for direct in (UP, RIGHT, DOWN, LEFT):
#                new_position = direct.go(list(state.worker))
#                
#                
#                if new_position in state.walls:
#                    continue
#                if new_position in state.boxes:
#                    new_box_position = direct.go(new_position)
#                    if new_box_position in state.walls:
#                        continue
#                    if new_box_position in state.boxes:
#                        continue
#                    if not state.allow_taboo_push:
#                        if new_box_position in read_taboo_cells(taboo_cells(state)):
#                            continue
#
#                # new_state = state.copy(tuple(new_position),new_box_position)
#                listOfActions.append(direct.__str__())

            return listOfActions
    
    
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
       
        str_warehouse = check_elem_action_seq(state, action)
            
        if str_warehouse == 'Impossible':
#            return str_warehouse
            return state
        return state.from_string(str_warehouse)
        

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        return set(self.goal) == set(state.boxes) 

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def h(self, n):
        heur = 0
        print(n.state.boxes)
        print(n.state.worker)
        for box in n.state.boxes:
    		#Find closest target
            closest_target = n.state.targets[0]
            for target in n.state.targets:
                if(mDist(target, box) < mDist(closest_target, box)):
                    closest_targetet = target
    				
    		 #updateHeuristic
            heur = heur + mDist(closest_target, box)              
    
        return heur
             
        # k = len(n.state)
        # assert k == len(self.goal)
        # misplaced = [x for i,x in enumerate(n.state) if x!=k-1-i]
        # if misplaced:
        #     # some elements misplaced
        #     return 1+max(misplaced)
        # else:
        #     return 0
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def mDist(loca_a, loca_b):

    return abs((loca_a[0] - loca_b[0])) + abs((loca_a[1] - loca_b[1]))



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
    position_one = position_two = warehouse.worker

    for step in action_seq:
        x, y = warehouse.worker
        
        if step == 'Left':
            position_one = LEFT.go(position_one)
            position_two = LEFT.go(position_one)
            
        elif step == 'Right':
            position_one = RIGHT.go(position_one)
            position_two = RIGHT.go(position_one)
        
        elif step == 'Up':
            position_one = UP.go(position_one)
            position_two = UP.go(position_one)
        
        elif step == 'Down':
            position_one = DOWN.go(position_one)
            position_two = DOWN.go(position_one)         
        
        if position_one in warehouse.walls:
            return 'Impossible'

        if position_one in warehouse.boxes:
            if position_two in warehouse.boxes or position_two in warehouse.walls:
                return 'Impossible'
            warehouse.boxes.remove(position_one)
            warehouse.boxes.append(position_two)

        warehouse.worker = position_one 

    return warehouse.__str__()
    
    
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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

    puzzle = SokobanPuzzle(warehouse)

    puzzleGoalState = warehouse.copy() 
#    puzzleSolution = search.breadth_first_graph_search(puzzle)
    puzzleSolution = search.astar_graph_search(puzzle)
    #puzzleSolution = depth_first_graph_search(puzzle)
    #puzzleSolution = astar_graph_search(puzzle, get_Heuristic)
    
    step_move_solution = []
    step_move = []
    
    for node in puzzleSolution.path():
        step_move.append(node.action)
    action_seq = step_move[1:]
    
    if (puzzle.goal_test(puzzleGoalState)):
        return step_move_solution
    elif (puzzleSolution is None or check_elem_action_seq(warehouse,action_seq) == 'Impossible'):
        return 'Impossible'
    else:
        return action_seq
    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def can_go_there(warehouse,dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''
#    frontier = set()
#    explored = set()
#    frontier.add(warehouse.worker)
#
#    while frontier:
#        curr_position = frontier.pop()
#        if curr_position == (dst[1],dst[0]):
#            return True
#        explored.add(curr_position)
#        
#        for direct in (UP, RIGHT, DOWN, LEFT):
#            new_position = direct.go(list(warehouse.worker))
#            
#            if (new_position not in frontier and 
#                new_position not in explored and
#                new_position not in warehouse.walls and 
#                new_position not in warehouse.boxes):
#                frontier.add(new_position)
#    return False
    # Need to flip because the coordinate of the test and the warehouse is opposite
    flipDst = (dst[1],dst[0])
    path = search.astar_graph_search(Travelling(warehouse.worker,flipDst,warehouse))
    if path is None:
        return False
    else:
        return True

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Travelling(search.Problem):
    
    def __init__(self, initial,goal,warehouse):
        '''
        Assign the passed values

        @param
            initial: the initial value of the worker
            warehouse: the warehouse object
            goal: the destination
        '''
        self.initial = initial
        self.goal = goal
        self.warehouse = warehouse
      
    def actions(self,state):
        listOfActions = []
        for direct in (UP, RIGHT, DOWN, LEFT):
            nextStep = direct.go(state)
            if nextStep not in self.warehouse.walls and nextStep not in self.warehouse.boxes:
                listOfActions.append(direct.__str__())
        return listOfActions
                
    def result(self,state,step):
        position = state
        if step == 'Left':
            position = LEFT.go(position)
        elif step == 'Right':
            position = RIGHT.go(position)
        elif step == 'Up':
            position = UP.go(position)
        elif step == 'Down':
            position = DOWN.go(position)  
        state = position
        return state

    def h(self,n):
        state = n.state
        curGoal = self.goal
        return math.sqrt((state[0]-curGoal[0])**2+(state[1]-curGoal[1])**2)
        
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
    
    if warehouse.targets == warehouse.boxes:
        return []
    
    sokoban_macro = SokobanMacro(warehouse)
    
    results = search.astar_graph_search(warehouse)
    if results == None:
        return ['Impossible']
    path = results.path()
    solution = []
    for node in path:
        solution.append(node.action)
    solution.remove(None)   
    #convert (x,y) to (r,c)
    macro_rc = []
    for action in solution:
        macro_rc.append(((action[0][1], action[0][0]), action[1]))
    
    return macro_rc


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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
    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

UP = direction.Way("Up", (0, -1))
RIGHT = direction.Way("Right", (1, 0))
DOWN = direction.Way("Down", (0, 1))
LEFT = direction.Way("Left", (-1, 0))