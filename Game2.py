# Trial code by Macy

import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Side-Scroller with Levels and Bosses")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Global variables
clock = pygame.time.Clock()
gravity = 0.8
game_over = False
font = pygame.font.SysFont(None, 36)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = HEIGHT - self.rect.height
        self.speed = 5
        self.jump_speed = -15
        self.vel_y = 0
        self.jumping = False
        self.shoot_cooldown = 0
        self.health = 100
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        # Movement left and right
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Jumping
        if keys[pygame.K_SPACE] and not self.jumping:
            self.jumping = True
            self.vel_y = self.jump_speed

        # Apply gravity
        self.vel_y += gravity
        self.rect.y += self.vel_y

        # Check ground collision
        if self.rect.y >= HEIGHT - self.rect.height:
            self.rect.y = HEIGHT - self.rect.height
            self.jumping = False

        # Shooting
        if keys[pygame.K_s] and self.shoot_cooldown == 0:
            projectile = Projectile(self.rect.centerx, self.rect.centery)
            projectiles.add(projectile)
            self.shoot_cooldown = 20

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.lives -= 1
            self.health = 100

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > WIDTH:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, is_boss=False):
        super().__init__()
        self.image = pygame.Surface((50, 50) if not is_boss else (100, 100))
        self.image.fill(RED if not is_boss else YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2 if not is_boss else 1
        self.health = 50 if not is_boss else 200
        self.is_boss = is_boss

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -self.rect.width:
            self.rect.x = WIDTH + random.randint(0, 100)
            self.rect.y = random.randint(HEIGHT - 80, HEIGHT - 40)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

# Collectible class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, type="health"):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.type = type
        if self.type == "health":
            self.image.fill(BLUE)
        elif self.type == "life":
            self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def apply_effect(self, player):
        if self.type == "health":
            player.health += 20
            if player.health > 100:
                player.health = 100
        elif self.type == "life":
            player.lives += 1

# GameManager class to handle levels and score
class GameManager:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.enemies = 5
        self.boss_fight = False

    def increase_score(self, points):
        self.score += points

    def next_level(self):
        self.level += 1
        if self.level > 3:
            self.level = 1  # Restart the game after level 3 for simplicity
        self.enemies += 2

    def spawn_boss(self):
        boss = Enemy(WIDTH + 200, HEIGHT - 100, is_boss=True)
        enemies.add(boss)
        self.boss_fight = True

# Game over screen
def game_over_screen():
    screen.fill(WHITE)
    over_text = font.render("Game Over! Press R to Restart", True, BLACK)
    screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - over_text.get_height() // 2))
    pygame.display.flip()

# Sprite groups
player_group = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

# Create player
player = Player()
player_group.add(player)

# Spawn enemies
for i in range(5):
    enemy = Enemy(WIDTH + i * 100, HEIGHT - 40)
    enemies.add(enemy)

# Spawn collectibles
for i in range(3):
    collectible = Collectible(random.randint(200, WIDTH), HEIGHT - 40, type=random.choice(["health", "life"]))
    collectibles.add(collectible)

# Game Manager instance
game_manager = GameManager()

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update sprites
    if not game_over:
        player_group.update()
        projectiles.update()
        enemies.update()
        collectibles.update()

        # Check collisions between player and enemies
        hit_enemies = pygame.sprite.spritecollide(player, enemies, False)
        for enemy in hit_enemies:
            player.take_damage(10)
            if player.lives == 0:
                game_over = True

        # Check collisions between projectiles and enemies
        hit = pygame.sprite.groupcollide(projectiles, enemies, True, False)
        for projectile, hit_enemies in hit.items():
            for enemy in hit_enemies:
                enemy.take_damage(25)
                if enemy.is_boss and enemy.health <= 0:
                    game_manager.next_level()
                    game_manager.boss_fight = False
                game_manager.increase_score(10)

        # Check collisions between player and collectibles
        collected = pygame.sprite.spritecollide(player, collectibles, True)
        for item in collected:
            item.apply_effect(player)

        # Draw everything
        player_group.draw(screen)
        projectiles.draw(screen)
        enemies.draw(screen)
        collectibles.draw(screen)

        # Display score, health, and lives
        score_text = font.render(f"Score: {game_manager.score}", True, BLACK)
        health_text = font.render(f"Health: {player.health}", True, BLACK)
        lives_text = font.render(f"Lives: {player.lives}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (10, 50))
        screen.blit(lives_text, (10, 90))

        # Level progression and boss spawning
        if game_manager.score >= 50 * game_manager.level and not game_manager.boss_fight:
            game_manager.spawn_boss()

        # Update screen
        pygame.display.flip()

    else:
        game_over_screen()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_manager = GameManager()
            player = Player()
            player_group.empty()
            player_group.add(player)
            enemies.empty()
            for i in range(5):
                enemy = Enemy(WIDTH + i * 100, HEIGHT - 40)
                enemies.add(enemy)
            collectibles.empty()
            for i in range(3):
                collectible = Collectible(random.randint(200, WIDTH), HEIGHT - 40, type=random.choice(["health", "life"]))
                collectibles.add(collectible)
            game_over = False

    # Frame rate
    clock.tick(60)

pygame.quit()
