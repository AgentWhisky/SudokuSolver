import pygame
import time
from pygame.color import Color

pygame.init()

win_size = (400, 400 + 40)
box_size = 40
background_colour = (255, 255, 255)

# Class to simulate a puzzle cell
class Box():
    def __init__(self, x, y):
        self.size = box_size
        self.rect = pygame.Rect(x, y, self.size, self.size)
        # Hover Colors
        self.color_base = (0, 0, 0)
        self.color_mouse_over = (255, 0, 0)
        self.color_selected = 21, 173, 74
        self.thick = 1

        self.selected = False

        self.current_color = self.color_base

    def draw(self, win, value):
        # Drawing Box
        pygame.draw.rect(win, self.current_color, self.rect, self.thick)

        # Box Value
        font = pygame.font.SysFont('arial', 30)
        if not value < 1 or value > 9:
            text = font.render(str(value), True, (0, 0, 0))
            win.blit(text, (self.rect.x + 13, self.rect.y + 1))


# Build UI Board
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
            cols.append(Box((i * box_size + offset_x), (j * box_size + offset_y)))
        boxes.append(cols)
    return boxes


# Run Tool
def run(window):
    # box = Box(20, 20)
    puzzle = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    solve_time = 0
    # Build Board
    boxes = build_board()

    current_box = (-1, -1)

    running = True
    while running:
        # Background
        pygame.draw.rect(window, background_colour, (0, 0, win_size[0], win_size[1]))

        mouse_pos = pygame.mouse.get_pos()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Mouse Interactions
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in range(9):
                        for j in range(9):
                            if boxes[i][j].rect.collidepoint(mouse_pos):
                                current_box = (i, j)
                elif event.button == 3:
                    current_box = (-1, -1)

            # Keyboard Interactions
            if event.type == pygame.KEYDOWN:

                if 48 < event.key < 58:
                    switch = {
                        49: 1,
                        50: 2,
                        51: 3,
                        52: 4,
                        53: 5,
                        54: 6,
                        55: 7,
                        56: 8,
                        57: 9
                    }
                    num = switch.get(event.key)
                    if num is not None:
                        puzzle[current_box[1]][current_box[0]] = num

                # Clear Selected Box
                elif event.key == 8:
                    if not current_box == (-1, -1):
                        puzzle[current_box[1]][current_box[0]] = 0

                # Delete Pressed, Clear Puzzle
                elif event.key == 127:
                    clear_puzzle(puzzle)
                    solve_time = 0

                # Space Pressed, Solve Puzzle (If Possible)
                elif event.key == 32:
                    clock = time.perf_counter()
                    if not solve_puzzle(puzzle):
                        print("Impossible Puzzle")
                        solve_time = -1
                    else:
                        solve_time = round((time.perf_counter() - clock) * 1000, 6)

        # Check box collision color
        for i in range(9):
            for j in range(9):
                if (i, j) == current_box:
                    boxes[i][j].current_color = boxes[i][j].color_selected
                    boxes[i][j].thick = 3

                elif boxes[i][j].rect.collidepoint(mouse_pos):
                    boxes[i][j].current_color = boxes[i][j].color_mouse_over
                    boxes[i][j].thick = 3
                else:
                    boxes[i][j].current_color = boxes[i][j].color_base
                    boxes[i][j].thick = 1

        # Draw
        draw_separators(window)

        # Draw Solve Time Text
        font = pygame.font.SysFont('arial', 24)
        if solve_time == 0:
            time_str = "Solve Time: "
        elif solve_time == -1:
            time_str = "Solve Time: Impossible"
        else:
            time_str = "Solve Time: " + str(solve_time) + "ms"
        text = font.render(time_str, True, (0, 0, 0))
        window.blit(text, (20, win_size[1] - 40))

        # Draw boxes with current values
        for i in range(9):
            for j in range(9):
                if (j, i) == current_box:
                    boxes[j][i].draw(window, puzzle[i][j])
                else:
                    boxes[j][i].draw(window, puzzle[i][j])

        pygame.display.flip()

    # Quit
    pygame.quit()


def draw_separators(window):
    # Draw Matrix Vertical Separators
    pygame.draw.line(window, (0, 0, 0), (4, 10), (4, box_size * 9 + 30 * 3), width=10)
    pygame.draw.line(window, (0, 0, 0), (box_size * 3 + 14, 10), (box_size * 3 + 14, box_size * 9 + 30), width=10)
    pygame.draw.line(window, (0, 0, 0), (box_size * 6 + 24, 10), (box_size * 6 + 24, box_size * 9 + 30), width=10)
    pygame.draw.line(window, (0, 0, 0), (box_size * 9 + 34, 10), (box_size * 9 + 34, box_size * 9 + 30 * 3), width=10)
    # Draw Matrix Horizontal Separators
    pygame.draw.line(window, (0, 0, 0), (0, 4), (box_size * 9 + 39, 4), width=10)
    pygame.draw.line(window, (0, 0, 0), (0, box_size * 3 + 14), (box_size * 9 + 39, box_size * 3 + 14), width=10)
    pygame.draw.line(window, (0, 0, 0), (0, box_size * 6 + 24), (box_size * 9 + 39, box_size * 6 + 24), width=10)
    pygame.draw.line(window, (0, 0, 0), (0, box_size * 9 + 34), (box_size * 9 + 39, box_size * 9 + 34), width=10)
    pygame.draw.line(window, (0, 0, 0), (0, box_size * 9 + 34 + 40), (box_size * 9 + 39, box_size * 9 + 34 + 40),
                     width=10)


# Print the Sudoku Puzzle to Console
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


# Function to recursive solve the puzzle
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


# Function to clear a given puzzle
def clear_puzzle(puzzle):
    for i in range(9):
        for j in range(9):
            puzzle[i][j] = 0


# Function to find the next empty cell
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


def main():
    window = pygame.display.set_mode(win_size)
    pygame.display.set_caption('Sudoku Solver Mk2')
    run(window)


if __name__ == '__main__':
    main()
