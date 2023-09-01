from utils import import_folder
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[]}
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.status = 'idle'
        self.facing_right = True

        self.air = False
        self.air_time = 0
        self.start_speed = 0
        self.start_pos_y = self.rect.y
        self.direction = pygame.math.Vector2(0, 0)
    
    def import_character_assets(self):
        for animation in self.animations.keys():
            self.animations[animation] = import_folder("player " + animation)

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right == False:
            image = pygame.transform.flip(image, True, False)
        self.image = image

    def set_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 0:
            self.status = 'fall'
        elif self.direction.x != 0:
            self.status = 'run'
        else:
            self.status = 'idle'

    def step(self, world_shift, action):  
        self.control(action)
        self.update_air_time()
        self.shift(world_shift)
        self.set_status()
        self.animate()

    def control(self, action):  
        if action == 0 and not self.air:
            self.jump()
        elif action == 1:
            self.facing_right = True
            self.direction.x = 8
        elif action == 2:
            self.facing_right = False
            self.direction.x = -8
        elif action == 3:
            pass

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.air:
            self.jump()
        elif keys[pygame.K_RIGHT]:
            self.facing_right = True
            self.direction.x = 8
        elif keys[pygame.K_LEFT]:
            self.facing_right = False
            self.direction.x = -8

    def update(self, world_shift):
        self.get_input()
        self.update_air_time()
        self.shift(world_shift)
        self.set_status()
        self.animate()

    def jump(self):
        self.air = True
        self.air_time = 0
        self.start_speed = 56
        self.start_pos_y = self.rect.y

    def on_tale(self, tale_pos):
        self.air = False
        self.air_time = 0
        self.rect.bottom = tale_pos
        self.start_pos_y = self.rect.y

    def off_tale(self):
        self.air = True
        self.air_time = 0
        self.start_speed = 0
        self.start_pos_y = self.rect.y

    def under_tale(self, tale_pos):
        self.air_time = 0
        self.start_speed = 0
        self.rect.top = tale_pos
        self.start_pos_y = self.rect.y

    def update_pos_y(self):
        new_pos = self.start_pos_y - self.start_speed * self.air_time + (9.81 * self.air_time ** 2) / 2
        self.update_direction_y(new_pos)
        self.rect.y = new_pos

    def update_pos_x(self):
        self.rect.x += self.direction.x

    def update_direction_y(self, new_height):
        self.direction.y = new_height - self.rect.y

    def update_air_time(self):
        if self.air:
            self.air_time += 1/3

    def shift(self, shift):
        self.rect.y += shift
        self.start_pos_y += shift
