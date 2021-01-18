import pygame
import os
import sys

import main
from main import *
menu_musfon = pygame.mixer.Sound("music/menu_fon.mp3")
first_time = datetime.datetime.now()

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


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        self.first_image = image

    def draw(self):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            self.image = load_image('Button.png')

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        if not self.rect.collidepoint(pos):
            self.image = self.first_image
        screen.blit(self.image, self.rect)

        return action


def menu():
    global lose
    global run
    global map_speed
    global finish
    global winner
    global first_time
    global first_time
    import start_music
    start_music.menu_music()
    menu_bg = pygame.transform.scale(load_image('Menu-Fon.png'), (864, 760))
    Start_button_img = load_image("Start-Button.png")
    About_Button_img = load_image("About-Button.png")
    Exit_Button_img = load_image("Exit-Button.png")
    Settings_Button_img = load_image('Settings-Button.png')
    start = Button(screen_width // 2, screen_height // 2 - 150, Start_button_img)
    exit = Button(screen_width // 2, screen_height // 2 + 150, Exit_Button_img)
    about = Button(screen_width // 2, screen_height // 2 + 50, About_Button_img)
    settings = Button(screen_width // 2, screen_height // 2 - 50, Settings_Button_img)
    while True:
        screen.blit(menu_bg, (0, 0))
        start.draw()
        about.draw()
        exit.draw()
        settings.draw()
        if start.clicked == True:
            first_time = datetime.datetime.now()
            pygame.mixer.stop()
            return
        if exit.clicked == True:
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        pygame.display.flip()

