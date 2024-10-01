import pygame
import random

# initialise pygame
pygame.init()

# constants
screen_width = 1000
screen_height = 800
fps = 90
white = (255, 255, 255)
black = (0, 0, 0)
initial_health = 100
initial_lives = 3
collectible_health_boost = 20

# setup the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Super Tank Adventure!")
clock = pygame.time.Clock()

# load images
player_image = pygame.image.load("tank.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (70, 70))  #scale to fit
enemy_image = pygame.image.load("ghost.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (50, 50))   #scale to fit

# font for displaying text
font = pygame.font.Font(None, 36)