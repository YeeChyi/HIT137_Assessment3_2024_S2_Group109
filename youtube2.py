import pygame

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('CLUB PENGUIN')


class Penguin(pygame.sprite.Sprite):
	def __init__(self, x, y, scale):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('girl1.jpg')
		self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def draw(self):
		screen.blit(self.image, self.rect)



player = Penguin(200, 200, 3)
player2 = Penguin(400, 200, 3)



run = True
while run:

	
	player.draw()
	player2.draw()

	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False


	pygame.display.update()

pygame.quit()