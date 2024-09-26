import pygame
import random

# Initialize Pygame
pygame.init()

# Game Settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side-Scrolling Game")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game Variables
GRAVITY = 1
PLAYER_SPEED = 5
JUMP_FORCE = 15
PROJECTILE_SPEED = 10

# Fonts
font = pygame.font.Font(None, 36)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))  # Blue player
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT - 100)
        self.vel_y = 0
        self.jump = False
        self.health = 100
        self.lives = 3

    def update(self, keys):
        self.vel_y += GRAVITY  # Gravity effect

        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        # Jumping
        if not self.jump and keys[pygame.K_SPACE]:
            self.jump = True
            self.vel_y = -JUMP_FORCE

        # Vertical movement
        self.rect.y += self.vel_y

        # Prevent falling through the ground
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = 0
            self.jump = False

    def shoot(self):
        # Create a projectile object and return it to the game loop
        return Projectile(self.rect.right, self.rect.centery)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 0, 0))  # Red projectile
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = PROJECTILE_SPEED

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > WIDTH:
            self.kill()  # Remove if it goes off-screen
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))  # Red enemy
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = random.choice([-2, -3])

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0:  # Reset the enemy position if off-screen
            self.rect.x = WIDTH

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type  # 'health' or 'life'
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))  # Green collectible
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def apply_effect(self, player):
        if self.type == 'health':
            player.health += 20  # Health boost
        elif self.type == 'life':
            player.lives += 1  # Extra life
        self.kill()  # Remove collectible after collection

class Level:
    def __init__(self, player):
        self.player = player
        self.enemies = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()

        # Add platforms, enemies, collectibles for the current level
        self.create_level()

    def create_level(self):
        # Add enemies and collectibles at specific positions
        for i in range(5):  # Adding enemies
            enemy = Enemy(WIDTH + i * 200, HEIGHT - 60)
            self.enemies.add(enemy)
        # Add collectibles
        self.collectibles.add(Collectible(400, HEIGHT - 50, 'health'))

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
projectiles = pygame.sprite.Group()

# Main game loop
running = True
while running:
    clock.tick(60)  # 60 FPS

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:  # Press 'S' to shoot
            projectile = player.shoot()
            all_sprites.add(projectile)
            projectiles.add(projectile)

    # Update
    keys = pygame.key.get_pressed()
    player.update(keys)
    projectiles.update()

    # Draw
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Display health and lives
    health_text = font.render(f'Health: {player.health}', True, BLACK)
    lives_text = font.render(f'Lives: {player.lives}', True, BLACK)
    screen.blit(health_text, (10, 10))
    screen.blit(lives_text, (10, 40))

    pygame.display.flip()

pygame.quit()

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, player):
        x = -player.rect.centerx + int(WIDTH / 2)
        y = -player.rect.centery + int(HEIGHT / 2)
        self.camera = pygame.Rect(x, y, self.width, self.height)