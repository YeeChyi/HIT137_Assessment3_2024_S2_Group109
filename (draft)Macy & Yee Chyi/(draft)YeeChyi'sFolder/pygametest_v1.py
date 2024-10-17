import pygame
import random

# initialise pygame
pygame.init()

# constants
screen_width = 800
screen_height = 600
fps = 60
gravity = 1

# colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# screen setup
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tank Battle Game")

# clock to control frame rate
clock = pygame.time.Clock()

# font
font = pygame.font.Font(None, 36)

# load images (for player, enemy, collectible, etc.)
player_image = pygame.Surface((50, 30))
player_image.fill(green)

enemy_image = pygame.Surface((50, 30))
enemy_image.fill(red)

collectible_image = pygame.Surface((20, 20))
collectible_image.fill(blue)

class projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
    
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > screen_width:
            self.kill()


# player class
class Player(pygame.sprite.Sprite):
    def __init__(self, all_sprites, projectiles):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = screen_height - 70
        self.speed = 5
        self.jump_strength = -15
        self.vel_y = 0
        self.on_ground = True
        self.health = 100
        self.lives = 3
        self.all_sprites = all_sprites
        self.projectiles = projectiles
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed       # moving to left means -
        if keys[pygame.K_RIGHT]:
            self.rect.y += self.speed       # moving to right means +
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False
        
        # gravity and jump mechanics
        self.vel_y += gravity
        self.rect.y += self.vel_y
        if self.rect.y >= screen_height - 70:
            self.rect.y = screen_height - 70
            self.vel_y = 0
            self.on_ground = True
    
    def shoot(self):
        projectile = projectile(self.rect.right, self.rect.centery)
        self.all_sprites.add(projectile)
        self.projectiles.add(projectile)
    
    
# enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3
        self.health = 50
    
    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
            

# collectible class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = collectible_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def apply_effect(self, player):
        # randomly choose between health boost or extra life
        effect = random.choice(["health", "life"])
        if effect == "health":
            player.health = min(player.health + 20, 100)
        else:
            player.lives += 1
        self.kill()
        

# health bar rendering
def draw_health_bar(surface, x, y, percentage):
    bar_length = 100
    bar_height = 10
    fill = (percentage / 100) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, green, fill_rect)
    pygame.draw.rect(surface, white, outline_rect, 2)


# game over screen
def game_over_screen():
    screen.fill(black)
    game_over_text = font.render("GAME OVER - PRESS R TO RESTART", True, white)
    screen.blit(game_over_text, (screen_width // 4, screen_height // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                waiting = False

# game loop
def game():
    all_sprites = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()
    
    player = Player(all_sprites, projectiles)
    all_sprites.add(player)
    
    score = 0
    level = 1
    
    
    # spawn enemies and collectibles
    def spawn_enemies():
        enemy = Enemy(screen_width, screen_height - 70)
        all_sprites.add(enemy)
        enemies.add(enemy)
    
    def spawn_collectibles():
        collectible = Collectible(random.randint(0, screen_width - 20), screen_height - 70)
        all_sprites.add(collectible)
        collectibles.add(collectible)
        
    
    # game loop variables 
    running = True
    game_over = False
    spawn_timer = 0
    
    while running:
        clock.tick(fps)
        
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    player.shoot()
        
        # game over check
        if player.lives <= 0:
            game_over = True
        
        # update
        if not game_over:
            all_sprites.update()
            
            # collision checks
            for enemy in pygame.sprite.groupcollide(enemies, projectiles, True, True):
                score += 100
            
            for collectible in pygame.sprite.spritecollide(player, collectibles, False):
                collectible.apply_effect(player)
                
            if pygame.sprite.spritecollideany(player, enemies):
                player.health -= 10
                if player.health <= 0:
                    player.lives -= 1
                    player.health = 100
                    
            # spawn new enemies and collectibles periodically
            spawn_timer += 1
            if spawn_timer > 100:
                spawn_enemies()
                spawn_collectibles()
                spawn_timer = 0
            
            # draw
            screen.fill(black)
            all_sprites.draw(screen)
            draw_health_bar(screen, 10, 10, player.health)
            
            # score display
            score_text = font.render(f"Score: {score}", True, white)
            screen.blit(score_text, (10, 50))
            
            # level display
            level_text = font.render(f"Level: {level}", True, white)
            screen.blit(level_text, (screen_width - 150, 10))
            
        else:
            game_over_screen()
        
        pygame.display.flip()

game()
pygame.quit()