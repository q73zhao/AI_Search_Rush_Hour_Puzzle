from board import *
import copy
import queue
    

def __new_lt__(self, other):
    if self.f < other.f:
        return True
    elif self.f == other.f:
        if self.id < other.id:
            return True
        elif self.id == other.id:
            if self.parent.id < other.parent.id:
                return True
            else:
                return False
        else:
            return False
    else:
        return False
    
State.__lt__ = __new_lt__


def a_star(init_board, hfn):
    """
    Run the A_star search algorithm given an initial board and a heuristic function.

    If the function finds a goal state, it returns a list of states representing
    the path from the initial state to the goal state in order and the cost of
    the solution found.
    Otherwise, it returns am empty list and -1.

    :param init_board: The initial starting board.
    :type init_board: Board
    :param hfn: The heuristic function.
    :type hfn: Heuristic
    :return: (the path to goal state, solution cost)
    :rtype: List[State], int
    """
    
    
    initialstate = State(init_board, hfn, hfn(init_board), 0, None)
    
    

    frontier = queue.PriorityQueue()
    frontier.put(initialstate)
    
    
    explored = list()
    length = 0

    
    while frontier:
    #for k in range(10): 
        index = -1

        currentState = frontier.get()
        #print(currentState.f, currentState.id)   

        if currentState.board not in explored:
            length += 1

            explored.append(currentState.board)
            
            if is_goal(currentState):
                print("Number of node expanded using " + hfn.__name__ + " is " + str(length))

                return get_path(currentState), currentState.depth
            
            los = get_successors(currentState)

            for s in los:
                frontier.put(s)


    empty = list()
    
    
    return empty, -1




def dfs(init_board):
    """
    Run the DFS algorithm given an initial board.

    If the function finds a goal state, it returns a list of states representing
    the path from the initial state to the goal state in order and the cost of
    the solution found.
    Otherwise, it returns am empty list and -1.

    :param init_board: The initial board.
    :type init_board: Board
    :return: (the path to goal state, solution cost)
    :rtype: List[State], int
    """
    
    
    
    initialstate = State(init_board, zero_heuristic, 0, 0, None)
    
    frontier = list()
    
    frontier.append(initialstate)

    
    explored = list()


    while frontier:
    #for i in range(1):  
        currentState = frontier.pop()
        
        if currentState.board not in explored:
            explored.append(currentState.board)            
            if is_goal(currentState):
                print("Number of node expanded by DFS is " + str(currentState.depth))
                return get_path(currentState), currentState.depth

        
            #tmp = get_successors(currentState)
            #print(len(tmp))

            statedict = dict()
            for successor in get_successors(currentState):
                #print("here")
                statedict[successor.id] = successor
            

            statedict = statedict.items()
            statedict = sorted(statedict,reverse=True)
            
            
            for key, value in statedict:
                frontier.append(value)
        
            
        
    empty = list()
    
    return empty, -1
        
        
        
    
    
def get_successors(state):
    """
    Return a list containing the successor states of the given state.
    The states in the list may be in any arbitrary order.

    :param state: The current state.
    :type state: State
    :return: The list of successor states.
    :rtype: List[State]
    """
    
    successors = list()
    
    for car in state.board.cars:
        
        if car.orientation == 'h':
                    
            lblank = 0
                        
            currentColumn = car.var_coord - 1
            
            while  currentColumn >= 0:
                
                if state.board.grid[car.fix_coord][currentColumn] == '.':
                    lblank += 1
                    currentColumn -= 1
                else:
                    break


            rblank = 0
            
            currentColumn = car.var_coord + car.length
            
            while currentColumn < state.board.size:
                
                if state.board.grid[car.fix_coord][currentColumn] == '.':
                    rblank += 1
                    currentColumn += 1
                else:
                    break

            factor = 1
            
            for i in range(lblank+rblank):
                
                tmp = i

                if i >= lblank:
                    factor = -1
                    tmp = i - lblank
                    
                #newCar = state.board.cars.copy()
                newCar = copy.deepcopy(state.board.cars)

                
                index = state.board.cars.index(car)
                
                newCar[index].set_coord(car.var_coord-(tmp+1)*factor)
                
                nextBoard = Board(state.board.name, state.board.size, newCar)
                
                nextF = state.hfn(nextBoard) + state.depth + 1 #one more cost
                
                nextState = State(nextBoard,state.hfn, nextF, state.depth+1, state)
                
                
                successors.append(nextState)
                
        else: #case when the orientation is v
            
            ublank = 0
            
            currentRow = car.var_coord - 1
            
            while currentRow >= 0:
                if state.board.grid[currentRow][car.fix_coord] == '.':
                    ublank += 1
                    currentRow -= 1
                else:
                    break
            
            dblank = 0
            
            currentRow = car.var_coord + car.length
            
            while currentRow < state.board.size:
                
                if state.board.grid[currentRow][car.fix_coord] == '.':
                    dblank += 1
                    
                    currentRow += 1
                else:
                    break
            
            factor = 1
            
            for i in range(ublank + dblank):
                
                tmp = i

                if i >= ublank:
                    factor = -1
                    tmp = i - ublank
                
                #newCar = state.board.cars.copy()
                newCar = copy.deepcopy(state.board.cars)
                
                index = state.board.cars.index(car)
                
                newCar[index].set_coord(car.var_coord-(tmp+1)*factor)
                
                nextBoard = Board(state.board.name, state.board.size, newCar)
                
                nextF = state.hfn(nextBoard) + state.depth + 1 #one more cost
                
                nextState = State(nextBoard,state.hfn, nextF, state.depth+1, state)
                
                
                successors.append(nextState)
                    

        
    return successors
        

