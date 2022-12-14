import pygame, os, sys, time, random
from load_sprite import*
from particles import*
from effects import*

from pygame.locals import *
pygame.init() # initiates pygam\

clock = pygame.time.Clock()

pygame.display.set_caption('Pygame Platformer')

WINDOW_SIZE = (600,400)
PIXEL_SIZE = 16

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

display = pygame.Surface((300,200)) # used as the surface for rendering, which is scaled

last_time = time.time()

left, right, jump = False, False, False

vertical_momentum = 0
jump_cooldown = 0

scroll = [0,0]

particle_color = [(255,255,255),(4,174,184),(56,136,156)]

dirt_img = pygame.image.load(os.path.join('asset', 'tile1.png')).convert()
dirt_img.set_colorkey((0,0,0))

class Play_Particle(pygame.sprite.Sprite):
    def __init__(self): 
        pygame.sprite.Sprite.__init__(self)
        self.particles = []
        
    def draw(self,surface,skin_image,physics): #physics:[bounce, seconds, gravity]
        for particle in self.particles:
            particle[0][0] += particle[1][0]
            loc_str = f'{int(particle[0][0] // PIXEL_SIZE)}:{int(particle[0][1] // PIXEL_SIZE)}'
            if physics[0] > 0:
                if loc_str in map.tile_map:
                    particle[1][0] = -physics[0] * particle[1][0]
                    particle[1][1] *= 0.95
                    particle[0][0] += particle[1][0] * 2
            particle[0][1] += particle[1][1]
            loc_str = f'{int(particle[0][0] // PIXEL_SIZE)}:{int(particle[0][1] // PIXEL_SIZE)}'
            if physics[0] > 0: 
                if loc_str in map.tile_map:
                    particle[1][1] = -physics[0] * particle[1][1]
                    particle[1][0] *= 0.95
                    particle[0][1] += particle[1][1] * 2
            particle[2] -= physics[1]
            particle[1][1] += physics[2]
            pygame.draw.circle(surface, (particle_color[random.randint(0,2)]), [particle[0][0],particle[0][1]], particle[2])
            if particle[2] <= 0:
                self.particles.remove(particle)

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.player_image = pygame.image.load(os.path.join('asset/idle', 'player_idle_right0.png')).convert()     
        self.player_image.set_colorkey((0,0,0))
        self.image_copy = self.player_image.copy()
        self.rect = self.image_copy.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.landing_image = pygame.image.load(os.path.join('asset/effects/landing', '0.png')).convert()
        self.landing_image_copy = self.landing_image.copy()
        self.landing_image_rect = self.landing_image_copy.get_rect()
        self.player_animation = 0
        self.effects_animation = -1
        self.effects_type = 'landing'
        self.animate = False
        self.facing = 'right'

    def collision_test(self):
        hit_list = []
        for tile in map.tiles:
            if tile[1].colliderect(self.rect):
                hit_list.append(tile[1])
        return hit_list

    def move(self,direction,dt):
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        self.rect.x += direction[1] * dt
        hit_list = self.collision_test()
        for tile in hit_list:
            if direction[1] > 0:
                self.rect.right = tile.left
            elif direction[1] < 0:
                self.rect.left = tile.right
        self.rect.y += direction[2] * dt
        hit_list = self.collision_test()
        for tile in hit_list:
            if direction[2] > 0:
                self.rect.bottom = tile.top
                collision_types['bottom'] = True
            elif direction[2] < 0:
                self.rect.top = tile.bottom
        
        self.update(direction,collision_types,dt)
    
    def update(self,status,collision_types,dt):
        if status[1] > 0:
            self.facing = 'right'
        if status[1] < 0:
            self.facing = 'left'
        if self.player_animation >= player_sprites[status[0]]['frames']:
            self.player_animation = 0
        self.player_animation += 0.185 * dt
        if self.player_animation <= player_sprites[status[0]]['frames']:
            self.player_image = pygame.image.load(os.path.join(f'asset/{status[0]}', 
            f'{player_sprites[status[0]][self.facing]}{int(self.player_animation)}.png'))
            self.player_image.set_colorkey((0,0,0))

