from utils import tile_size, screen_height, player_width, player_height, extra_floors_groups, extra_fininsh_floors_groups, floors_in_group
from player import Player
from tile import Tile
import pygame
import random


class Level:
    def __init__(self, layout, surface):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.display_surface = surface

        self.score = 0
        self.world_shift = 2
        self.finish = False
        self.setup_level(layout)

    def step(self, action):
        self.tiles.update(self.world_shift)
        self.player.sprite.step(self.world_shift, action) 
        self.horizontal_movement_collision()
        colision_status = self.vertical_movement_collision()
        self.update_score()

        reward = self.reward_shaping(colision_status)
        return reward
    
    def reward_shaping(self, status):
        reward = None
        if status == 0:  # alive
            reward = 1
        elif status == 1:  # higher plaform
            reward = 3
        elif status == 2:  # lower or same platform
            reward = -3
        elif status == 3:  # last platform
            reward = 100
        
        if self.check_fail():  # fail
            reward = -10
        return reward

    def render(self):
        self.tiles.draw(self.display_surface)
        self.player.draw(self.display_surface)

    def reset(self, layout):
        self.score = 0
        self.finish = False
        for sprite in self.tiles.sprites():
            sprite.kill()
        self.player.sprite.kill()

        self.setup_level(layout)

    def setup_level(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size - tile_size - tile_size * (extra_floors_groups + extra_fininsh_floors_groups) * floors_in_group
                if cell == 'X':
                    tile = Tile((x, y), tile_size, "tile")
                    if col_index != 0 and col_index != 20:
                        tile.displace()
                    r = random.randint(1, 10)
                    if r % 10 == 0 and col_index != 0 and col_index != 20:
                        del tile
                    else:
                        self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x - (player_width - tile_size) / 2, y - (player_height - tile_size)))
                    self.player.add(player_sprite)
                if cell == 'F':
                    tile = Tile((x, y), tile_size, "tile last")
                    tile.displace()
                    self.tiles.add(tile)

    def run(self):
        self.tiles.update(self.world_shift)
        self.player.update(self.world_shift)
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.tiles.draw(self.display_surface)
        self.player.draw(self.display_surface)
        self.update_score()

    def horizontal_movement_collision(self):
        player = self.player.sprite 
        player.update_pos_x()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

        player.direction.x = 0 

    def vertical_movement_collision(self):
        collision_status = 0
        player = self.player.sprite
        player.update_pos_y()

        player_on_tale = False
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.under_tale(sprite.rect.bottom)

                elif player.direction.y > 0:
                    if player.start_pos_y > player.rect.y:
                        collision_status = 1
                        if sprite.type == "tile last":
                            collision_status = 3
                            self.finish = True
                    elif player.start_pos_y < player.rect.y:
                        collision_status = 2 

                    player.on_tale(sprite.rect.top)
                    player_on_tale = True

            if player.rect.bottom == sprite.rect.top:
                if player.rect.right > sprite.rect.left and player.rect.left < sprite.rect.right:
                    player_on_tale = True

        if not player_on_tale and not player.air:
            player.off_tale()

        return collision_status

    def check_fail(self):
        if self.player.sprite.rect.y > screen_height:
            return True
        return False

    def check_end(self):
        if self.check_fail() or self.finish == True:
            return True
        return False

    def update_score(self):
        if self.check_end() == False:
            self.score += 1
        if self.finish:
            self.score = 1500

    def update_shift(self):
        print (self.player.sprite.rect.y)
        if self.player.sprite.rect.y < 300:
            self.world_shift = 2

    def get_score(self):
        return self.score