def is_goal(state):
    """
    Returns True if the state is the goal state and False otherwise.

    :param state: the current state.
    :type state: State
    :return: True or False
    :rtype: bool
    """
    
    goalcar = state.board.cars[0]
    
    return (goalcar.var_coord == 4)


def get_path(state):
    """
    Return a list of states containing the nodes on the path 
    from the initial state to the given state in order.

    :param state: The current state.
    :type state: State
    :return: The path.
    :rtype: List[State]
    """
    
    
    
    path = list()
    
    
    while state.parent != None:
        path.insert(0, state)
        state = state.parent
        
    path.insert(0,state) 
    
    return path       
    


def blocking_heuristic(board):
    """
    Returns the heuristic value for the given board
    based on the Blocking Heuristic function.

    Blocking heuristic returns zero at any goal board,
    and returns one plus the number of cars directly
    blocking the goal car in all other states.

    :param board: The current board.
    :type board: Board
    :return: The heuristic value.
    :rtype: int
    """
    
    
    currentState = State(board,zero_heuristic,0,0,None)
    
    if is_goal(currentState):
        return 0
    
    goalcar = board.cars[0]
    counter = 1
    
    for car in board.cars:
        if car.orientation == 'v' and car.fix_coord >= \
            goalcar.var_coord + goalcar.length and car.var_coord <= \
                goalcar.fix_coord and car.var_coord+car.length-1 >= \
                    goalcar.fix_coord:
            counter += 1
    

    return counter


def advanced_heuristic(board):
    """
    An advanced heuristic of your own choosing and invention.

    :param board: The current board.
    :type board: Board
    :return: The heuristic value.
    :rtype: int
    """

    currentState = State(board, zero_heuristic, 0, 0, None)

    if is_goal(currentState):
        return 0

    goalcar = board.cars[0]
    counter = 1
    blocking = list()
    filterblocking = list()

    for car in board.cars:
        if car.orientation == 'v' and car.fix_coord > \
                goalcar.var_coord + goalcar.length-1 and car.var_coord <= \
                goalcar.fix_coord and car.var_coord + car.length - 1 >= \
                goalcar.fix_coord:
            counter += 1
            blocking.append(car)

    for car in blocking:

        ublank = 0
        dblank = 0
        i = 1
        upfree = car.var_coord + car.length - goalcar.fix_coord
        downfree = goalcar.fix_coord - car.var_coord + 1

        while car.var_coord - i >= 0:
            if board.grid[car.var_coord - i][car.fix_coord] == '.':
                ublank += 1
                i += 1
            else:
                break
        i = 1
        while car.var_coord + car.length - 1 + i < board.size:
            if board.grid[car.var_coord + car.length - 1 + i][car.fix_coord] == '.':
                dblank += 1
                i += 1

            else:
                break

        if ublank >= upfree or dblank >= downfree:
            continue
        else:
            filterblocking.append(car)

    # for each blocking car, we need to find the car directy blocking it

    if len(filterblocking) > 0:
        counter += 1

    return counter







