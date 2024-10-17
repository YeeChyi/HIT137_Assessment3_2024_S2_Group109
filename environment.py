import pygame
import button
import csv

pygame.init()

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
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 14
level = 0  # SAFETY CHECK
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
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/tiles/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (40, 40))
    img_list.append(img)
    

save_img = pygame.image.load('img/save_btn.png').convert_alpha() 
load_img = pygame.image.load('img/load_btn.png').convert_alpha() 
save_img = pygame.transform.scale(save_img, (100, 50)) 
load_img = pygame.transform.scale(load_img, (100, 50))

# define colors
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

# font for level display
font = pygame.font.SysFont('Futura', 30)

# empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

# create a ground
for tile in range(0, MAX_COLS):
    world_data[ROWS - 1][tile] = 0


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# drawing background
def draw_bg():
    screen.fill(BLUE)
    width = sky_img.get_width()
    for x in range(7):
        screen.blit(sky_img, ((x * width) - scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 50))
        screen.blit(tree_img, ((x * width) - scroll * 0.7, SCREEN_HEIGHT - tree_img.get_height() - 5))
        screen.blit(clouds_img, ((x * width) - scroll * 0.8, SCREEN_HEIGHT - clouds_img.get_height() - 70))


# for grid
def draw_grid():
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))


# drawing the environment
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))


# create buttons
save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)

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

# Main game loop
run = True
while run:
    clock.tick(FPS)
    draw_bg()
    draw_grid()
    draw_world()

    # display level and instructions
    draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text('Press UP or DOWN to change level', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

    # save and load functionality
    if save_button.draw(screen):
        with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in world_data:
                writer.writerow(row)

    if load_button.draw(screen):
        scroll = 0  # to scroll back to the start of level
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

    # tile panel
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    # choose tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count
    # highlight the selected tile
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    # scroll map
    if scroll_left and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll += 5 * scroll_speed

    # add new tiles to background using mouse
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    # check if within tile area
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        if pygame.mouse.get_pressed()[0] == 1:  # left-click to place tile
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:  # right-click to erase tile
            world_data[y][x] = -1

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # keyboard press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
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
