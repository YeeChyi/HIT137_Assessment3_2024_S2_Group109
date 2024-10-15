import pygame
import os
import random
import csv

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
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT//ROWS
TILE_TYPES = 18
level = 1

# define player moves
moving_left = False
moving_right = False
shoot = False

img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/tiles/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

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

# display info 
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg():
    screen.fill(BACKGROUND)

# creating our character
class Penguin(
    pygame.sprite.Sprite):
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
        
        # player movements (images)
        animation_types = ['idle', 'walking', 'jumping', 'death']
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (70, 70))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
    def move(self, moveing_left, moving_right):
        dx = 0
        dy = 0
        
        # to keep the player within the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            
        # assign movement if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        
        # jump action
        if self.jump and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        
        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y
        
        # check collision with floor
        if self.rect.bottom + dy > 609:
            dy = 609 - self.rect.bottom
            self.in_air = False      # check if allowed to jump
        
        self.rect.x += dx
        self.rect.y += dy
        
        def shoot(self):
            if self.shoot_cooldown == 0 and self.ammo > 0:
                self.shoot_cooldown = 20
                bullet = bullet(self.rect.centerx + (0.75 * self.rect.width * self.direction), self.rect.centery, self.direction)
                bullet_group.add(bullet)
                self.ammo -= 1