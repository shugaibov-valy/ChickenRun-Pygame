import pygame
import os
import sys

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 760

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Chiken Run')

# define game variables
flying = False
game_over = False
score = 0

# load images
bg = pygame.image.load('img/bg.png')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


tile_images = {
    'wall': load_image('box.png'),
}
tile_width = tile_height = 50

tiles_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]

        self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if flying == True:
            # gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
        if game_over == False:
            # jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # handle the animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
        else:
            self.image = pygame.transform.rotate(self.images[self.index], self.vel)


def load_level(filename):
    filename = "data/" + filename
    # reading the level by removing newline characters
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # and calculate the maximum length
    max_width = max(map(len, level_map))

    # complete each line with empty cells ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level, c):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('wall', x - c, y)
    # we will return the player, as well as the size of the field in cells
    return new_player, x, y


bird_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)

speed_tile = 0
run = True
while run:

    clock.tick(fps)

    # draw background
    tiles_group = pygame.sprite.Group()
    screen.blit(bg, (0, 0))
    level_map = load_level('map.txt')
    hero, level_x, level_y = generate_level(level_map, speed_tile)
    speed_tile += 0.04
    tiles_group.draw(screen)
    tiles_group.update()
    bird_group.draw(screen)
    bird_group.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
    pygame.display.update()

pygame.quit()
