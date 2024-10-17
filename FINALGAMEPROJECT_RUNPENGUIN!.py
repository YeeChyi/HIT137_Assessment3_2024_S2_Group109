import pygame
import os
import random
import csv
import button

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('RUN PENGUIN, RUN!')

# framerate
clock = pygame.time.Clock()
FPS = 60

# game variables
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT//ROWS
TILE_TYPES = 14
MAX_LEVELS = 3
scroll = 0
bg_scroll = 0
level = 1
start_game = False

# define player moves
moving_left = False
moving_right = False 
shoot = False

# load images
start_img = pygame.image.load('img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()

# background
bigtrees_img = pygame.image.load('img/background/bigtrees.png').convert_alpha()
clouds_img = pygame.image.load('img/background/clouds.png').convert_alpha()
mountain_img = pygame.image.load('img/background/MTN.png').convert_alpha()
sky_img = pygame.image.load('img/background/sky.png').convert_alpha()

# store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/tiles/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

# bullet image
bullet_img = pygame.image.load('img/icon/bullet.png').convert_alpha()

# pick up items
health_box_img = pygame.image.load('img/icon/life.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icon/ammo_box.png').convert_alpha()

item_boxes = {
    'Health' : health_box_img,
    'Ammo' : ammo_box_img
}

# to add colors
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255,0)
BLACK = (0,0,0)

font = pygame.font.SysFont('Futura', 30)

# display info
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))


def draw_bg():
    screen.fill(BG)
    width = sky_img.get_width()
    for x in range(7):
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 50))
        screen.blit(bigtrees_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - bigtrees_img.get_height() - 5))
        screen.blit(clouds_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - clouds_img.get_height() - 70))

# to reset level
def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    item_box_group.empty()
    water_group.empty()
    exit_group.empty()

# empty tile list
    data = []
    for row in range (ROWS):
        r = [-1] * COLS
        data.append(r)
    return data

score = 0

# creating a character
class Penguin(
    pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True  # player is alive
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0 
        self.health = 1000
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # idle
        self.update_time = pygame.time.get_ticks()

        # for AI movements
        self.move_counter = 0
        self.vision = pygame.Rect(0,0,150,20)
        self.idling = True
        self.idling_counter = 0 

        # player movements - UPDATE DEATH
        animation_types = ['idle', 'walking', 'jumping', 'death']
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (70, 70))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        # reset movement variables
        scroll = 0
        dx = 0
        dy = 1    # dy is =1 so that player can move forward and backward smoothly
        
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


        # COLLISION WITH WATER???
        if pygame.sprite.spritecollide(self, water_group,False):
            self.health = 0
        
        # COLLISION WITH EXIT???
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group,False):
            level_complete = True


        # FALL OFF MAP???
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0


        # check for collision
        for tile in world.obstacle_list:
            #check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # ai has hit a wall turn around
            if self.char_type == 'enemy':
                self.direction *= -1
                self.move_counter = 0
            #check collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.topa
                # check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom       

        # update rectangle
        self.rect.x += dx
        self.rect.y += dy
        
        # update scroll based on player position
        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                scroll = -dx
                
        return scroll, level_complete
                

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.width * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.ammo -= 1

# enemy movement
    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 50) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 50
            # check if enemy is near player
            if self.vision.colliderect(player.rect):
                self.update_action(0) # stop running 
                self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1) # walk
                    self.move_counter += 1

                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    pygame.draw.rect(screen, RED, self.vision)

                    if self.move_counter > TILE_SIZE:
                        self.direction  *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
        
        # scroll
        self.rect.x += scroll   
        
    
    def update_score():
        global score
        score += 100
    
    update_score()

    
            
    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 3:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else: 
                    self.frame_index = 0
                
    # to check if action is different from previous one
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0  # update settings
            self.update_time = pygame.time.get_ticks()

    # life 
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) #REMOVE IF NOT WORKING
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    
                    if tile >= 0 and tile <= 6:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 7 and tile <= 8:
                    #     pass # DIE?!
                    # elif tile == 8:
                         water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                         water_group.add(water)
                         
                    elif tile == 9: # create enemy
                            enemy = Penguin('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 20)
                            enemy_group.add(enemy)

                    elif tile == 10: # create a player
                        player = Penguin('player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5, 20)
                        health_bar = HealthBar(10,10,player.health, player.health)

                    elif tile == 11: # create ammo box
                        item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)

                    elif tile == 12: # health
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)

                    elif tile == 13: # new level
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)

        return player, health_bar
    
    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += scroll
            screen.blit(tile[0], tile[1])

