import pygame as pg
import pygame.image
import random
import noise

from .settings import TILE_SIZE

class World:
    def __init__(self, grid_length_x, grid_length_y, width, height):
        self.grid_lenth_x = grid_length_x
        self.grid_lenth_y = grid_length_y
        self.width = width
        self.height = height
        self.perlin_scale = grid_length_x / 2

        # Creates a surface to draw to the screen to avoid needing to iterate through each grass block tile
        # Instead just draw this one surface which contains all the grass block tiles
        # The width is the total amount of tiles * tile width * 2 since the isometric poly had 2 times the width of a cartesian rectangle
        # The y gets an additional offset since the horizontal of the iso surface is longer than 1 edge of the cartesian surface rect
        self.grass_tiles = pg.Surface((grid_length_x * TILE_SIZE * 2, grid_length_y * TILE_SIZE + 8 * TILE_SIZE)).convert_alpha()
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
                # x values must be positive to blit onto the surface so we offset x to make them positive
                self.grass_tiles.blit(self.tiles['block'], (render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))

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
        perlin = 100 * noise.pnoise2(grid_x / self.perlin_scale, grid_y/self.perlin_scale)

        if perlin >= 15 or perlin <= -35:
            tile = 'tree'
        else:
            if r == 1:
                tile = 'tree'
            elif r<= 2:
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