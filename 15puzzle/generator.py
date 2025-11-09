import csv
import random
import fifteenpuzzle as F  # Make sure you have this module set up properly

def get_inversions(arr):
    """
    Count the number of inversions in the puzzle.
    """
    inv_count = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j] and arr[i] != 0 and arr[j] != 0:
                inv_count += 1
    return inv_count

def is_solvable(puzzle):
    """
    Check if the puzzle is solvable based on inversions.
    """
    inv_count = get_inversions([num for row in puzzle for num in row])
    return inv_count % 2 == 0

def generate_scenarios(filename, count):
    """
    Generate solvable 15-puzzle configurations and write to CSV.
    """
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        generated = 0
        while generated < count:
            puzzle = F.createRandomFifteenPuzzle(100)  # Create a random 15-puzzle
            if is_solvable(puzzle.cells):  # Check if the puzzle is solvable
                writer.writerow([num for row in puzzle.cells for num in row])
                print(f"Generated solvable puzzle #{generated + 1}")
                generated += 1
    print(f"{count} solvable puzzles generated and saved to {filename}")

if __name__ == "__main__":
    generate_scenarios("scenarios.csv", 250)  # Generate 250 random solvable puzzles
