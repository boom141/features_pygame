import pygame, os

class Pulse(pygame.sprite.Sprite):
	def __init__(self,x,y,value):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('asset/effects', 'pulse.png'))
		self.image_copy = self.image
		self.rect = self.image_copy.get_rect()
		self.rect.x = x 
		self.rect.y = y
		self.scale = [0,0]
		self.play_animation = value

	def update(self,dt):
		if self.play_animation:
			self.scale[0] += 6 * dt # value per second
			self.scale[1] += 6 * dt

		if self.scale[0] > 180: # duration value
			self.play_animation = False
			self.kill()

		self.image_copy = pygame.transform.scale(self.image,(int(self.scale[0]),
		int(self.scale[1])))
		self.image_copy.set_colorkey((0,0,0))

	def draw(self,surface):
		surface.blit(self.image_copy,((self.rect.x - self.image_copy.get_width()//2) + 20 # x offset
		,((self.rect.y - self.image_copy.get_height()//2) + 5))) # y offset