import csv
import time
from fifteenpuzzle import FifteenPuzzleState, FifteenPuzzleSearchProblem, createRandomFifteenPuzzle
from search import aStarSearch, H1, H2, H3, H4
from statistics import mean
from tabulate import tabulate
from multiprocessing import Process, Queue
#start of task 3 
# Define a dictionary to map heuristics to their functions
heuristics = {
    'h1': H1,
    'h2': H2,
    'h3': H3,
    'h4': H4
}

# Generate random puzzles and save them in a file
def generate_random_puzzles(filename, num_puzzles=20):
    """
    Generate random 15-puzzle configurations and save them to a file.
    """
    with open(filename, 'w') as file:
        for _ in range(num_puzzles):
            puzzle = createRandomFifteenPuzzle()
            config = [puzzle.cells[row][col] for row in range(4) for col in range(4)]
            config_str = ' '.join(map(str, config))
            file.write(config_str + '\n')

# Read puzzle configurations from a file
def read_puzzle_configurations(filename):
    """
    Read puzzle configurations from a file.
    """
    configurations = []
    with open(filename, 'r') as file:
        for line in file:
            config = [int(n) for n in line.strip().split()]
            configurations.append(config)
    return configurations

# Run the A* search with the specified heuristic and log the results in the result_queue
def run_search_algorithm(problem, heuristic_function, result_queue):
    """
    Function to run the search algorithm and put the result in the queue.
    """
    start_time = time.time()
    try:
        result = aStarSearch(problem, heuristic_function)
        
        # Return result as expected
        path = result['Solution']
        nodes_expanded = result['Expanded Nodes']
        max_fringe_size = result['Max Fringe Size']
        depth = result['Depth']
        execution_time = time.time() - start_time
        
        result_queue.put((path, nodes_expanded, max_fringe_size, depth, execution_time))
    except Exception as e:
        print(f"Error: {e}")
        result_queue.put((None, "Timeout", "Timeout", "Timeout", "Timeout"))

def main():
    # Step 1: Generate random puzzles and save them to a CSV file
    puzzle_filename = 'scenarios.csv'
    generate_random_puzzles(puzzle_filename)

    # Step 2: Read puzzle configurations from the CSV file
    configurations = read_puzzle_configurations(puzzle_filename)
    
    # Step 3: Define a dictionary to store results for each heuristic
    results = {heuristic: {'Nodes Expanded': [], 'Max Fringe Size': [], 'Depth': [], 'Execution Time': []} for heuristic in heuristics.keys()}
    timeout = 120 # Timeout value in seconds for each configuration

    # Step 4: Open the results CSV file and write headers
    with open('results.csv', 'w', newline='') as results_file:
        results_writer = csv.writer(results_file)
        results_writer.writerow(['Initial State', 'Heuristic', 'Expanded Nodes', 'Max Fringe Size', 'Depth', 'Execution Time'])

        # Step 5: Iterate over each puzzle configuration
        for config in configurations:
            puzzle = FifteenPuzzleState(config)  # Create a FifteenPuzzleState object for each configuration
            problem = FifteenPuzzleSearchProblem(puzzle)  # Create a search problem for the configuration

            # Step 6: Run the search algorithm for each heuristic
            for heuristic_name, heuristic_function in heuristics.items():
                result_queue = Queue()
                process = Process(target=run_search_algorithm, args=(problem, heuristic_function, result_queue))
                process.start()

                # Wait for the process to finish or timeout
                process.join(timeout)

                if process.is_alive():
                    print(f"Timeout occurred for configuration {config} with heuristic {heuristic_name}")
                    process.terminate()
                    process.join()
                    results_writer.writerow([' '.join(map(str, config)), heuristic_name, "Timeout", "Timeout", "Timeout", "Timeout"])
                else:
                    try:
                        path, nodes_expanded, max_fringe_size, depth, execution_time = result_queue.get()
                    except Exception as e:
                        print(f"Error retrieving results from queue: {e}")
                        path, nodes_expanded, max_fringe_size, depth, execution_time = None, "Error", "Error", "Error", "Error"

                    if path is None:
                        nodes_expanded = max_fringe_size = depth = execution_time = "Timeout"

                    if nodes_expanded != "Timeout":
                        results[heuristic_name]['Nodes Expanded'].append(nodes_expanded)
                        results[heuristic_name]['Max Fringe Size'].append(max_fringe_size)
                        results[heuristic_name]['Depth'].append(depth)
                        results[heuristic_name]['Execution Time'].append(execution_time)
                    
                    results_writer.writerow([' '.join(map(str, config)), heuristic_name, nodes_expanded, max_fringe_size, depth, execution_time])

    # Calculate averages for each heuristic
    averages = {
        heuristic: {
            'Avg Nodes Expanded': mean(metrics['Nodes Expanded']) if metrics['Nodes Expanded'] else "N/A",
            'Avg Max Fringe Size': mean(metrics['Max Fringe Size']) if metrics['Max Fringe Size'] else "N/A",
            'Avg Depth': mean(metrics['Depth']) if metrics['Depth'] else "N/A",
            'Avg Execution Time': mean(metrics['Execution Time']) if metrics['Execution Time'] else "N/A"
        }
        for heuristic, metrics in results.items()
    }

    # Display the average results using the tabulate library
    headers = ["Heuristic", "Avg Nodes Expanded", "Avg Max Fringe Size", "Avg Depth", "Avg Execution Time"]
    rows = [[heuristic, averages[heuristic]['Avg Nodes Expanded'], averages[heuristic]['Avg Max Fringe Size'], averages[heuristic]['Avg Depth'], averages[heuristic]['Avg Execution Time']] for heuristic in averages.keys()]
    
    print("\nAverage Results:")
    print(tabulate(rows, headers=headers, tablefmt="grid"))

if _name_ == "_main_":
    main()



    #end of task 3 