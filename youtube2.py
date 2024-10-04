import pygame

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


# player moves
moving_left = False
moving_right = False 

# to add colors
BG = (144, 201, 120)
RED = (255, 0, 0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))
    

# creating a character
class Penguin(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True # player is alive
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.flip = False

        # for movement of player
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 # idle
        self.update_time = pygame.time.get_ticks()
    
    
        # IDLE 
        temp_list = []
        img = pygame.image.load('0.png')
        img = pygame.transform.scale(img, (70, 70))
        temp_list.append(img)
        self.animation_list.append(temp_list)

        # RUN ANIMATION
        temp_list = []
        for i in range(1, 4):
            img = pygame.image.load(f'img/{self.char_type}/walking/{i}.png')
            img = pygame.transform.scale(img, (70, 70))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

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
        if self.jump == True:
            self.vel_y = -11 
            self.jump = False
            
		 # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        self.rect.x += dx
        self.rect.y += dy


	# check collision with floor
    if self.rect.bottom + dy > 300:
        dy = 300 - self.rect.bottom



        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
                
	# to check if action is different from previous one
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0  # update settings
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

player = Penguin('player', 200, 200, 3, 5)

run = True
while run:

    clock.tick(FPS)

    draw_bg()
    player.update_animation()
    
# to check player actions to walk
if player.alive:
    if moving_left or moving_right:
        player.update_action(1)  # walk
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
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and player.alive: # jump 
                player.jump = True    
            if event.key == pygame.K_ESCAPE:
                run = False
                
        # keyboard functions when not pressed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()

pygame.quit()