import pygame
import os
import random

from pygame.sprite import _Group

# initialise pygame
pygame.init()

# screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Run Penguin, RUN!")

# constants
BACKGROUND = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# framerate
clock = pygame.time.Clock
FPS = 60

# game variables
GRAVITY = 0.75
TITLE_SIZE = 40

# define player moves
moving_left = False
moving_right = False
shoot = False

# load bullet image
bullet_img = pygame.image.load("img/icon/bullet.png").convert_alpha()

# pick up items - health & ammo
healthbox_img = pygame.image.load("img/icon/life.png").convert_alpha()
ammo_box_img = pygame.image.load("img/icon/ammo_box.png").convert_alpha()

item_boxes = {
    "Health" : healthbox_img,
    "Ammo" : ammo_box_img
}

# font for displaying text
font = pygame.font.SysFont(None, 36)

# creating our character
class Penguin(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True    # player is alive at start
        self.char_type = char_type
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.health = 200
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0        # when player is in idle mode
        self.update_time = pygame.time.get_ticks()
        
        # for AI movements
        self.move_counter = 0
        self.vision = pygame.Rect(0,0,150,20)
        self.idling = False
        self.idling_counter = 0