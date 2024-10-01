# Trial code by Macy

import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5
        self.jump_speed = -15
        self.gravity = 1
        self.velocity_y = 0
        self.health = 100
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE]:
            self.jump()

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0

    def jump(self):
        if self.rect.bottom == SCREEN_HEIGHT:
            self.velocity_y = self.jump_speed

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > SCREEN_WIDTH:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# Collectible class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# Game setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Side-Scrolling Game")

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

projectiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                projectile = Projectile(player.rect.centerx, player.rect.centery)
                all_sprites.add(projectile)
                projectiles.add(projectile)

    all_sprites.update()

    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

    pygame.time.delay(30)

pygame.quit()
