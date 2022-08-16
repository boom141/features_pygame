import pygame ,os, math, sys, random

pygame.init()

WIDTH ,HEIGHT = 400,400
Display = pygame.display.set_mode((WIDTH, HEIGHT))
Window = pygame.Surface((WIDTH,HEIGHT))
pygame.display.set_caption('Aim and shoot Test')
CLOCK = pygame.time.Clock()
GRID_SIZE = 80

class Current_Weapon:
    def __init__(self, weapon_name, facing,):
        self.weapon_name = weapon_name
        self.facing = facing
    
    def Deploy_Weapon(self):
        sprite_image = pygame.image.load(os.path.join('asset', f'{self.weapon_name}{self.facing}.png')) #original image
        sprite_image_copy =  sprite_image.copy() # reserve for containing the upadated transform in image / also the one that we need to blit
        sprite_image_rect = sprite_image_copy.get_rect(center=(200,200)) # declaring values for the center position of the image

        return sprite_image, sprite_image_copy, sprite_image_rect

class Default_Bullet:
    def __ini__(self):
        pass
    def Bullet_Attribute(self, muzzle_pos, direction, duration, angle):
        return [[muzzle_pos[0],muzzle_pos[1]],[direction[0],direction[1]],random.randint(duration[0],duration[1]),angle]
    
    def Deploy_Bullet(self,surface,bullets,bounce,GRID_SIZE,tile_map,duration):
        for bullet in bullets:
            bullet[0][0] += bullet[1][0]
            loc_str = f'{int(bullet[0][0] / GRID_SIZE)}:{int(bullet[0][1] / GRID_SIZE)}'
            if bounce > 0:
                if loc_str in tile_map:
                    bullet[1][0] = -bounce * bullet[1][0]
                    bullet[1][1] *= 0.95
                    bullet[0][0] += bullet[1][0] * 2
            bullet[0][1] += bullet[1][1]
            loc_str = f'{int(bullet[0][0] / GRID_SIZE)}:{int(bullet[0][1] / GRID_SIZE)}'
            if bounce > 0: 
                if loc_str in tile_map:
                    bullet[1][1] = -bounce * bullet[1][1]
                    bullet[1][0] *= 0.95
                    bullet[0][1] += bullet[1][1] * 2
            bullet[2] -= duration
            pygame.draw.circle(surface, (255, 255, 255), [int(bullet[0][0]), 
            int(bullet[0][1])], int(bullet[2]))
            if bullet[2] <= 0:
                bullets.remove(bullet)


sprite_image_crosser = pygame.image.load(os.path.join('asset', 'crosser.png'))
sprite_crosser_object = sprite_image_crosser.copy()

facing = 'left'
bullet_list = []
tile_map = {}

while True:
    Window.fill((40,40,40))
    CLOCK.tick(60)
    pygame.mouse.set_visible(False)
    
    sprite_image_gun, sprite_object,  sprite_rect = Current_Weapon('gun_ak_', facing).Deploy_Weapon()

    mouse_x, mouse_y = pygame.mouse.get_pos()
    sprite_x, sprite_y = sprite_rect.center

    distance_x = mouse_x - sprite_x
    distance_y = mouse_y - sprite_y
    
    horizontal_grid_size = (mouse_x//30)
    
    angle = math.degrees(math.atan2(distance_y,distance_x))
    
    direction_x = math.cos(math.atan2(distance_y,distance_x))
    direction_y = math.sin(math.atan2(distance_y,distance_x))

    sprite_crosser_object = pygame.transform.scale(sprite_image_crosser,(30,30)).convert_alpha()
    sprite_crosser_rect = sprite_crosser_object.get_rect()

    Window.blit(sprite_crosser_object,(mouse_x - sprite_crosser_rect.centerx,mouse_y - sprite_crosser_rect.centery))

    if horizontal_grid_size < 6:
        facing = 'right'
    else:
        facing = 'left'
    
    sprite_object = pygame.transform.rotate(sprite_image_gun, -angle).convert_alpha()
    sprite_rect = sprite_object.get_rect(center=(sprite_x,sprite_y)) #reposition of image
    
    Window.blit(sprite_object,sprite_rect)
    
    if pygame.mouse.get_pressed()[0]:
        bullet_list.append(Default_Bullet().Bullet_Attribute([200,200],[direction_x,direction_y],[4,6],angle))

    Default_Bullet().Deploy_Bullet(Window,bullet_list,0,GRID_SIZE,tile_map,0.035)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    Display.blit(Window,(0,0))
    pygame.display.update()
