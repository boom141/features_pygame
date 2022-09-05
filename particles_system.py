import pygame, sys, random, os

pygame.init()
Window = pygame.display.set_mode((400,400))
Display = pygame.Surface((400,400))
Fps = pygame.time.Clock()


GRID_SIZE = 80
slide =  [0,0]

right, left = False, False

tile_map = {}
# for i in range(400//GRID_SIZE):
#     tile_map[f'{i}:4'] = [i,4,'grey'] #hash mapping


class Particle_System:
    def __init__(self):
        self.Particles = []
    def Scatter_Effect(self, x, y, random_range):
        return[[x, y], [random.randrange(-random_range[0],random_range[0]),
        random.randrange(-random_range[1],random_range[1])], random.randint(4, 6)]

    def Fountain_Effect(self,x,y,dimension):
        return [[x, y], [random.randrange(-dimension[0], dimension[0]), -dimension[1]], random.randint(4, 6)]
    
    def Rocket_Boost_Effect(self,x,y):
        return [[x, y], [random.randint(0, 20) / 10 - 1, 2], random.randint(4, 6)]

class Play_Particle(pygame.sprite.Sprite):
	def __init__(self): 
		pygame.sprite.Sprite.__init__(self)
		self.particles = []
		
	def draw(self,surface,skin_image,physics): #physics:[bounce, seconds, gravity]
		for particle in self.particles:
			particle[0][0] += particle[1][0]
			loc_str = f'{int(particle[0][0] // GRID_SIZE)}:{int(particle[0][1] // GRID_SIZE)}'
			if physics[0] > 0:
				if loc_str in tile_map:
					particle[1][0] = -physics[0] * particle[1][0]
					particle[1][1] *= 0.95
					particle[0][0] += particle[1][0] * 2
			particle[0][1] += particle[1][1]
			loc_str = f'{int(particle[0][0] // GRID_SIZE)}:{int(particle[0][1] // GRID_SIZE)}'
			if physics[0] > 0: 
				if loc_str in tile_map:
					particle[1][1] = -physics[0] * particle[1][1]
					particle[1][0] *= 0.95
					particle[0][1] += particle[1][1] * 2
			particle[2] -= physics[1]
			particle[1][1] += physics[2]
			image = pygame.image.load(os.path.join('particle-skin', skin_image)).convert_alpha()
			image.set_colorkey((0,0,0))
			surface.blit(image, (particle[0][0],particle[0][1]))
			if particle[2] <= 0:
				self.particles.remove(particle)

   

play_particle1 = Play_Particle()
play_particle2 = Play_Particle()


while 1:
	Display.fill((25,25,25))
	Fps.tick(60)
	mouse_x, mouse_y = pygame.mouse.get_pos()

# Spawn per click -------------------------------------------------#
	if pygame.mouse.get_pressed()[0]:
		for i in range(10):
			play_particle2.particles.append(Particle_System().Fountain_Effect(mouse_x,mouse_y,[3,10]))
	elif pygame.mouse.get_pressed()[2]:
		for i in range(10):
			play_particle1.particles.append(Particle_System().Scatter_Effect(mouse_x,mouse_y,[5,5]))
		
    # Continous spawn --------------------------------------------------------#
    # Particle_Type.append(Particle_system().Fountain_Effect(200,200,[4,8],0.5))
	
	play_particle1.draw(Display, 'default_skin.png', [0.4, 0.1, 0.5]) #physics:[bounce, seconds, gravity]
	play_particle2.draw(Display, 'default_skin.png', [0.4, 0.1, 0.5]) #physics:[bounce, seconds, gravity]

	move = [0,0]
	if right:
		move[0] += 3
	if left:
		move[0] -= 3

	slide[0] += move[0]

	for i in range(400//GRID_SIZE):
		rect = pygame.draw.rect(Display, 'grey', (i* GRID_SIZE - int(slide[0]), 320, GRID_SIZE, GRID_SIZE))
		tile_map[f'{int(rect.x//GRID_SIZE)}:{320//GRID_SIZE}'] = rect

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

	Window.blit(Display,(0,0))
	pygame.display.update()

