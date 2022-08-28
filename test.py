import pygame, os, sys, time
from pygame.locals import *
pygame.init() # initiates pygam\

clock = pygame.time.Clock()

pygame.display.set_caption('Pygame Platformer')

WINDOW_SIZE = (600,400)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

display = pygame.Surface((300,200)) # used as the surface for rendering, which is scaled

last_time = time.time()

left, right, jump = False, False, False

vertical_momentum = 0
jump_cooldown = 0

scroll = [0,0]

dirt_img = pygame.image.load(os.path.join('asset', 'tile1.png')).convert()
dirt_img.set_colorkey((0,0,0))

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('asset/idle', 'player_idle_right0.png')).convert()
        self.image.set_colorkey((0,0,0))
        self.image_copy = self.image.copy()
        self.rect = self.image_copy.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation = 0
        self.vertical_momentum = 0

    def collision_test(self):
        hit_list = []
        for tile in map.tiles:
            if tile[1].colliderect(self.rect):
                hit_list.append(tile[1])
        return hit_list

    def move(self,direction):
        self.rect.x += direction[1]
        hit_list = self.collision_test()
        for tile in hit_list:
            if direction[1] > 0:
                self.rect.right = tile.left
            elif direction[1] < 0:
                self.rect.left = tile.right
        self.rect.y += direction[2]
        hit_list = self.collision_test()
        for tile in hit_list:
            if direction[2] > 0:
                self.rect.bottom = tile.top
            elif direction[2] < 0:
                self.rect.top = tile.bottom
        
        self.update(direction[0])
    
    def update(self,status):
        print(status)

    def draw(self,surface):
        surface.blit(self.image,(self.rect.x - int(scroll[0]),self.rect.y + 3 - int(scroll[1])))


class Map(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.tiles = []
        self.tile_map = {}
    
    def setup(self):
        for i in range(600//16):
           self.tile_map[f'{i}:180'] = 0
           image = pygame.image.load(os.path.join('asset', 'tile1.png'))
           image.set_colorkey((0,0,0))
           rect = image.get_rect()
           rect.x = i*16
           rect.y = 180
           self.tiles.append([image,rect])
   
    def draw(self,surface):
        for tile in self.tiles:
            surface.blit(tile[0],(tile[1].x - int(scroll[0]),tile[1].y-int(scroll[1])))

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
    
    def draw(self,surface):
        surface.blit(self.image,(self.rect.x - int(scroll[0]),self.rect.y - int(scroll[1])))


map = Map()
map.setup()
player = Player(125,80)
trees, droplets = [], []

location1 = [[30,180],[250, 180]]
location2 = [[200,140],[400,140]]

for position in location1:
    tree = Trees(position[0], position[1])
    trees.append(tree)

for position in location2:
    droplet = Droplet(position[0], position[1])
    droplets.append(droplet)


while True: # game loop
    dt = time.time() - last_time
    dt *= 60
    last_time = time.time()
    display.fill((25,25,25)) 

#camera ----------------------------------------------------------------#
    scroll[0] += (player.rect.x-scroll[0]-128)/20
    scroll[1] += (player.rect.y-scroll[1]-115)/20
    
    player_movement = ['idle',0,0]
    if left:
        player_movement[1] -= 3
        player_movement[0] = 'left'
    if right:
         player_movement[1] += 3
         player_movement[0] = 'right'
    player_movement[2] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3
    if jump_cooldown > 0:
        jump_cooldown -= 1

    for tree in trees:
        tree.update(dt)
        tree.draw(display)
    for droplet in droplets:
        droplet.update(dt)
        droplet.draw(display)

    map.draw(display)
    player.move(player_movement)
    player.draw(display)
    
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
                    jump_cooldown = 60 #60 for single jump 30 for multiple/double jumps
                    vertical_momentum = -5

        if event.type == KEYUP:
            if event.key == K_d:
               right = False
            if event.key == K_a:
               left = False
        
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)
