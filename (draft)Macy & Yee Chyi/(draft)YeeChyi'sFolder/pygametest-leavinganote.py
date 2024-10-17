import pygame

# initialise pygame
pygame.init()

# setup the display
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Hello Pygame!")

# set a colour
blue = (0, 0, 255)
white = (255, 255, 255)

# setup fonts
font = pygame.font.Font(None, 74)  #none for the default font, size 74
text = font.render("Hello, Pygame!", True, white)

# get the rectangle of the text for positioning
text_rect = text.get_rect(center=(320, 240))  # centered on the screen

# main loop
running = True
while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the screen with blue colour
    screen.fill(blue)
    
    # draw the text on the screen
    screen.blit(text, text_rect)
    
    # update the display
    pygame.display.flip()
    
# quit pygame
pygame.quit()