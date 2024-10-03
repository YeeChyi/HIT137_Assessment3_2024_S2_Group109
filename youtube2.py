import pygame

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('CLUB PENGUIN')

# speed rate
clock = pygame.time.Clock()
FPS = 60


# player moves
moving_left = False
moving_right = False 

# creating character
class Penguin(pygame.sprite.Sprite):
	def __init__(self, x, y, scale, speed):
		pygame.sprite.Sprite.__init__(self)
		self.speed = speed

		img = pygame.image.load('girl1.jpg')
		self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

# for movements
def move(self, moving_left, moving_right):
	dx = 0
	dy = 0
    

if moving_left: 
        dx = -self.speed
if moving_right:
        dy = self.speed
		
        self.rect.x += dx
        self.rect.y += dy
        



def draw(self):
		screen.blit(self.image, self.rect)



player = Penguin(200, 200, 3, 5)


run = True
while run:

	clock.tick()
	
	player.draw()

player.move(moving_left, moving_right)


for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False

   # keyboard functions when pressed
if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				moving_left = True
			if event.key == pygame.K_d:
				moving_right = True
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