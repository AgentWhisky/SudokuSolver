from copy import copy, deepcopy

import pygame
import time
import constants

pygame.init()


class Box():
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, constants.BOX_SIZE, constants.BOX_SIZE)

    def draw(self, win, value, color, thickness, new):
        # Drawing Box
        pygame.draw.rect(win, constants.COLOR_WHITE, self.rect)
        pygame.draw.rect(win, color, self.rect, thickness)

        # Box Value
        font = pygame.font.SysFont('arial', 30)

        if new:
            text_color = constants.COLOR_GREEN
        else:
            text_color = constants.COLOR_BLACK

        # Only display if value is 1-9
        if not value < 1 or value > 9:
            text = font.render(str(value), True, text_color)
            win.blit(text, (self.rect.x + 13, self.rect.y + 1))


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


def is_empty(puzzle):
    for i in range(9):
        for j in range(9):
            if not puzzle[i][j] == 0:
                return False
    return True


# Function to solve a given 2D array puzzle
def solve_puzzle(puzzle):
    # No empty spots
    index = find_empty(puzzle)
    if not index:
        return True
    for i in range(1, 10):
        if valid(puzzle, i, index):
            puzzle[index[0]][index[1]] = i

            if solve_puzzle(puzzle):
                return True
            puzzle[index[0]][index[1]] = 0
    return False


def find_empty(puzzle):
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                index = (i, j)
                return index
    return None


# Check if the value is valid in the row
def row_valid(puzzle, value, index):
    for i in range(9):
        if value == puzzle[index[0]][i]:
            return False
    return True


# Check if the value is valid in the column
def col_valid(puzzle, value, index):
    for i in range(9):
        if value == puzzle[i][index[1]]:
            return False
    return True


# Check if the value is valid inside the box
def box_valid(puzzle, value, index):
    if index[0] < 3:
        # Top Boxes
        if index[1] < 3:
            box = (0, 0)
        elif index[1] < 6:
            box = (0, 3)
        else:
            box = (0, 6)
    elif index[0] < 6:
        # Middle Boxes
        if index[1] < 3:
            box = (3, 0)
        elif index[1] < 6:
            box = (3, 3)
        else:
            box = (3, 6)
    else:
        # Bottom Boxes
        if index[1] < 3:
            box = (6, 0)
        elif index[1] < 6:
            box = (6, 3)
        else:
            box = (6, 6)

    for i in range(3):
        for j in range(3):
            if value == puzzle[i + box[0]][j + box[1]]:
                return False
    return True


# Check that the puzzle to be solved has valid entries
def is_valid_puzzle(puzzle):
    for i in range(9):
        for j in range(9):
            if not puzzle[i][j] == 0:
                hold_value = puzzle[i][j]
                puzzle[i][j] = 0

                if not valid(puzzle, hold_value, (i, j)):
                    puzzle[i][j] = hold_value
                    return False
                puzzle[i][j] = hold_value
    return True


# Check if a given value is valid in the location given
def valid(puzzle, value, loc):
    if not row_valid(puzzle, value, loc):
        return False
    if not col_valid(puzzle, value, loc):
        return False
    if not box_valid(puzzle, value, loc):
        return False
    return True


def build_empty_puzzle():
    puzzle = []
    for i in range(9):
        puzzle.append([])
        for j in range(9):
            puzzle[i].append(0)
    return puzzle


def clear_puzzle(puzzle):
    for i in range(9):
        for j in range(9):
            puzzle[i][j] = 0


def copy_puzzle(puzzle):
    copy_puzzle = []
    for i in range(9):
        copy_puzzle.append([])
        for j in range(9):
            copy_puzzle[i].append(puzzle[i][j])
    return copy_puzzle


def build_board():
    boxes = []
    offset_x = 0
    offset_y = 0
    for i in range(9):
        cols = []
        if i == 0 or i == 3 or i == 6:
            offset_x += 10
        offset_y = 0
        for j in range(9):
            if j == 0 or j == 3 or j == 6:
                offset_y += 10
            cols.append(Box((i * constants.BOX_SIZE + offset_x), (j * constants.BOX_SIZE + offset_y)))
        boxes.append(cols)
    return boxes


