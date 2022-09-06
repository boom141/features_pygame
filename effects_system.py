import pygame, sys, os, time	


pygame.init()
Window = pygame.display.set_mode((400,400))
Fps = pygame.time.Clock()

last_time = time.time()

class Pulse(pygame.sprite.Sprite):
	def __init__(self,x,y,value):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('asset/effects', 'pulse.png'))
		self.image_copy = self.image
		self.position = [x,y]
		self.scale = [0,0]
		self.scale_value = 15
		self.transition = [20,2,550]
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
		surface.blit(self.image_copy,(self.position[0] - self.image_copy.get_width()//2
		,self.position[1] - self.image_copy.get_height()//2))

pulses = pygame.sprite.Group()

while 1:    
#framerate independence -------------------------------------------------#
	dt = time.time() - last_time
	dt *= 60
	last_time = time.time()

	Window.fill((25,25,25))
	mx,my = pygame.mouse.get_pos()

	if pygame.mouse.get_pressed()[0]:
			pulse = Pulse(mx,my,True)
			if len(pulses) == 0:
				pulses.add(pulse)
	
	for pulse in pulses:
		pulse.update(dt)
		pulse.draw(Window)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_d:
				right = True
			if event.key == pygame.K_a:
				left = True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_d:
				right = False
			if event.key == pygame.K_a:
				left = False

	pygame.display.update()