class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
         pygame.sprite.Sprite.__init__(self)
         self.image = img
         self.rect = self.image.get_rect()
         self.rect.midtop = (x + TILE_SIZE//2, y + (TILE_SIZE - self.image.get_height()))
    
    def update(self):
        self.rect.x += scroll

class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
         pygame.sprite.Sprite.__init__(self)
         self.image = img
         self.rect = self.image.get_rect()
         self.rect.midtop = (x + TILE_SIZE//2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += scroll


# creating items
class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
         pygame.sprite.Sprite.__init__(self)
         self.item_type = item_type
         self.image = item_boxes[self.item_type]
         self.rect = self.image.get_rect()
         self.rect.midtop = (x + TILE_SIZE//2, y+(TILE_SIZE - self.image.get_height()))

    def update(self):
        # scroll
        self.rect.x += scroll
        # check if player has picked up items
        if pygame.sprite.collide_rect(self, player):
            # check item type
            if self.item_type == 'Health':
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo += 15
            # delete after picking up
            self.kill()

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
    
    def draw(self, health):
        # update with new health
        self.health = health
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x-2, self.y-2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))

# creating bullets
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10 
        self.image = bullet_img # USE IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction

    def update(self):
        self.rect.x += (self.direction * self.speed) + scroll
        # check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
            
        # check for collision with level and walls
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        # check collision with character
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 1000
                    self.kill()

        
# buttons
start_button = button.Button(SCREEN_WIDTH//2 - 130, SCREEN_HEIGHT//2 - 150, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH//2 - 110, SCREEN_HEIGHT//2 + 50, exit_img, 1)
restart_button = button.Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50, restart_img, 1)


# create sprite groups
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()


# empty tile list
world_data = []
for row in range (ROWS):
    r = [-1] * COLS
    world_data.append(r)

# to open the game levels
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
player, health_bar = world.process_data(world_data)

pygame.font.init()
font = pygame.font.SysFont(None, 30)

def draw_score(screen, score):
    score_text = font.render(f'Score: {score}', True, (255,255,255))
    screen.blit(score_text, (10, 10))

run = True
while run:

    clock.tick(FPS)

    if start_game == False:
        # menu
        screen.fill(BG)
        if start_button.draw(screen):
            start_game = True
        if exit_button.draw(screen):
            run = False

    else:
        draw_bg()
        world.draw()

        # show health
        health_bar.draw(player.health)

        # change the font size for the 'Ammo:' text
        font = pygame.font.Font(None, 25)
        # show ammo
        draw_text('AMMO:', font, WHITE, 10, 35)
        for x in range(player.ammo):
            screen.blit(bullet_img, (90 + (x*10),40))

        player.update()

        for enemy in enemy_group:
            enemy.ai()
            enemy.update()
            enemy.draw()
        
        # update and draw groups
        bullet_group.update()
        item_box_group.update()
        water_group.update()
        exit_group.update()
        bullet_group.draw(screen)
        item_box_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)

        # to check player actions 
        if player.alive:
            if shoot:
                player.shoot()
            if player.in_air:
                player.update_action(2)  # jump
            elif moving_left or moving_right:
                player.update_action(1)  # run
            else:
                player.update_action(0)  # idle
            scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= scroll
            if level_complete:
                level += 1 
                bg_scroll = 0
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter = ',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                world = World()
                player, health_bar = world.process_data(world_data)


        else:
            scroll = 0
            # display "Game Over!" on the screen
            font = pygame.font.SysFont('Futura', 50)
            game_over_text = font.render('Uh-oh, Game Over!', True, (255, 0, 0))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3 - game_over_text.get_height() // 2))
     
            if restart_button.draw(screen):
                bg_scroll = 0
                world_data = reset_level()
                with open(f'level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter = ',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                player, health_bar = world.process_data(world_data)


    for event in pygame.event.get():
        # to quit game
        if event.type == pygame.QUIT:
            run = False

        # keyboard functions when pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # move left
                moving_left = True
            if event.key == pygame.K_RIGHT:  # move right
                moving_right = True
            if event.key == pygame.K_SPACE:  # to shoot
                shoot = True
            if event.key == pygame.K_UP and player.alive:  # jump 
                player.jump = True    
            if event.key == pygame.K_ESCAPE:
                run = False
                
        # keyboard functions when not pressed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
    
    draw_score(screen, score)
    
    player.draw()
    pygame.display.update()

pygame.quit()