def draw_text(window, solve_time, toggle_new):
    font_info = pygame.font.SysFont('arial', 24)

    if solve_time == -1:
        time_str = constants.IMPOSSIBLE
    elif solve_time == 0:
        time_str = constants.TIME_STR
    else:
        time_str = "Solve Time: " + str(solve_time) + "ms"

    if toggle_new:
        new_str = "Show New: On"
    else:
        new_str = "Show New: Off"

    time_text = font_info.render(time_str, True, constants.COLOR_WHITE)
    window.blit(time_text, (20, constants.WINDOW_SIZE[1] - constants.BOX_SIZE * 2))

    new_text = font_info.render(new_str, True, constants.COLOR_WHITE)
    window.blit(new_text, (20, constants.WINDOW_SIZE[1] - constants.BOX_SIZE))


def run(window):
    # Building Empty Default Puzzle
    puzzle = build_empty_puzzle()
    orig_puzzle = []

    # Building Board
    boxes = build_board()

    # Setting Default Solve Time
    solve_time = 0

    # Set Current Box Index to unassigned
    current_index = (-1, -1)

    # Set Show new values
    show_new = False

    running = True
    while running:

        # Get Mouse Position
        mouse_pos = pygame.mouse.get_pos()

        # Events
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                running = False

            # Mouse Click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == constants.LEFT_MOUSE:
                    for i in range(9):
                        for j in range(9):
                            if boxes[i][j].rect.collidepoint(mouse_pos):
                                current_index = (i, j)
                elif event.button == constants.RIGHT_MOUSE:
                    current_index = (-1, -1)

            # Key Pressed
            if event.type == pygame.KEYDOWN:
                if 48 < event.key < 58:
                    switch = {
                        constants.ONE_KEY: 1,
                        constants.TWO_KEY: 2,
                        constants.THREE_KEY: 3,
                        constants.FOUR_KEY: 4,
                        constants.FIVE_KEY: 5,
                        constants.SIX_KEY: 6,
                        constants.SEVEN_KEY: 7,
                        constants.EIGHT_KEY: 8,
                        constants.NINE_KEY: 9,
                    }
                    num = switch.get(event.key)
                    if num is not None:
                        puzzle[current_index[1]][current_index[0]] = num

                # Clear Selected Box
                elif event.key == constants.BACKSPACE_KEY:
                    if not current_index == (-1, -1):
                        puzzle[current_index[1]][current_index[0]] = 0

                # Clear Puzzle
                elif event.key == constants.DELETE_KEY:
                    clear_puzzle(puzzle)
                    solve_time = 0
                    orig_puzzle = []


                # Space Pressed, Solve Puzzle (If Possible)
                elif event.key == constants.SPACE_KEY:
                    print_puzzle(puzzle)
                    if not is_valid_puzzle(puzzle):
                        solve_time = -1
                        orig_puzzle = []
                    else:
                        if not is_empty(puzzle):
                            orig_puzzle = copy_puzzle(puzzle)
                            current_index = (-1, -1)
                            clock = time.perf_counter()
                            if not solve_puzzle(puzzle):
                                solve_time = -1
                                orig_puzzle = []
                            else:
                                solve_time = round((time.perf_counter() - clock) * 1000, 6)



                # Toggle Show New
                elif event.key == constants.TILDE_KEY:
                    if show_new:
                        show_new = False
                    else:
                        show_new = True

        # Drawing Components

        # Drawing Background
        pygame.draw.rect(window, constants.COLOR_BLACK, (0, 0, constants.WINDOW_SIZE[0], constants.WINDOW_SIZE[1]))

        # Draw Solve Time Text
        draw_text(window, solve_time, show_new)

        # Drawing Boxes
        for i in range(9):
            for j in range(9):

                # Default color
                new = 0

                # If show new is toggled
                if show_new:
                    # Check if value new (from solving puzzle)
                    if orig_puzzle:
                        if not puzzle[j][i] == orig_puzzle[j][i]:
                            new = 1
                # If the box is currently selected
                if (i, j) == current_index:
                    boxes[i][j].draw(window, puzzle[j][i], constants.COLOR_GREEN, 2, new)
                # If mouse is hovering over box
                elif boxes[i][j].rect.collidepoint(mouse_pos):
                    boxes[i][j].draw(window, puzzle[j][i], constants.COLOR_RED, 1, new)
                # Default Box
                else:
                    boxes[i][j].draw(window, puzzle[j][i], constants.COLOR_BLACK, 1, new)

        # Update Window
        pygame.display.flip()

    # Quit
    pygame.quit()


def main():
    window = pygame.display.set_mode(constants.WINDOW_SIZE)
    pygame.display.set_caption('Sudoku Solver Mk3')
    run(window)


if __name__ == '__main__':
    main()
