import pygame
pygame.init()

# game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT+LOWER_MARGIN))
pygame.display.set_caption('ENVIRONMENT')

# load images 
snow_img = pygame.image.load('img/background/clouds.png').convert_alpha
mountain_img = pygame.image.load('img/background/MTN.png').convert_alpha
sky_img = pygame.image.load('img/background/sky.png').convert_alpha

# drawing background
def draw_bg():
    screen.blit(sky_img, (0,0))


run = True
while run:

    draw_bg()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    pygame.display.update()

pygame.quit()