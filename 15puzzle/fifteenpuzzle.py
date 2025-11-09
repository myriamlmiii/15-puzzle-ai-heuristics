import random
import search

# start of task 1 
class FifteenPuzzleState:
    def __init__(self, numbers):
        self.cells = []
        numbers = numbers[:]  # Avoid side effects by copying
        numbers.reverse()  # Reverse the list to populate the grid correctly
        for row in range(4): # Changed from 3 to 4 for 15-puzzle
            self.cells.append([])  # Create rows
            for col in range(4): # Changed from 3 to 4 for 15-puzzle
                self.cells[row].append(numbers.pop())  # Fill the grid
                if self.cells[row][col] == 0:
                    self.blankLocation = row, col  # Store blank tile location in the space of most bottom right 


    def __getAsciiString(self):
        lines = []
        horizontalLine = ('-' * (5 * 4 + 1))  # Line for 4x4 grid
        lines.append(horizontalLine)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col == 0:
                    col = ' '  # Represent the blank tile
                rowLine += ' {:2} |'.format(col)  # Format for alignment
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()

    def __eq__(self, other):
        return self.cells == other.cells

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.cells))

    def __lt__(self, other):
        return str(self) < str(other)


 # end of taks 1 


    def isGoal(self):
        current = 1
        for row in range(4):
            for col in range(4):
                if row == 3 and col == 3:
                    return self.cells[row][col] == 0  # Blank tile at bottom-right
                if self.cells[row][col] != current:
                    return False
                current += 1
        return True

    def legalMoves(self):
        moves = []
        row, col = self.blankLocation
        if row != 0:
            moves.append('up')
        if row != 3:
            moves.append('down')
        if col != 0:
            moves.append('left')
        if col != 3:
            moves.append('right')
        return moves

    def result(self, move):
        row, col = self.blankLocation
        if move == 'up':
            newrow = row - 1
            newcol = col
        elif move == 'down':
            newrow = row + 1
            newcol = col
        elif move == 'left':
            newrow = row
            newcol = col - 1
        elif move == 'right':
            newrow = row
            newcol = col + 1
        else:
            raise Exception("Illegal move")

        newPuzzle = FifteenPuzzleState([0] * 16)
        newPuzzle.cells = [values[:] for values in self.cells]
        newPuzzle.cells[row][col] = self.cells[newrow][newcol]
        newPuzzle.cells[newrow][newcol] = 0
        newPuzzle.blankLocation = newrow, newcol

        return newPuzzle

class FifteenPuzzleSearchProblem(search.SearchProblem):
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.expanded_nodes = 0  # Track how many nodes have been expanded
        self.max_fringe_size = 0  # Track the maximum size of the fringe

    def getStartState(self):
        return self.puzzle

    def isGoalState(self, state):
        return state.isGoal()

    def getSuccessors(self, state):
        successors = []
        for action in state.legalMoves():
            successor = state.result(action)
            successors.append((successor, action, 1))  # Cost is 1 for all moves
        return successors

    def getCostOfActions(self, actions):
        return len(actions)

def createRandomFifteenPuzzle(moves=100):
    puzzle = FifteenPuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0])
    for _ in range(moves):
        puzzle = puzzle.result(random.choice(puzzle.legalMoves()))
    return puzzle

if __name__ == '__main__':
    puzzle = createRandomFifteenPuzzle(25)
    print('Random puzzle:')
    print(puzzle)

    problem = FifteenPuzzleSearchProblem(puzzle)

    # Display search algorithm and heuristic options
    print("Choose a search method:")
    print("1: Uniform Cost Search (UCS)")
    print("2: Breadth-First Search (BFS)")
    print("3: Depth-First Search (DFS)")
    print("4: A* Search with Heuristics (choose which one after)")
    print("Press any other letter to exit.")

    method_choice = input("Choose method (1, 2, 3, 4): ").strip()

    if method_choice == '4':
        # Dictionary of heuristics
        heuristics = {
            '1': ('Misplaced Tiles', search.H1),
            '2': ('Euclidean Distance', search.H2),
            '3': ('Manhattan Distance', search.H3),
            '4': ('Heuristic based on Row/Column Misalignment', search.H4)
        }

        print("Choose a heuristic for A* search:")
        print("1: Misplaced Tiles - Counts the number of tiles not in their correct position.")
        print("2: Euclidean Distance - Measures the straight-line distance of each tile to its goal.")
        print("3: Manhattan Distance - Measures the number of moves each tile is away from its goal position.")
        print("4: Heuristic based on Row/Column Misalignment - Counts the number of tiles not in their goal row/column.")
        print("Press any other letter to exit.")
        
        heuristic_choice = input("Choose heuristic (1, 2, 3, 4): ").strip()

        if heuristic_choice in heuristics:
            heuristic_name, heuristic = heuristics[heuristic_choice]
            print(f"You chose A* search with heuristic: {heuristic_name}")
            result = search.aStarSearch(problem, heuristic)
            path = result.get('Solution')
        else:
            print("Invalid heuristic. Please choose a valid option next time.")
            path = None  # Set path to None to indicate no solution process.

    elif method_choice == '1':
        print("You chose Uniform Cost Search (UCS).")
        path = search.uniformCostSearch(problem)

    elif method_choice == '2':
        print("You chose Breadth-First Search (BFS).")
        path = search.breadthFirstSearch(problem)

    elif method_choice == '3':
        print("You chose Depth-First Search (DFS).")
        path = search.depthFirstSearch(problem)

    else:
        print("Exiting the program.")
        path = None

    # Display the solution path step-by-step if a valid search method was chosen.
    if path is not None and path:
        print(f"Search found a path of {len(path)} moves.")
        print('Solution path:')
        curr = puzzle
        for i, action in enumerate(path):
            curr = curr.result(action)
            print(f'After move {i+1}: {action}')
            print(curr)
            input("Press Enter to view the next state...")  # Wait for user to press Enter before showing next move
        print("Congratulations! Goal is reached. Puzzle is solved!")
        print(f"A* found a path: {path}")  # Print the sequence of moves at the end
    elif path is not None:
        print("No solution found.")
