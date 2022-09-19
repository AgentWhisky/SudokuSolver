def main():
    # X DOWN
    # Y RIGHT
    puzzle = [[3, 0, 0, 0, 0, 0, 0, 0, 8],
              [6, 0, 0, 0, 0, 0, 0, 5, 2],
              [0, 5, 0, 0, 2, 0, 4, 0, 0],
              [0, 4, 1, 8, 0, 9, 2, 0, 6],
              [7, 0, 0, 2, 0, 6, 0, 0, 4],
              [2, 0, 6, 5, 0, 7, 3, 8, 0],
              [0, 0, 3, 0, 7, 0, 0, 6, 0],
              [4, 6, 0, 0, 0, 0, 0, 0, 7],
              [1, 0, 0, 0, 0, 0, 0, 0, 3]]

    if not (solve_puzzle(puzzle)):
        print("Impossible Puzzle")
    else:
        print_puzzle(puzzle)


# Print the Sudoku Puzzle
def print_puzzle(puzzle):
    print("-" * 25)
    for i in range(9):
        if i == 3 or i == 6:
            print("-" * 25)
        print("|", end=" ")
        for j in range(9):
            if j == 3 or j == 6:
                print("|", end=" ")
            print(puzzle[i][j], end=" ")
        print("|")
    print("-" * 25)


# Function or recursively solve the puzzle
def solve_puzzle(puzzle):
    # No empty spots
    loc = find_empty(puzzle)
    if not loc:
        return True

    for i in range(1, 10):
        if valid(puzzle, i, loc):
            puzzle[loc[0]][loc[1]] = i

            if solve_puzzle(puzzle):
                return True
            puzzle[loc[0]][loc[1]] = 0
    return False


# Find index of next empty puzzle cell
def find_empty(puzzle):
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                loc = (i, j)
                return loc
    return None


# Check if a given value is valid in the location given
def valid(puzzle, value, loc):
    if not row_valid(puzzle, value, loc):
        return False
    if not col_valid(puzzle, value, loc):
        return False
    if not box_valid(puzzle, value, loc):
        return False
    return True


# Check if the value is valid in the row
def row_valid(puzzle, value, loc):
    for i in range(9):
        if value == puzzle[loc[0]][i]:
            return False
    return True


# Check if the value is valid in the column
def col_valid(puzzle, value, loc):
    for i in range(9):
        if value == puzzle[i][loc[1]]:
            return False
    return True


# Check if the value is valid inside the box
def box_valid(puzzle, value, loc):
    if loc[0] < 3:
        # Top Boxes
        if loc[1] < 3:
            box = (0, 0)
        elif loc[1] < 6:
            box = (0, 3)
        else:
            box = (0, 6)
    elif loc[0] < 6:
        # Middle Boxes
        if loc[1] < 3:
            box = (3, 0)
        elif loc[1] < 6:
            box = (3, 3)
        else:
            box = (3, 6)
    else:
        # Bottom Boxes
        if loc[1] < 3:
            box = (6, 0)
        elif loc[1] < 6:
            box = (6, 3)
        else:
            box = (6, 6)

    for i in range(3):
        for j in range(3):
            if value == puzzle[i + box[0]][j + box[1]]:
                return False
    return True


if __name__ == '__main__':
    main()
