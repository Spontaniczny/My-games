import pygame
from random import choice

# just some colors in RGB
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
PURPLE = (170, 0, 255)
DARK_BLUE = (0, 0, 165)
BLUE = (0, 140, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 75, 0)
COLOR_DIFFERENCE = 5  # Used later in snake's color shift

CELL_SIZE = 30  # Size of one cell in pixels
COLUMNS = 16  # Number of columns
ROWS = 16  # Number of rows
MARGIN = 1  # Distance between cells in pixels
SCOREBOARD_HEIGHT = 20  # Height of the scoreboard
SPACE = []  # Position of every cell in which the snake can move safely

WIDTH = COLUMNS * CELL_SIZE + MARGIN * (COLUMNS + 1)  # Width of the window in pixels
HEIGHT = ROWS * CELL_SIZE + MARGIN * (ROWS + 1)  # Height of the window in pixels
WINDOW_SIZE = [WIDTH, HEIGHT + SCOREBOARD_HEIGHT]

LEFT = [-1, 0]
RIGHT = [1, 0]
UP = [0, -1]
DOWN = [0, 1]


def add_food(food, free_space):
    """Adds food on available cell"""

    food[0] = choice(free_space)  # Picks new food position from free_space list

    # Removes new food's position from free_space list
    if food[0] in free_space:
        free_space.remove(food[0])


def move_snake(direction, snake, free_space, food):
    """Moves snake in given direction"""

    n = len(snake)

    # Defines snake's head position after making a move
    new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]

    # This loop moves every snake's cell
    for i in range(n, 1, -1):
        snake[i - 1] = snake[i - 2][:]

    # Checks if new head's position is on anything
    if new_head in food:  # If true, adds new food and expands snake
        snake.append([snake[n - 1][0], snake[n - 1][1]])
        add_food(food, free_space)
    elif new_head in snake:  # If touches wall or itself, snake dies
        kill_snake("You died", n)
    elif new_head[0] == 0 or new_head[0] == (COLUMNS - 1) or new_head[1] == 0 or new_head[1] == (ROWS - 1):
        kill_snake("You died", n)
    else:
        free_space.append([snake[n - 1][0], snake[n - 1][1]])  # Appends free_space list to
        if new_head in free_space:                             # allow food to spawn there
            free_space.remove(new_head)  # Removes from free_space list to prevent food from spawning there

    snake[0] = new_head  # New head's position


