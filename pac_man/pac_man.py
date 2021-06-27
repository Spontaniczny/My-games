import pygame
from math import fabs

WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (170, 0, 255)
BLACK = (0, 0, 0)


WIDTH = 699
HEIGHT = 756
fps = 50


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


class PacMan(pygame.sprite.Sprite):

    def __init__(self, x = WIDTH // 2, y = 568):
        super(PacMan, self).__init__()
        self.image_2 = pygame.image.load("pac_man2.png")
        self.image_left = pygame.image.load("pac_man_left.png")
        self.image_right = pygame.image.load("pac_man_right.png")
        self.image_up = pygame.image.load("pac_man_up.png")
        self.image_down = pygame.image.load("pac_man_down.png")
        self.image = self.image_2
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.score = 0
        self.last_image = self.image_2
        self.dx = 0
        self.dy = 0
        self.last_dx = self.dx
        self.last_dy = self.dy
        self.last_x = self.rect.x
        self.last_y = self.rect.y
        self.animation_time = 0
        self.time = 0
        self.direction = None
        self.distance1 = 0
        self.distance2 = 0
        self.score = 0

    def update(self):
        self.time += 1
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.change_movement()
        self.check_if_touch()
        self.check_image()
        self.teleportation()
        self.last_x = self.rect.x
        self.last_y = self.rect.y
        self.last_dx = self.dx
        self.last_dy = self.dy
        self.message = "Score " + str(self.score)
        add_text(self.message, y = 15, font_size=25, on_right=True)

    def get_colisions(self):
        self.colide = pygame.sprite.spritecollide(self, all_sprites_list, False)
        if self in self.colide:
            self.colide.remove(self)

    def check_movement(self, key):
        if key == pygame.K_w:
            self.direction = "w"
        elif key == pygame.K_s:
            self.direction = "s"
        elif key == pygame.K_a:
            self.direction = "a"
        elif key == pygame.K_d:
            self.direction = "d"

    def change_movement(self):
        if self.direction == "a" or self.direction == "d":
            if self.rect.centery % 23 == 16 or self.dy == 0:
                if self.direction == "a":
                    self.rect.x -= 2
                    self.get_colisions()
                    if self.colide:
                        for sprite in self.colide:
                            if type(sprite) != Wall:
                                self.dx = -1
                                self.dy = 0
                    else:
                        self.dx = -1
                        self.dy = 0
                    self.rect.x += 2
                else:
                    self.rect.x += 2
                    self.get_colisions()
                    if self.colide:
                        for sprite in self.colide:
                            if type(sprite) != Wall:
                                self.dx = 1
                                self.dy = 0
                    else:
                        self.dx = 1
                        self.dy = 0
                    self.rect.x -= 2
        elif self.direction == "w" or self.direction == "s":
            if self.rect.centerx % 23 == 16 or self.dx == 0:
                if self.direction == "w":
                    self.rect.y -= 2
                    self.get_colisions()
                    if self.colide:
                        for sprite in self.colide:
                            if type(sprite) != Wall:
                                self.dy = -1
                                self.dx = 0
                    else:
                        self.dy = -1
                        self.dx = 0
                    self.rect.y += 2
                else:
                    self.rect.y += 2
                    self.get_colisions()
                    if self.colide:
                        for sprite in self.colide:
                            if type(sprite) != Wall:
                                self.dy = 1
                                self.dx = 0
                    else:
                        self.dy = 1
                        self.dx = 0
                    self.rect.y -= 2

    def check_image(self):
        self.animation_time += 1
        self.last_image = self.image
        if self.last_dx != self.dx or self.last_dy != self.dy:
            self.animation_time = 24
        if self.animation_time % 25 == 0 and (self.last_x != self.rect.x or self.last_y != self.rect.y):
            if self.dx == -1:
                self.image = self.image_left
                self.image.set_colorkey(WHITE)
            if self.dx == 1:
                self.image = self.image_right
                self.image.set_colorkey(WHITE)
            if self.dy == -1:
                self.image = self.image_up
                self.image.set_colorkey(WHITE)
            if self.dy == 1:
                self.image = self.image_down
                self.image.set_colorkey(WHITE)
            if self.last_image != self.image_2 and (self.dx != 0 or self.dy != 0):
                self.image = self.image_2
                self.image.set_colorkey(WHITE)

    def check_if_touch(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.get_colisions()
        if self.colide:
            for spirit in self.colide:
                if type(spirit) == Point:
                    self.score += 10
                    spirit.kill()
                elif self.dx != 0:
                    self.distance1 = fabs(self.rect.left - spirit.rect.right)
                    self.distance2 = fabs(self.rect.right - spirit.rect.left)
                    if self.distance1 < self.distance2:
                        self.rect.left = spirit.rect.right + 1
                    else:
                        self.rect.right = spirit.rect.left - 1
                elif self.dy != 0:
                    self.distance1 = fabs(self.rect.top - spirit.rect.bottom)
                    self.distance2 = fabs(self.rect.bottom - spirit.rect.top)
                    if self.distance1 < self.distance2:
                        self.rect.top = spirit.rect.bottom + 1
                    else:
                        self.rect.bottom = spirit.rect.top - 1
        else:
            self.rect.x -= self.dx
            self.rect.y -= self.dy

    def teleportation(self):
        if self.dx == 1 and self.rect.left == WIDTH:
            self.rect.right = 0
        elif self.dx == -1 and self.rect.right == 0:
            self.rect.left = WIDTH


class Point(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(Point, self).__init__()
        self.image = pygame.Surface([6, 6])
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        pygame.draw.rect(self.image, WHITE, [0, 0, 6, 6])


class Wall(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        super(Wall, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        for spirit in pygame.sprite.spritecollide(self, all_sprites_list, False):
            if type(spirit) != Wall:
                spirit.kill()


# Initiating pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac Man")
clock = pygame.time.Clock()
all_sprites_list = pygame.sprite.Group()

pacman = PacMan()
all_sprites_list.add(pacman)

for i in range(59, WIDTH - 42, 23):
    for j in range(59, HEIGHT - 39, 23):
        point = Point(i, j)
        all_sprites_list.add(point)


image = pygame.image.load("surface.bmp")

wall = Wall(image, 30, 30)
all_sprites_list.add(wall)
wall = Wall(image, 30, HEIGHT - 30)
all_sprites_list.add(wall)

image = pygame.image.load("wall_3x2.bmp")

wall = Wall(image, 82, 82)
all_sprites_list.add(wall)
wall = Wall(image, 542, 82)
all_sprites_list.add(wall)

image = pygame.image.load("wall_4x2.bmp")

wall = Wall(image, 197, 82)
all_sprites_list.add(wall)
wall = Wall(image, 404, 82)
all_sprites_list.add(wall)

image = pygame.image.load("wall_1x3.bmp")

wall = Wall(image, 335, 197)
all_sprites_list.add(wall)
wall = Wall(image, 335, 473)
all_sprites_list.add(wall)
wall = Wall(image, 335, 611)
all_sprites_list.add(wall)
wall = Wall(image, 128, 542)
all_sprites_list.add(wall)
wall = Wall(image, 542, 542)
all_sprites_list.add(wall)
wall = Wall(image, 197, 588)
all_sprites_list.add(wall)
wall = Wall(image, 473, 588)
all_sprites_list.add(wall)

image = pygame.image.load("wall_3x1.bmp")

wall = Wall(image, 82, 174)
all_sprites_list.add(wall)
wall = Wall(image, 542, 174)
all_sprites_list.add(wall)
wall = Wall(image, 82, 519)
all_sprites_list.add(wall)
wall = Wall(image, 542, 519)
all_sprites_list.add(wall)
wall = Wall(image, 220, 243)
all_sprites_list.add(wall)
wall = Wall(image, 404, 243)
all_sprites_list.add(wall)

image = pygame.image.load("wall_1x7.bmp")

wall = Wall(image, 197, 174)
all_sprites_list.add(wall)
wall = Wall(image, 473, 174)
all_sprites_list.add(wall)

image = pygame.image.load("wall_1x4.bmp")

wall = Wall(image, 197, 381)
all_sprites_list.add(wall)
wall = Wall(image, 473, 381)
all_sprites_list.add(wall)

image = pygame.image.load("wall_7x1.bmp")

wall = Wall(image, 266, 174)
all_sprites_list.add(wall)
wall = Wall(image, 266, 450)
all_sprites_list.add(wall)
wall = Wall(image, 266, 588)
all_sprites_list.add(wall)

image = pygame.image.load("wall_4x1.bmp")

wall = Wall(image, 197, 519)
all_sprites_list.add(wall)
wall = Wall(image, 404, 519)
all_sprites_list.add(wall)

image = pygame.image.load("wall_9x1.bmp")

wall = Wall(image, 82, 657)
all_sprites_list.add(wall)
wall = Wall(image, 404, 657)
all_sprites_list.add(wall)

image = pygame.image.load("wall_2x1.bmp")

wall = Wall(image, 35, 588)
all_sprites_list.add(wall)
wall = Wall(image, 611, 588)
all_sprites_list.add(wall)

image = pygame.image.load("wall_9.bmp")

wall = Wall(image, 30, 42)
all_sprites_list.add(wall)
wall = Wall(image, 657, 42)
all_sprites_list.add(wall)

image = pygame.image.load("block.bmp")

wall = Wall(image, 30, 243)
all_sprites_list.add(wall)
wall = Wall(image, 542, 243)
all_sprites_list.add(wall)
wall = Wall(image, 30, 381)
all_sprites_list.add(wall)
wall = Wall(image, 542, 381)
all_sprites_list.add(wall)

image = pygame.image.load("wall_11.bmp")

wall = Wall(image, 30, 479)
all_sprites_list.add(wall)
wall = Wall(image, 657, 479)
all_sprites_list.add(wall)

image = pygame.image.load("cell.bmp")

wall = Wall(image, 266, 312)
all_sprites_list.add(wall)

time = 0
while True:

    # Check all useful events
    for event in pygame.event.get():
        # If the windows is closed, quit the program
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            pacman.check_movement(event.key)

    screen.fill(BLACK)
    all_sprites_list.draw(screen)

    all_sprites_list.update()

    pygame.display.flip()
    time += 1
    clock.tick(fps)
