import pygame
import os
import random

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
TILE_SIZE = 40

# define player moves
moving_left = False
moving_right = False 
shoot = False

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
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))

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

        # check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
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

# creating items
class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
         pygame.sprite.Sprite.__init__(self)
         self.item_type = item_type
         self.image = item_boxes[self.item_type]
         self.rect = self.image.get_rect()
         self.rect.midtop = (x + TILE_SIZE//2, y+(TILE_SIZE-self.image.get_height()))

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

        # check collision with character
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
                
        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alive:
                enemy.health -= 25
                self.kill()

# create sprite groups
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()

# temporary - create item boxes
item_box = ItemBox('Health', 100,260)
item_box_group.add(item_box)
item_box = ItemBox('Ammo', 400,260)
item_box_group.add(item_box)


player = Penguin('player', 200, 200, 1.65, 5, 20)
health_bar = HealthBar(10,10,player.health, player.health)


enemy1 = Penguin('enemy', 400, 200, 1.65, 2, 20)
enemy2 = Penguin('enemy', 300, 200, 1.65, 2, 20)
enemy_group.add(enemy1)
enemy_group.add(enemy2)

run = True
while run:

    clock.tick(FPS)

    draw_bg()

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
