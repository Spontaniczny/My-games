import pygame
import random
from math import sqrt


WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (170, 0, 255)
BLACK = (0, 0, 0)

WIDTH = 600
HEIGHT = 500
fps = 60


def add_text(message, color = PURPLE, font_size = 30, x = 0, y = 0, on_left = False, on_right = False):
    """Adds text on screen"""

    message = message
    font = pygame.font.Font('freesansbold.ttf', font_size)
    text = font.render(message, True, color)
    surface = text.get_rect()
    if on_left:
        surface.left = 15
    elif on_right:
        surface.right = WIDTH - 15
    else:
        surface.centerx = x
    surface.centery = y
    screen.blit(text, surface)


class Paddle(pygame.sprite.Sprite):

    def __init__(self, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.centery = 475
        self.distance = 0
        self.x_temp = 0
        pygame.draw.rect(self.image, WHITE, [0, 0, width, height])

    def update(self):
        self.x_temp = self.rect.x
        self.rect.x = pygame.mouse.get_pos()[0]
        if self.rect.left <= 45:
            self.rect.left = 45
        elif self.rect.right >= WIDTH - 45:
            self.rect.right = WIDTH - 45

        self.distance = self.rect.x - self.x_temp


class Ball(pygame.sprite.Sprite):

    def __init__(self):
        super(Ball, self).__init__()
        self.speed = 8
        self.image = pygame.Surface([15, 15])
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.centery = HEIGHT // 2
        self.dy = random.randint(100, self.speed * 100 - 10) / 100
        self.speed_dx()
        self.paddle_enabled = True
        self.score = 0
        pygame.draw.rect(self.image, WHITE, [0, 0, 15, 15])

    def speed_dx(self):
        """Calculates vertical speed, when everything else is known"""
        self.dx = sqrt(self.speed * self.speed - self.dy * self.dy)

    def speed_dy(self):
        """Calculates horizontal speed, when everything else is known"""
        self.dy = sqrt(self.speed * self.speed - self.dx * self.dx)

    def move(self):
        """Moves ball"""
        self.rect.x += self.dx
        self.rect.y += self.dy

    def update(self):

        # Checks all sprites that collide with ball
        for thing in pygame.sprite.spritecollide(self, all_sprites_list, False):
            # If ball touches paddle...
            if type(thing) == Paddle and self.paddle_enabled:
                # and ball is not too low, then bounce up
                if thing.rect.top <= self.rect.bottom <= (thing.rect.top + self.dy * 1.4):
                    self.paddle_enabled = False
                    # paddle.distance allows player to control the ball
                    self.dx = paddle.distance / 3 + self.dx
                    if self.dx >= self.speed:
                        self.dx = self.speed - 0.3
                    elif -self.dx >= self.speed:
                        self.dx = -(self.speed - 0.3)
                    self.speed_dy()
                    self.dy = -1 * self.dy
                    self.score += 10
                # and ball is too low, then bounce left or right
                else:
                    self.paddle_enabled = False
                    if self.rect.right >= thing.rect.left and paddle.distance == 0:
                        self.dx = -self.dx
                    elif paddle.distance < 0 and self.dx < 0 or paddle.distance > 0 and self.dx > 0:
                        self.dx = -(paddle.distance / 3 - self.dx)
                    else:
                        self.dx = (paddle.distance / 3 - self.dx)

            elif type(thing) == Ceiling:
                self.paddle_enabled = True
                self.rect.y += 1
                self.dy = -self.dy

            elif type(thing) == Wall:
                if self.dx < 0:
                    self.rect.x += 1
                else:
                    self.rect.x -= 1
                self.dx = -self.dx

        self.move()
        self.score_update()

        if self.rect.top >= HEIGHT + 5:
            self.kill()
            self.end_game()

    def score_update(self):
        """Updates score"""
        message = "Score: " + str(self.score)
        add_text(message, color = RED, font_size = 18, y = 10, on_right = True)

    @staticmethod
    def end_game():
        """Displays eng message, and ands the game"""
        add_text("You lose!", x = WIDTH // 2, y = HEIGHT // 2)
        pygame.display.flip()
        for i in range(300):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
            clock.tick(60)
        pygame.quit()
        quit()


class Wall(pygame.sprite.Sprite):

    def __init__(self, x):
        super(Wall, self).__init__()
        self.image = pygame.Surface([30, 455])
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = 20
        pygame.draw.rect(self.image, WHITE, [0, 0, 30, 455])


class Ceiling(pygame.sprite.Sprite):

    def __init__(self):
        super(Ceiling, self).__init__()
        self.image = pygame.Surface([510, 30])
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.y = 20
        pygame.draw.rect(self.image, WHITE, [0, 0, 540, 30])


# Initiating pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
all_sprites_list = pygame.sprite.Group()
pygame.mouse.set_visible(False)

# Creating paddle
paddle = Paddle(100, 20)
all_sprites_list.add(paddle)

ball = Ball()
all_sprites_list.add(ball)

wall_left = Wall(30)
all_sprites_list.add(wall_left)
wall_right = Wall(570)
all_sprites_list.add(wall_right)
celling = Ceiling()
all_sprites_list.add(celling)

while True:

    # Checks all useful events
    for event in pygame.event.get():
        # If the windows is closed, quit the program
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

    screen.fill(BLACK)
    # Draws every sprite in the list on the screen
    all_sprites_list.draw(screen)
    # Calls the update method of every sprite in the list
    all_sprites_list.update()

    pygame.display.flip()
    clock.tick(fps)
