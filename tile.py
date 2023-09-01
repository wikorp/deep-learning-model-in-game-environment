from utils import tile_size, screen_height, extra_floors_groups, floors_in_group, import_file
import pygame
import random


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, type):
        super().__init__()
        self.type = type
        self.import_assets(type)
        self.rect = self.image.get_rect(topleft=pos)

    def import_assets(self, type):
        self.image = import_file(type)

    def update(self, shift):
        self.shift(shift)

    def shift(self, shift):
        self.rect.y += shift

    def displace(self):
        shift = random.randint(-5, 5)
        self.rect.x += shift
