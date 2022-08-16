import pygame, sys, random

pygame.init()
Window = pygame.display.set_mode((400,400))
Display = pygame.Surface((400,400))
Fps = pygame.time.Clock()

class Particle_System:
    def __init__(self):
        self.Particles = []
    def Scatter_Effect(self, x, y, random_range, gravity):
        return[[x, y], [random.randrange(-random_range[0],random_range[0]),
        random.randrange(-random_range[1],random_range[1])], random.randint(4, 6), gravity]

    def Fountain_Effect(self,x,y,dimension,gravity):
        return [[x, y], [random.randrange(-dimension[0], dimension[0]), -dimension[1]], random.randint(4, 6), gravity]
    
    def Rocket_Boost_Effect(self,x,y,gravity):
        return [[x, y], [random.randint(0, 20) / 10 - 1, 2], random.randint(4, 6), gravity]

class Play_Particle:
    def __init__(self):
        pass
    def Deploy_Particle(self, surface, particles, bounce, duration, GRID_SIZE, tile_map):
        for particle in particles:
            particle[0][0] += particle[1][0]
            loc_str = f'{int(particle[0][0] / GRID_SIZE)}:{int(particle[0][1] / GRID_SIZE)}'
            if bounce > 0:
                if loc_str in tile_map:
                    particle[1][0] = -bounce * particle[1][0]
                    particle[1][1] *= 0.95
                    particle[0][0] += particle[1][0] * 2
            particle[0][1] += particle[1][1]
            loc_str = f'{int(particle[0][0] / GRID_SIZE)}:{int(particle[0][1] / GRID_SIZE)}'
            if bounce > 0: 
                if loc_str in tile_map:
                    particle[1][1] = -bounce * particle[1][1]
                    particle[1][0] *= 0.95
                    particle[0][1] += particle[1][1] * 2
            particle[2] -= duration
            particle[1][1] += particle[3]
            pygame.draw.circle(surface, (255, 255, 255), [int(particle[0][0]), 
            int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                particles.remove(particle)

GRID_SIZE = 80

tile_map = {}
for i in range(400//GRID_SIZE):
    tile_map[f'{i}:4'] = [i,4,'grey'] #hash mapping

Particle_Type = []
while 1:
    Display.fill('black')
    Fps.tick(60)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Spawn per click -------------------------------------------------#
    if pygame.mouse.get_pressed()[0]:
        for i in range(10):
         Particle_Type.append(Particle_System().Scatter_Effect(mouse_x,mouse_y,[3,10], 0))
    elif pygame.mouse.get_pressed()[2]:
        for i in range(10):
         Particle_Type.append(Particle_System().Scatter_Effect(mouse_x,mouse_y,[5,5],0.5))    

    # Continous spawn --------------------------------------------------------#
    # Particle_Type.append(Particle_system().Fountain_Effect(200,200,[4,8],0.5))
    
    
    Play_Particle().Deploy_Particle(Display, Particle_Type, 0.7, 0.1, GRID_SIZE, tile_map) # takes a (particles: list, bounce: float, duration: float, GRID_SIZE: int, tile_map: dict)
    Window.blit(Display,(0,0))
    
    for tile in tile_map:
        pygame.draw.rect(Window, tile_map[tile][2], pygame.Rect(tile_map[tile][0]*GRID_SIZE, tile_map[tile][1]*GRID_SIZE, GRID_SIZE,GRID_SIZE))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            sys.exit()
            
    
    pygame.display.update()
    
