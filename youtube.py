import pygame
from pygame.locals import *
    
pygame.init()

# screen view
screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('The Rise of the Zombies')

# define game variables
tile_size = 200

#load images
sun_img = pygame.image.load('night.jpg')
sun_img = pygame.transform.scale(sun_img, (screen_width, screen_height))

def draw_grid():
    for line in range(0,6):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

# to run game continuously
run = True
while run:

    screen.blit(sun_img, (0,0))

    draw_grid()

# to quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
