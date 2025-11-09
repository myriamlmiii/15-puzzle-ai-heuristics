import time
import csv
from fifteenpuzzle import FifteenPuzzleSearchProblem, createRandomFifteenPuzzle  # Import your problem and puzzle creation
from search import aStarSearch, breadthFirstSearch, depthFirstSearch, uniformCostSearch  # Import your search algorithms
#start of task 4 
# Define the number of test cases
num_tests = 250
results = []

# Define search strategies
strategies = {
    'A* (H3)': aStarSearch,
    'BFS': breadthFirstSearch,
    'DFS': depthFirstSearch,
    'UCS': uniformCostSearch
}

# Run tests
for i in range(num_tests):
    puzzle = createRandomFifteenPuzzle()  # Create a random 15-puzzle
    problem = FifteenPuzzleSearchProblem(puzzle)  # Set up the search problem

    for strategy_name, strategy in strategies.items():
        start_time = time.time()
        result = strategy(problem)  # Execute the search strategy

        if result['Solved']:
            execution_time = time.time() - start_time
            results.append([
                puzzle, strategy_name, result['Expanded Nodes'], 
                result['Max Fringe Size'], result['Depth'], 
                execution_time
            ])
        else:
            results.append([
                puzzle, strategy_name, "Timeout", "Timeout", "Timeout", "Timeout"
            ])

# Write results to a CSV file
with open('comparison_results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Initial State', 'Strategy', 'Expanded Nodes', 'Max Fringe Size', 'Depth', 'Execution Time'])
    writer.writerows(results)

# Print results summary (optional)
for row in results:
    print(row)


#end of task 4 