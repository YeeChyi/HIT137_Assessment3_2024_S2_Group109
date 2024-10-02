import pygame
from pygame.locals import *

pygame.init()

# screen view
screen_width = 500
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tank vs Zombie')

# to run game continuously
run = True
while run:

# to quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
