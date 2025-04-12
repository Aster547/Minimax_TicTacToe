import pygame
import math
import minimax_algo

pygame.init()

# Screen
WIDTH = 440
ROWS = 4
# WIDTH = 600
# ROWS = 3
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("TicTacToe")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Images
box_size = WIDTH // ROWS  # Dynamically calculate the box size
X_IMAGE = pygame.transform.scale(pygame.image.load("images/x.png"), (box_size - 20, box_size - 20))
O_IMAGE = pygame.transform.scale(pygame.image.load("images/o.png"), (box_size - 20, box_size - 20))

# Fonts
END_FONT = pygame.font.SysFont('arial', 40)


def draw_grid():
    gap = WIDTH // ROWS

    # Starting points
    x = 0
    y = 0

    for i in range(ROWS):
        x = i * gap

        pygame.draw.line(win, GRAY, (x, 0), (x, WIDTH), ROWS)
        pygame.draw.line(win, GRAY, (0, x), (WIDTH, x), ROWS)


def initialize_grid():
    dis_to_cen = WIDTH // ROWS // 2

    game_array = [[None for _ in range(ROWS)] for _ in range(ROWS)]

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x = dis_to_cen * (2 * j + 1)
            y = dis_to_cen * (2 * i + 1)

            # Adding centre coordinates
            game_array[i][j] = (x, y, "", True)

    return game_array


def click(game_array):
    global x_turn, o_turn, images

    # Get mouse position
    m_x, m_y = pygame.mouse.get_pos()

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x, y, char, can_play = game_array[i][j]

            # Calculate the distance between the mouse click and the center of the box
            dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)

            # Check if the click is within the box
            if dis < WIDTH // ROWS // 2 and can_play:
                images.append((x, y, X_IMAGE))
                x_turn = False
                o_turn = True
                game_array[i][j] = (x, y, 'x', False)

                # Get the best move from the AI
                best_move = minimax_algo.TicTacToe(game_array).get_best_move()

                if best_move is not None:
                    row, col = best_move
                    x_ai, y_ai, _, _ = game_array[row][col]

                    images.append((x_ai, y_ai, O_IMAGE))
                    x_turn = True
                    o_turn = False
                    game_array[row][col] = (x_ai, y_ai, 'o', False)


# Checking if someone has won
def has_won(game_array):
    # Checking rows
    for i in range(len(game_array)):
        points = 0
        for j in range(len(game_array)):
            if game_array[i][j][2] == 'o':
                points -= 1
            elif game_array[i][j][2] == 'x':
                points += 1
            if points == len(game_array):
                display_message("X has won!")
                return True
            elif points == -len(game_array):
                display_message("O has won!")
                return True
        points = 0
        for j in range(len(game_array)):
            if game_array[j][i][2] == 'o':
                points -= 1
            elif game_array[j][i][2] == 'x':
                points += 1
            if points == len(game_array):
                display_message("X has won!")
                return True
            elif points == -len(game_array):
                display_message("O has won!")
                return True
    points = 0
    for i in range(len(game_array)):    
        if game_array[i][i][2] == 'o':
            points -= 1
        elif game_array[i][i][2] == 'x':
            points += 1
        if points == len(game_array):
            display_message("X has won!")
            return True
        elif points == -len(game_array):
            display_message("O has won!")
            return True
    points = 0
    for i in range(len(game_array)):    
        if game_array[i][len(game_array)-1-i][2] == 'o':
            points -= 1
        elif game_array[i][len(game_array)-1-i][2] == 'x':
            points += 1
        if points == len(game_array):
            display_message("X has won!")
            return True
        elif points == -len(game_array):
            display_message("O has won!")
            return True
    return False


def has_drawn(game_array):
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            if game_array[i][j][2] == "":
                return False

    display_message("It's a draw!")
    return True


def display_message(content):
    pygame.time.delay(500)
    win.fill(WHITE)
    end_text = END_FONT.render(content, 1, BLACK)
    win.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(3000)


def render():
    win.fill(WHITE)  # Clear the screen
    draw_grid()  # Draw the grid

    # Draw X's and O's
    for image in images:
        x, y, IMAGE = image
        win.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))

    pygame.display.update()  # Update the display


def main():
    global x_turn, o_turn, images, draw

    images = []
    draw = False

    run = True

    x_turn = True
    o_turn = False

    game_array = initialize_grid()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click(game_array)

        render()

        if has_won(game_array) or has_drawn(game_array):
            run = False


while True:
    if __name__ == '__main__':
        main()
