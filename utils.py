from os import walk
import pygame


tile_size = 25
screen_width = 525
screen_height = 725
player_width = 39
player_height = 52
floors_in_group = 5
floors_group_on_screen = 6
extra_floors_groups = 14
extra_fininsh_floors_groups = 7

image_types = {
  "tile": ('graphics/tile/1.png', (tile_size, tile_size)),
  "tile last": ('graphics/tile/2.png', (tile_size, tile_size)),
}

folder_types = {
    "player idle": ('graphics/player/idle', (player_width, player_height)),
    "player run": ('graphics/player/run', (player_width, player_height)),
    "player jump": ('graphics/player/jump', (player_width, player_height)),
    "player fall": ('graphics/player/fall', (player_width, player_height))
}

def import_folder(folder_type):
    surface_list = []
    try:
        path = folder_types[folder_type][0]
    except:
        print("warning! folder name not maped")

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()

            if image_surf.get_width() != folder_types[folder_type][1][0] or image_surf.get_height() != folder_types[folder_type][1][1]:
                print("warning! dimiensions of imported images diffrent than defined") 
            surface_list.append(image_surf)

    return surface_list

def import_file(image_type):
    try:
        path = image_types[image_type][0]
    except:
        print("warning! file name not maped")
    image_surf = pygame.image.load(path).convert_alpha()
    return image_surf