# landing animation ----------------------------------------------------------------#
        if collision_types['bottom'] == False:
            self.effects_animation = 0
       
        if collision_types['bottom']:
            self.effects_animation += 0.395 * dt
            self.animate = True
            self.effects_type = 'landing'

        if self.effects_animation >= 4:
            self.effects_animation = 4
            self.animate = False

        self.landing_image = pygame.image.load(os.path.join(f'asset/effects/{self.effects_type}', f'{int(self.effects_animation)}.png'))
        self.landing_image_copy = pygame.transform.scale(self.landing_image,(105,30))
        self.landing_image_copy.set_colorkey((0,0,0))
    def draw(self,surface):
        surface.blit(self.player_image,(self.rect.x - int(scroll[0]),self.rect.y + 3 - int(scroll[1])))
        if self.animate:
            surface.blit(self.landing_image_copy,((self.rect.x - 20)- int(scroll[0]),(self.rect.bottom - 15) - int(scroll[1])))

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('asset/enemy-idle', 'idle_right0.png')).convert()
        self.image.set_colorkey((0,0,0))
        self.image_copy = self.image.copy()
        self.rect = self.image_copy.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation = 0
        self.walk_countdown = 0
        self.idle_countdown = -1
        self.walk_direction = True
        self.vertical_momentum = 0
        self.status = 'walk'
        self.facing = 'right'

    def collision_test(self):
        hit_list = []
        for tile in map.tiles:
            if tile[1].colliderect(self.rect):
                hit_list.append(tile[1])
        return hit_list
    
    def move(self,dt):
        direction = [0,0] 
        direction[1] += self.vertical_momentum 
        self.vertical_momentum += 0.2
        if self.vertical_momentum > 3:
            self.vertical_momentum = 3
        
        if self.idle_countdown > 0:
            self.idle_countdown -= 1

        if random.randint(1,200) == 1 and self.idle_countdown == 0:
            self.status = 'idle'
            self.idle_countdown = 50 

        if self.idle_countdown <= 0:
            self.status = 'walk'
            self.idle_countdown = 0

            if self.walk_countdown == 80:
                self.walk_direction = not self.walk_direction
                self.walk_countdown = 0
            self.walk_countdown += 0.5
            
            if self.walk_direction:
                direction[0] += 2 * dt
                self.facing = 'right'
            else:
                direction[0] -= 2 * dt
                self.facing = 'left'


        self.rect.x += int(direction[0])
        self.rect.y += direction[1]
        hit_list = self.collision_test()
        for tile in hit_list:
            if direction[1] > 0:
                self.rect.bottom = tile.top
            elif direction[1] < 0:
                self.rect.top = tile.bottom

        self.update(dt)

    def update(self,dt):
        if self.animation >= enemy_sprites[self.status]['frames']:
            self.animation = 0
        self.animation += 0.175 * dt
        if self.animation <= enemy_sprites[self.status]['frames']:
            self.image = pygame.image.load(os.path.join(f'asset/enemy-{self.status}', 
            f'{enemy_sprites[self.status][self.facing]}{int(self.animation)}.png'))
            self.image.set_colorkey((0,0,0)) 

    def draw(self,surface):
        surface.blit(self.image,(self.rect.x - int(scroll[0]),self.rect.y + 3 - int(scroll[1])))

