import pygame
import os
import random
import csv

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('CLUB PENGUIN')

# framerate
clock = pygame.time.Clock()
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

# Load bullet image
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
        self.health = 100
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
        self.idling = False
        self.idling_counter = 0 

        # player movements - UPDATE DEATH
        animation_types = ['idle', 'walking', 'jumping', 'death'] # ADD DEATH LATER
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

        # check for collision
        for tile in world.obstacle_list:
            #check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            #check collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #  check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
            
        if self.rect.bottom + dy > 609:
            dy = 609 - self.rect.bottom
            self.in_air = False  # check if allowed to jump        

        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.width * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.ammo -= 1

# enemy movement
    def ai(self):
        if self.alive and player.alive:
            if self.idling ==False and random.randint(1, 200) == 1:
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
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile>= 0 and tile <= 6:
                        self.obstacle_list.append(tile_data)

                    elif tile >= 7 and tile <= 10:
                        pass # die

                    elif tile >= 11 and tile <= 12:
                         water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                         water_group.add(water)
    
                    elif tile == 14: # create a player
                        player = Penguin('player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5, 20)
                        health_bar = HealthBar(10,10,player.health, player.health)

                    elif tile == 13: # create enemy
                        enemy = Penguin('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 20)
                        enemy_group.add(enemy)

                    elif tile == 15: # create ammo box
                        item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)

                    elif tile == 16: # health
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)

                    elif tile == 17: # new level
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)

        return player, health_bar
    
    def draw(self):
        for tile in self.obstacle_list:
            screen.blit(tile[0], tile[1])

class Water(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
         pygame.sprite.Sprite.__init__(self)
         self.image = img
         self.rect = self.image.get_rect()
         self.rect.midtop = (x + TILE_SIZE//2, y + (TILE_SIZE - self.image.get_height()))

class Exit(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
         pygame.sprite.Sprite.__init__(self)
         self.image = img
         self.rect = self.image.get_rect()
         self.rect.midtop = (x + TILE_SIZE//2, (TILE_SIZE - self.image.get_height()))


# creating items
class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
         pygame.sprite.Sprite.__init__(self)
         self.item_type = item_type
         self.image = item_boxes[self.item_type]
         self.rect = self.image.get_rect()
         self.rect.midtop = (x + TILE_SIZE//2, y+(TILE_SIZE - self.image.get_height()))

    def update(self):
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
    def __init__(self, x,y, health, max_health):
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
        self.direction = direction

    def update(self):
        self.rect.x += (self.direction * self.speed)
        # check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        # check for collision with level
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
                    enemy.health -= 25
                    self.kill()

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


run = True
while run:

    clock.tick(FPS)

    draw_bg()
    world.draw()

    # show health
    health_bar.draw(player.health)

    # show ammo
    draw_text('AMMO:', font, WHITE, 10, 35)
    for x in range(player.ammo):
        screen.blit(bullet_img, (90 + (x*10),40)) # change pictures of ammo

    player.update()

    for enemy in enemy_group:
        enemy.ai()
        enemy.update()
        enemy.draw()
    
    # update and draw groups
    bullet_group.update()
    bullet_group.draw(screen)
    item_box_group.update()
    item_box_group.draw(screen)
    water_group.update()
    water_group.draw(screen)
    exit_group.update()
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
        player.move(moving_left, moving_right)
    
    player.draw()

    for event in pygame.event.get():
        # to quit game
        if event.type == pygame.QUIT:
            run = False

        # keyboard functions when pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:  # move left
                moving_left = True
            if event.key == pygame.K_d:  # move right
                moving_right = True
            if event.key == pygame.K_s:  # to shoot
                shoot = True
            if event.key == pygame.K_w and player.alive:  # jump 
                player.jump = True    
            if event.key == pygame.K_ESCAPE:
                run = False
                
        # keyboard functions when not pressed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_s:
                shoot = False

    pygame.display.update()

pygame.quit()
