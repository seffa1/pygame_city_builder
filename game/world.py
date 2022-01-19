import pygame as pg
import pygame.image
import random

from .settings import TILE_SIZE

class World:
    def __init__(self, grid_length_x, grid_length_y, width, height):
        self.grid_lenth_x = grid_length_x
        self.grid_lenth_y = grid_length_y
        self.width = width
        self.height = height

        # Creates a surface to draw to the screen to avoid needing to iterate through each grass block tile
        # Instead just draw this one surface which contains all the grass block tiles
        self.grass_tiles = pg.Surface((width, height))
        self.tiles = self.load_images()
        self.world = self.create_world()


    def create_world(self):
        """Returns a 2D array of dictionaries representing each of the world's tiles.
        Each dictionary contains information about its tile"""
        world = []

        for grid_x in range(self.grid_lenth_x):
            world.append([])
            for grid_y in range(self.grid_lenth_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)

                render_pos = world_tile['render_pos']
                self.grass_tiles.blit(self.tiles['block'], (render_pos[0] + self.width/2, render_pos[1] + self.height/4))

        return world

    def grid_to_world(self, grid_x, grid_y):
        """Transforms grid coordinates to tile elements"""
        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]

        # Create a list of (x, y) coordinates for the isometric polygon from the rect above
        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]

        # This creates the coords for the tile image's top left corner
        minx = min([x for x, y in iso_poly])
        miny = min([y for x, y in iso_poly])

        # Randomly choose a tile type (image)
        r = random.randint(1, 100)
        if r<= 5:
            tile = 'tree'
        elif r<= 10:
            tile = 'rock'
        else:
            tile = ''

        out = {
            'grid': [grid_x, grid_y],
            'cart_rect': rect,
            'iso_poly': iso_poly,
            'render_pos': [minx, miny],  # top left
            'tile': tile  # image
        }

        return out

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y

    def load_images(self):
        block = pygame.image.load('assets/graphics/block.png').convert_alpha()
        tree = pygame.image.load('assets/graphics/tree.png').convert_alpha()
        rock = pygame.image.load('assets/graphics/rock.png').convert_alpha()

        return {'block': block,
                'tree': tree,
                'rock': rock}