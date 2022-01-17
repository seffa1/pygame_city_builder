import pygame as pg
from .settings import TILE_SIZE

class World:
    def __init__(self, grid_length_x, grid_length_y, width, height):
        self.grid_lenth_x = grid_length_x
        self.grid_lenth_y = grid_length_y
        self.width = width
        self.height = height
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

        return world

    def grid_to_world(self, grid_x, grid_y):
        """Transforms grid coordinates to tile elements"""
        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]

        out = {
            'grid': [grid_x, grid_y],
            'cart_rect': rect
        }

        return out