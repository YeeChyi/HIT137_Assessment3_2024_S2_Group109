import pygame
from pygame.locals import *

pygame.init()

# screen view
screen_width = 500
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('The Rise of the Zombies')

#load images
sun_img = pygame.image.load('night.jpg')
sun_img = pygame.transform.scale(sun_img, (screen_width, screen_height))

# to run game continuously
run = True
while run:

    screen.blit(sun_img, (0,0))

# to quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
