import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
INITIAL_HEALTH = 100
INITIAL_LIVES = 3
COLLECTIBLE_HEALTH_BOOST = 20

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Side-Scrolling Tank Game")
clock = pygame.time.Clock()

# Load assets (replace with actual image paths)
player_image = pygame.image.load("tank.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (70, 70))  # Scale to fit
enemy_image = pygame.image.load("ghost.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (50, 50))  # Scale to fit

# Font for displaying text
font = pygame.font.Font(None, 36)

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, all_sprites, projectiles):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 70
        self.speed = 5
        self.vel_y = 0
        self.on_ground = True
        self.health = INITIAL_HEALTH
        self.lives = INITIAL_LIVES
        self.all_sprites = all_sprites
        self.projectiles = projectiles

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -15  # Jump strength
            self.on_ground = False

        # Gravity
        self.vel_y += 1  # Gravity
        self.rect.y += self.vel_y
        if self.rect.y >= SCREEN_HEIGHT - 70:
            self.rect.y = SCREEN_HEIGHT - 70
            self.vel_y = 0
            self.on_ground = True

    def shoot(self):
        projectile = Projectile(self.rect.right, self.rect.centery)
        self.all_sprites.add(projectile)
        self.projectiles.add(projectile)

# Projectile Class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > SCREEN_WIDTH:
            self.kill()

# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -self.rect.width:
            self.kill()  # Remove enemy if it goes off-screen

# Collectible Class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))  # Green collectible
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def apply_effect(self, player):
        player.health = min(player.health + COLLECTIBLE_HEALTH_BOOST, INITIAL_HEALTH)  # Health boost

# Function to spawn enemies
def spawn_enemy(level):
    enemy = Enemy(SCREEN_WIDTH + 50, SCREEN_HEIGHT - 70)
    enemies.add(enemy)
    all_sprites.add(enemy)

# Function to spawn collectibles
def spawn_collectible():
    collectible = Collectible(SCREEN_WIDTH + random.randint(50, 80), SCREEN_HEIGHT - 70)
    collectibles.add(collectible)
    all_sprites.add(collectible)

# Function to draw health bar
def draw_health_bar(surface, x, y, health):
    pygame.draw.rect(surface, (255, 0, 0), (x, y, 100, 10))  # Red background
    pygame.draw.rect(surface, (0, 255, 0), (x, y, health, 10))  # Green health

# Game Over Screen
def game_over_screen():
    screen.fill(BLACK)
    game_over_text = font.render("Game Over!", True, WHITE)
    restart_text = font.render("Press R to Restart", True, WHITE)

    screen.blit(game_over_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 - 50))
    screen.blit(restart_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))

    pygame.display.flip()  # Show the game over screen

# Level Complete Screen
def show_level_complete_screen(level):
    screen.fill(WHITE)
    if level >= 3:  # If level is 3 or higher, show complete message
        complete_text = font.render("Game Complete!", True, BLACK)
        screen.blit(complete_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 - 50))
    else:
        level_complete_text = font.render(f"Level {level - 1} Complete!", True, BLACK)
        next_level_text = font.render(f"Starting Level {level}...", True, BLACK)
        screen.blit(level_complete_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 - 50))
        screen.blit(next_level_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    pygame.time.wait(2000)  # Wait for 2 seconds before starting the next level

# Function to increase difficulty based on level
def increase_difficulty(level):
    global PLAYER_SPEED

    if level == 1:  # Easy
        PLAYER_SPEED = 5
    elif level == 2:  # Moderate
        PLAYER_SPEED = 7
    elif level == 3:  # Hard
        PLAYER_SPEED = 9

    # Increase enemy speed
    for enemy in enemies:
        enemy.speed = random.randint(3 + level, 6 + level)  # Adjusted for level difficulty

# Game Loop
def game():
    global all_sprites, projectiles, enemies, collectibles
    all_sprites = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()

    score = 0
    level = 1
    level_threshold = 500
    spawn_timer = 0

    player = Player(all_sprites, projectiles)
    all_sprites.add(player)

    running = True
    game_over = False

    # Set initial difficulty
    increase_difficulty(level)

    while running:
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    player.shoot()
                if game_over and event.key == pygame.K_r:
                    # Restart the game
                    score = 0
                    level = 1
                    player.lives = INITIAL_LIVES
                    player.health = INITIAL_HEALTH
                    all_sprites.empty()  # Clear all sprites
                    projectiles.empty()  # Clear all projectiles
                    enemies.empty()  # Clear all enemies
                    collectibles.empty()  # Clear all collectibles
                    player = Player(all_sprites, projectiles)  # Recreate player
                    all_sprites.add(player)  # Add player to the sprite group
                    game_over = False  # Reset game over status
                    increase_difficulty(level)  # Reset difficulty

        # Game Over Check
        if player.lives <= 0:
            game_over = True

        # Update
        if not game_over:
            player.move()  # Call the player movement method
            all_sprites.update()

            # Collision checks
            for enemy in pygame.sprite.groupcollide(enemies, projectiles, True, True):
                score += 100  # Increase score when an enemy is defeated

            for collectible in pygame.sprite.spritecollide(player, collectibles, False):
                collectible.apply_effect(player)

            if pygame.sprite.spritecollideany(player, enemies):
                player.health -= 10
                if player.health <= 0:
                    player.lives -= 1
                    player.health = INITIAL_HEALTH

            # Spawn new enemies and collectibles periodically
            spawn_timer += 1
            if spawn_timer > 100 - level * 10:  # Increase frequency of spawns with level
                spawn_enemy(level)
                spawn_collectible()
                spawn_timer = 0

            # Draw
            screen.fill(WHITE)
            all_sprites.draw(screen)
            draw_health_bar(screen, 10, 10, player.health)

            # Score display
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 50))

            # Level display
            level_text = font.render(f"Level: {level}", True, BLACK)
            screen.blit(level_text, (SCREEN_WIDTH - 150, 10))

            # Check for level progression
            if level <= 3 and score >= level_threshold * level:
                level += 1
                show_level_complete_screen(level)
                increase_difficulty(level)

            # End game if level exceeds 3
            if level > 3:
                game_over = True  # Trigger game over if all levels are complete

        else:
            game_over_screen()

        pygame.display.flip()

# Start the game
game()
pygame.quit()
