import pygame
pygame.init()
import button

clock = pygame.time.Clock()
FPS = 60

# game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('ENVIRONMENT')

# define variables
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT//ROWS
TILE_TYPES = 14
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

# load images for background
mountain_img = pygame.image.load('img/background/MTN.png').convert_alpha()
tree_img = pygame.image.load('img/background/bigtrees.png').convert_alpha()
clouds_img = pygame.image.load('img/background/clouds.png').convert_alpha()
sky_img = pygame.image.load('img/background/sky.png').convert_alpha()

# images for tiles
img_list =[]
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/tiles/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)


# define colors
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

# empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

# create a ground
for tile in range(0, MAX_COLS):
    world_data[ROWS-1][tile] = 0


# drawing background
def draw_bg():
    screen.fill(BLUE)
    width = sky_img.get_width()
    for x in range(4):
        screen.blit(sky_img, ((x * width) - scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 50))
        screen.blit(tree_img, ((x * width) - scroll * 0.7, SCREEN_HEIGHT - tree_img.get_height() - 5))
        screen.blit(clouds_img, ((x * width) - scroll * 0.8, SCREEN_HEIGHT - clouds_img.get_height() - 70))

# for grid
def draw_grid():
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0),(c*TILE_SIZE - scroll, SCREEN_HEIGHT))
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE),(SCREEN_WIDTH, c*TILE_SIZE))

# drawing the environment
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE-scroll, y * TILE_SIZE))


# create buttons
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0


run = True
while run:
    clock.tick(FPS)
    draw_bg()
    draw_grid()
    draw_world()

    # tile panel
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH,0,SIDE_MARGIN, SCREEN_HEIGHT))

    # choose tile
    button_count = 0
    for button_count, i in enumerate (button_list):
        if i.draw(screen):
            current_tile = button_count

    # highlight tile
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)            

    # scroll map
    if scroll_left and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right:
        scroll += 5 * scroll_speed

# add new tiles to background  by using mouse
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    # check for coordinates within tile area
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        if pygame.mouse.get_pressed()[0] == 1: # to change tile view
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile

        if pygame.mouse.get_pressed()[2] == 1: # to erase using right click
                world_data[y][x] = -1 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # keyboard press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 0.5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1

    pygame.display.update()

pygame.quit()