def add_text(message, font_size = 45, x = WIDTH // 2, y = HEIGHT // 2):
    """Adds text on screen"""

    message = message
    font = pygame.font.Font('freesansbold.ttf', font_size)
    text = font.render(message, True, PURPLE)
    surface = text.get_rect()
    surface.center = (x, y)
    screen.blit(text, surface)
    pygame.display.flip()


def scoreboard_update(n):
    """Counts points and display score"""

    score = n * 10 - 40
    message = "Score: " + str(score)
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(message, True, RED)
    surface = text.get_rect()
    surface.topright = (WIDTH - 10, 3)
    screen.blit(text, surface)


def high_score_display(hs):
    """Displays high score"""

    if not hs:
        hs = 0
    message = "High score: " + str(hs)
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(message, True, RED)
    surface = text.get_rect()
    surface.topleft = (10, 3)
    screen.blit(text, surface)


def get_high_score():
    """Reads the high_score.txt file, and returns high score"""

    try:
        file = open("high_score.txt", "r")
        return file.readline()
    except FileNotFoundError:
        file = open("high_score.txt", "x")
        file.close()
        return None


def high_score_save(n):
    """If your score is better then high score, replace it in file"""

    score = n * 10 - 40
    hs = get_high_score()
    if not hs:
        file = open("high_score.txt", "w")
        file.write(str(score))
    elif score > int(hs):
        file = open("high_score.txt", "w")
        file.write(str(score))


def kill_snake(message, n):
    """Kills snake"""

    high_score_save(n)
    add_text(message)
    # wait 2 seconds
    for i in range(120):
        clock.tick(60)
    add_text("Wanna play again?", font_size = 30, y = HEIGHT // 2 + 50)
    add_text("Press any key if yes", font_size = 25, y = HEIGHT // 2 + 85)
    add_text("Escape if no", font_size = 25, y = HEIGHT // 2 + 110)
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key != pygame.K_ESCAPE:
                    start_game()
        clock.tick(60)


def start_game():
    """Starts game"""

    snake = [[i, ROWS // 2] for i in range(5, 1, -1)]  # Position of every cell of the snake [x, y]
    SPACE.clear()
    free_space = []  # Position of every cell in which food can spawn
    food = [[10, ROWS // 2]]  # Position of first food
    direction = []  # Direction of snake's movement
    last_direction = RIGHT  # Last value in direction list, RIGHT value prevents from dying at the start
    last_move = []  # Direction of snake's previous movement
    darken = True  # Used later in snake's color shift
    time = 0

    # This loop fills up WALLS and SPACE lists
    for column in range(0, COLUMNS):
        for row in range(0, ROWS):
            if not (column == 0 or column == (COLUMNS - 1) or row == 0 or row == (ROWS - 1)):
                SPACE.append([column, row])

    # This loop fills up free_space list
    for cell in SPACE:
        if cell not in snake and cell not in food:
            free_space.append(cell)

    # Main loop of the game
    while True:

        # Check all useful events
        for event in pygame.event.get():
            # If the windows is closed, quit the program
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_w or event.key == pygame.K_UP) and last_direction != DOWN:
                    if UP not in direction:
                        if len(direction) == 1 and last_move == last_direction:
                            direction[0] = UP
                        direction.append(UP)
                        last_direction = UP
                elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and last_direction != RIGHT:
                    if LEFT not in direction:
                        if len(direction) == 1 and last_move == last_direction:
                            direction[0] = LEFT
                        direction.append(LEFT)
                        last_direction = LEFT
                elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and last_direction != UP:
                    if DOWN not in direction:
                        if len(direction) == 1 and last_move == last_direction:
                            direction[0] = DOWN
                        direction.append(DOWN)
                        last_direction = DOWN
                elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and last_direction != LEFT:
                    if RIGHT not in direction:
                        if len(direction) == 1 and last_move == last_direction:
                            direction[0] = RIGHT
                        direction.append(RIGHT)
                        last_direction = RIGHT

        # Moves snake and update screen every 10th frame
        if time % 10 == 0:
            if direction:
                move_snake(direction[0], snake, free_space, food)
                last_move = direction[0]

            # Loop checks if there is any duplicated or changed direction
            # Deletes duplicated or old one if true
            while len(direction) > 1:
                if direction[0] == direction[1]:
                    direction.pop(1)
                else:
                    direction.pop(0)
                    break

            screen.fill(BLACK)  # Color of MARGIN
            temp = GREEN[1]
            for row in range(ROWS):  # Checks every cell in program
                for column in range(COLUMNS):  # Checks every cell in program
                    if row == 0 or column == 0 or row == ROWS - 1 or column == COLUMNS - 1:  # Checks if cell is a wall
                        color = DARK_BLUE
                    elif [column, row] in snake:  # Checks if cell belongs to snake
                        temp = GREEN[1]  # Important variable used under this line
                        #  This loop is used for nice color shift of the snake
                        for i in range(snake.index([column, row])):
                            if darken:  # If true next color is darker
                                if (temp - COLOR_DIFFERENCE) >= DARK_GREEN[1]:  # Checks if next color is in available
                                    temp -= COLOR_DIFFERENCE  # Adds color to variable
                                else:
                                    darken = False  # Color was out of available range, so we make next color lighter
                                    temp += COLOR_DIFFERENCE  # Adds color to variable
                            else:  # If true next color is lighter
                                if (temp + COLOR_DIFFERENCE) <= 255:  # Checks if next color is in available range
                                    temp += COLOR_DIFFERENCE  # Adds color to variable
                                else:
                                    darken = True  # Color was out of available range, so we make next color darker
                                    temp -= COLOR_DIFFERENCE  # Adds color to variable
                        color = (0, temp, 0)  # Color of the snake's cell

                    elif [column, row] == food[0]:  # Checks if cell is in food's position
                        color = RED
                    else:
                        color = BLUE  # Color of free space

                    # Draw a cell
                    pygame.draw.rect(screen,
                                     color,
                                     [(MARGIN + CELL_SIZE) * column + MARGIN,
                                      (MARGIN + CELL_SIZE) * row + MARGIN + SCOREBOARD_HEIGHT,
                                      CELL_SIZE,
                                      CELL_SIZE])
            # Score update
            scoreboard_update(len(snake))
            # Display high score
            high_score_display(get_high_score())
            # Never happening line but really important
            if len(snake) == len(SPACE):
                kill_snake("You win!", len(snake))

        time += 1
        clock.tick(60)
        pygame.display.flip()  # Update the screen


def main():

    # Initiating pygame
    pygame.init()
    global screen
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Snake")
    global clock
    clock = pygame.time.Clock()

    start_game()


if __name__ == '__main__':
    main()
