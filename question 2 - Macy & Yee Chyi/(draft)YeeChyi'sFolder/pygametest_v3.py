import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank Battle Game")

# Clock to control frame rate
clock = pygame.time.Clock()

# Font
font = pygame.font.Font(None, 36)

# Load images (for player, enemy, collectible, etc.)
player_image = pygame.Surface((50, 30))
player_image.fill(GREEN)

enemy_image = pygame.Surface((50, 30))
enemy_image.fill(RED)

collectible_image = pygame.Surface((20, 20))
collectible_image.fill(BLUE)


# Projectile Class (Move this above the Player class)
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > SCREEN_WIDTH:
            self.kill()


# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, all_sprites, projectiles):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 70
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
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False

        # Gravity and jump mechanics
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        if self.rect.y >= SCREEN_HEIGHT - 70:
            self.rect.y = SCREEN_HEIGHT - 70
            self.vel_y = 0
            self.on_ground = True

    def shoot(self):
        projectile = Projectile(self.rect.right, self.rect.centery)
        self.all_sprites.add(projectile)
        self.projectiles.add(projectile)


# Enemy Class
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


# Collectible Class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = collectible_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def apply_effect(self, player):
        # Randomly choose between health boost or extra life
        effect = random.choice(["health", "life"])
        if effect == "health":
            player.health = min(player.health + 20, 100)
        else:
            player.lives += 1
        self.kill()


# Health bar rendering
def draw_health_bar(surface, x, y, percentage):
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)


# Game Over Screen
def game_over_screen():
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER - Press R to Restart", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                waiting = False


# Game Loop
def game():
    all_sprites = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()

    player = Player(all_sprites, projectiles)
    all_sprites.add(player)

    score = 0
    level = 1
    level_threshold = 500

    # Spawn enemies and collectibles
    def spawn_enemy():
        enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT - 70)
        all_sprites.add(enemy)
        enemies.add(enemy)

    def spawn_collectible():
        collectible = Collectible(random.randint(0, SCREEN_WIDTH - 20), SCREEN_HEIGHT - 70)
        all_sprites.add(collectible)
        collectibles.add(collectible)

    # Game loop variables
    running = True
    game_over = False
    spawn_timer = 0

    while running:
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    player.shoot()

        # Game Over Check
        if player.lives <= 0:
            game_over = True

        # Update
        if not game_over:
            player.move()
            all_sprites.update()

            # Collision checks
            for enemy in pygame.sprite.groupcollide(enemies, projectiles, True, True):
                score += 100

            for collectible in pygame.sprite.spritecollide(player, collectibles, False):
                collectible.apply_effect(player)

            if pygame.sprite.spritecollideany(player, enemies):
                player.health -= 10
                if player.health <= 0:
                    player.lives -= 1
                    player.health = 100

            # Spawn new enemies and collectibles periodically
            spawn_timer += 1
            if spawn_timer > 100:
                spawn_enemy()
                spawn_collectible()
                spawn_timer = 0

            # Draw
            screen.fill(BLACK)
            all_sprites.draw(screen)
            draw_health_bar(screen, 10, 10, player.health)

            # Score display
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 50))

            # Level display
            level_text = font.render(f"Level: {level}", True, WHITE)
            screen.blit(level_text, (SCREEN_WIDTH - 150, 10))

        else:
            game_over_screen()

        pygame.display.flip()


game()
pygame.quit()
