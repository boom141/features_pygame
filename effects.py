import pygame, os

class Pulse(pygame.sprite.Sprite):
	def __init__(self,x,y,transition,offset,value):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('asset/effects', 'pulse.png'))
		self.image_copy = self.image
		self.rect = self.image_copy.get_rect()
		self.rect.x = x 
		self.rect.y = y
		self.transition = transition
		self.offset = offset
		self.scale = [0,0]
		self.scale_value = 0
		self.play_animation = value

	def update(self,dt):
		if self.play_animation:
			if self.scale[0] < self.transition[2] - 50:
				self.scale_value = self.transition[0]
			else:
				self.scale_value = self.transition[1] 
			self.scale[0] += self.scale_value * dt
			self.scale[1] += self.scale_value * dt

		if self.scale[0] > self.transition[2]:
			self.play_animation = False
			self.kill()

		self.image_copy = pygame.transform.scale(self.image,(int(self.scale[0]),
		int(self.scale[1])))
		self.image_copy.set_colorkey((0,0,0))

	def draw(self,surface):
		surface.blit(self.image_copy,((self.rect.x - self.image_copy.get_width()//2) + self.offset[0] # x offset
		,((self.rect.y - self.image_copy.get_height()//2) + self.offset[1]))) # y offset