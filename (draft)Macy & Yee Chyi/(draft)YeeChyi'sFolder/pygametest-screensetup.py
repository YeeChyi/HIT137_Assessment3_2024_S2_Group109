import pygame

# initialise pygame
pygame.init()

# setup the display
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Hello Pygame!!")

# set a colour
blue = (0, 0, 255) # RGB value

# main loop
running = True
while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # fill the screen with the blue colour
    screen.fill(blue)
    
    # update the display
    pygame.display.flip()
    
# quit pygame
pygame.quit()