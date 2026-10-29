import heapq
from termcolor import colored #3shan alwan (3abas)
import math
import time
GOAL = (0, 1, 2, 3, 4, 5, 6, 7, 8)


"""
#Priorities bt3tna : Up, Down, Left, Right hsb refrence
NEIGHBORS = {
    0: [(3, 'Down'), (1, 'Right')],
    1: [(4, 'Down'), (0, 'Left'), (2, 'Right')],
    2: [(5, 'Down'), (1,'Left')],
    3: [(0,'Up'), (6,'Down'), (4,'Right')],
    4: [(1, 'Up'), (7, 'Down'), (3, 'Left'), (5, 'Right')],
    5: [(2,'Up'), (8,'Down'), (4,'Left')],
    6: [(3,'Up'), (7,'Right')],
    7: [(4,'Up'), (6,'Left'), (8,'Right')],
    8: [(5,'Up'),(7,'Left')]
}

"""


#Priorities hsb refrence: Up, Down, Left, Right
moves = { #hasa nfs el neighbors bas msh mot2keda
            #yup, nfs el neighbors
    'Up': -3,  
    'Down': 3,   
    'Left': -1,  
    'Right': 1   
}


class Node:
    def __init__(self, board, parent=None, move=None, depth=0,cost = 0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost
    def __lt__(self,other):
        return self.cost < other.cost

def swap(state, i, j):
    board = list(state)
    board[i], board[j] = board[j], board[i]
    return tuple(board)


"""
def get_children(node):
    i = node.board.index(0)
    children = []
    for j, d in NEIGHBORS[i]:
        new_board = swap(node.board, i, j)
        child = Node(new_board, node, d, node.depth + 1)
        children.append(child)
    return children
"""

#lw 3ozna length el path? len(moves)
def get_path(node):
    moves = []
    while node.parent != None:
        moves.append(node.move)   #han save
        node = node.parent      
    moves.reverse()               # gebna mn goal ll parent, ne3ks ba
    return moves




def moveBlank(board, move, blank):
    return swap(board, blank, blank + moves[move])



#shaklan helw bs, trust
def print_board(board):
    print("┌───┬───┬───┐")
    for r in range(3):
        row = board[r*3 : r*3+3]
        print("│" + "│".join(f" {t if t else ' '} " for t in row) + "│")
        if r < 2:
            print("├───┼───┼───┤")
    print("└───┴───┴───┘")



def print_solution(goal_node):
    nodes = []
    node = goal_node
    while node != None:
        nodes.append(node)
        node = node.parent
    nodes.reverse()

    print("Initial board:")
    print_board(nodes[0].board)

    for step, node in enumerate(nodes[1:], start=1):
        print(f"Step {step}: move {node.move}")
        print_board(node.board)

    print("Goal reached!")


"""
def moveBlank(board,move,blank):
    #move the number based on the move and change blacnk pos
    new = list(board)
    newBlank_position = blank + moves[move]
    new[blank],new[newBlank_position] = new[newBlank_position],new[blank]
    return tuple(new)
"""
#sorry ya rokaia





def HeuristicsEuclidean(board):
    h = 0
    for i,t in enumerate(board):
        if t !=0: #malnash da3wa bl fadi
            x1,y1 = divmod(i,3) #current position
            x2,y2 = divmod(t,3) #goal position
            h += math.sqrt((x1-x2)**2 + (y1-y2)**2)
    return h


def AStarEuclidean(start):
    frontier = []
    explored = set()
    nodes_expanded = 0
    max_depth = 0
    heapq.heappush(frontier,Node(start, None, None, 0, HeuristicsEuclidean(start))) # put start node in heapq
    while frontier:
        current = heapq.heappop(frontier) # get the current with the lowest cost
        max_depth = max(max_depth, current.depth)



        if current.board == GOAL: # if goal reached
            return current, nodes_expanded, max_depth

        
        if current.board in explored:
            continue
        explored.add(tuple(current.board))
        nodes_expanded += 1                      # we expanded this board
        

        blank = current.board.index(0)
        
        for move in moves:
            #no illigal move
            if move =='Up' and blank < 3:
                continue
            if move =='Down' and blank > 5:
                continue
            if move =='Left' and blank % 3 == 0:
                continue
            if move =='Right' and blank % 3 == 2:
                continue
            # shift el Blank
            newboard = moveBlank(current.board, move, blank)
            if tuple(newboard) in explored:
                continue
            #next node
            new = Node(newboard,current,move,current.depth+1,HeuristicsEuclidean(newboard)+current.depth+1)
            heapq.heappush(frontier,new) #push in queue
    return None, nodes_expanded, max_depth
                

def HeuristicsManhattan(board):
    h = 0
    for i, t in enumerate(board):
        if t != 0:  # ignore the blank
            x1, y1 = divmod(i, 3)  # current position
            x2, y2 = divmod(t, 3)  # goal position
            h += abs(x1 - x2) + abs(y1 - y2)
    return h


def AStarManhattan(start):
    frontier = []
    explored = set()
    nodes_expanded = 0
    max_depth = 0
    
    heapq.heappush(frontier, Node(start, None, None, 0, HeuristicsManhattan(start)))
    while frontier:
        current = heapq.heappop(frontier)
        max_depth = max(max_depth, current.depth)
        
        if current.board == GOAL:
            return current, nodes_expanded, max_depth

        if current.board in explored:  # already expanded, skip
            continue
        explored.add(current.board)
        nodes_expanded += 1                      # we expanded this board
        
        blank = current.board.index(0)


        for move in moves:
            if move == 'Up' and blank < 3:
                continue
            if move == 'Down' and blank > 5:
                continue
            if move == 'Left' and blank % 3 == 0:
                continue
            if move == 'Right' and blank % 3 == 2:
                continue

            newboard = moveBlank(current.board, move, blank)
            if newboard in explored:
                continue
            new = Node(newboard, current, move, current.depth + 1,
                       HeuristicsManhattan(newboard) + current.depth + 1)
            heapq.heappush(frontier, new)
    return None, nodes_expanded, max_depth



def run_manhattan(start):
    t0 = time.perf_counter()
    goal_node, expanded, depth = AStarManhattan(start)
    elapsed = time.perf_counter() - t0

    if goal_node is None:
        print("No solution")
        return
    path = get_path(goal_node)
    print_solution(goal_node)                    # every step printed
    print("Path to goal:", path)
    print("Cost of path:", len(path))            # each move costs 1
    print("Nodes expanded:", expanded)
    print("Search depth:", depth)
    print(f"Running time: {elapsed:.4f} s")



def run_euclidean(start):
    t0 = time.perf_counter()
    goal_node, expanded, depth = AStarEuclidean(start)
    elapsed = time.perf_counter() - t0

    if goal_node is None:
        print("No solution")
        return
    path = get_path(goal_node)
    print_solution(goal_node)                    # every step printed
    print("Path to goal:", path)
    print("Cost of path:", len(path))            # each move costs 1
    print("Nodes expanded:", expanded)
    print("Search depth:", depth)
    print(f"Running time: {elapsed:.4f} s")


"""
#mesh ana eli 3mla el test
if __name__ == "__main__":

    start = (8, 0, 6, 5, 4, 7, 2, 3, 1)
    solution = AStarEuclidean(start)
    # Test 1: children of the start (expect 3: Up, Down, Left)
    if solution:
        print("A* solution:", get_path(solution))
        print_solution(solution)
    start_node = Node(start) 
    print("Test 1: children")
    for child in get_children(start_node):
        print(child.move)
        print_board(child.board)

    # Build a small path by hand
    a = Node((1, 2, 0, 3, 4, 5, 6, 7, 8), start_node, 'Up', 1)
    b = Node((1, 0, 2, 3, 4, 5, 6, 7, 8), a, 'Left', 2)
    c = Node(GOAL, b, 'Left', 3)

    # Test 2: get_path (expect ['Up', 'Left', 'Left'])
    print("Test 2: path")
    print(get_path(c))

    # Test 3: print_solution (initial board, 3 steps, goal reached)
    print("Test 3: full solution")
    print_solution(c)

    """



if __name__ == "__main__":
    start = (1, 0, 2, 3, 4, 5, 6, 7, 8)
    print("===== MANHATTAN =====")
    run_manhattan(start)
    print("===== EUCLIDEAN =====")
    run_euclidean(start)