class Map(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.tiles = []
        self.tile_map = {}
    
    def setup(self):
        for i in range(600//16):
            image = pygame.image.load(os.path.join('asset', 'tile1.png'))
            image.set_colorkey((0,0,0))
            rect = image.get_rect()
            rect.x = i*16
            rect.y = 180
            self.tiles.append([image,rect])
   
    def draw(self,surface):
        for tile in self.tiles:
            rect = surface.blit(tile[0],(tile[1].x - int(scroll[0]),tile[1].y-int(scroll[1])))
            self.tile_map[f'{int(rect.x // PIXEL_SIZE)}:{int(rect.y // PIXEL_SIZE)}'] = rect

class Misc(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.water_meter = pygame.image.load(os.path.join('asset/misc', 'water_meter.png'))
        self.image1 = pygame.transform.scale(self.water_meter,(105,13))
        self.image1.set_colorkey((0,0,0))

    def update(self):
        pass

    def draw(self,surface):
        surface.blit(self.image1,(5,5))


class Trees(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('asset/tree', 'tree0.png'))
        self.image_copy = self.image.copy()
        self.rect = self.image_copy.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.animation = 0
    
    def update(self,dt):
        if self.animation >= 8:
            self.animation =0
        self.animation += 0.2 * dt
        if self.animation <= 8:
            self.image = pygame.image.load(os.path.join('asset/tree', f'tree{int(self.animation)}.png')).convert_alpha()
            self.image.set_colorkey((0,0,0))
            
    def draw(self,surface):
        surface.blit(self.image,(self.rect.x - int(scroll[0]),self.rect.y - int(scroll[1])))

class Droplet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('asset/droplet', 'water_droplet0.png'))
        self.image_copy = self.image.copy()
        self.rect = self.image_copy.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation = 0
    
    def update(self,dt):
        if self.animation >= 7:
            self.animation = 0
        self.animation += 0.2 * dt
        if self.animation <= 7:
            self.image = pygame.image.load(os.path.join('asset/droplet', f'water_droplet{int(self.animation)}.png')).convert_alpha()
            self.image.set_colorkey((0,0,0))
   
    def player_collision(self):
        if self.rect.colliderect(player.rect):
           pulse = Pulse(player.rect.x - int(scroll[0]),player.rect.y - int(scroll[1]),[8,3,180],[25,15],True)
           effects.add(pulse)  
           for i in range(30):
                droplet_particle.particles.append(Particle_System().Scatter_Effect(self.rect.x - int(scroll[0]),
                self.rect.y - int(scroll[1]),[5,5]))
           self.kill()     
    
    def draw(self,surface):
        surface.blit(self.image,(self.rect.x - int(scroll[0]),self.rect.y - int(scroll[1])))


map = Map()
map.setup()
player = Player(125,80)
enemy = Enemy(200,120)
misc = Misc()
droplet_particle = Play_Particle()
trees = pygame.sprite.Group()
droplets = pygame.sprite.Group()
effects = pygame.sprite.Group() 

location1 = [[30,183],[250, 183]]
location2 = [[200,100],[400,140]]

for position in location1:
    tree = Trees(position[0], position[1])
    trees.add(tree)

for position in location2:
    droplet = Droplet(position[0], position[1])
    droplets.add(droplet)
 

while True: # game loop
#framerate independence -------------------------------------------------#
    dt = time.time() - last_time
    dt *= 60
    last_time = time.time()
    display.fill((25,25,25)) 

#camera ----------------------------------------------------------------#
    scroll[0] += (player.rect.x-scroll[0]-128)/20
    scroll[1] += (player.rect.y-scroll[1]-115)/20

#player controller -----------------------------------------------------#    
    player_movement = ['idle',0,0]
    if left:
        player_movement[1] -= 3
        player_movement[0] = 'walk'
    if right:
         player_movement[1] += 3
         player_movement[0] = 'walk'
    player_movement[2] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3
    if jump_cooldown > 0:
        jump_cooldown -= 1
        player_movement[0] = 'jump'

# draw section----------------------------------------------------------#
    for tree in trees:
        tree.update(dt)
        tree.draw(display)
    
    for droplet in droplets:
        droplet.update(dt)
        droplet.player_collision()
        droplet.draw(display)
    
    map.draw(display)
    player.move(player_movement,dt)
    player.draw(display)
    enemy.move(dt)
    enemy.draw(display)
    droplet_particle.draw(display, 'default_skin.png', [0.4, 0.1, 0])
    misc.draw(display)

    for effect in effects:
        effect.update(dt)
        effect.draw(display)

    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_d:
                right = True
            if event.key == K_a:
                left = True
            if event.key == K_SPACE:
                if jump_cooldown == 0:
                    jump_cooldown = 65 #60 for single jump 30 for multiple/double jumps
                    vertical_momentum = -5

        if event.type == KEYUP:
            if event.key == K_d:
               right = False
            if event.key == K_a:
               left = False
        
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)
