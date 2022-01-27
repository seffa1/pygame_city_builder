import pygame as pg
import pygame.image
import random
import noise

from .settings import TILE_SIZE

class World:
    def __init__(self, hud, grid_length_x, grid_length_y, width, height):
        self.hud = hud
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

        self.temp_tile = None
        self.examine_tile = None


    def update(self, camera):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        # If we right click, drop the selected tile
        if mouse_action[2]:
            self.examine_tile = None
            self.hud.examined_tile = None

        if self.hud.selected_tile is not None:
            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)

            self.temp_tile = None
            if self.can_place_tile(grid_pos):

                img = self.hud.selected_tile['image'].copy()
                img.set_alpha(100)

                render_pos = self.world[grid_pos[0]][grid_pos[1]]['render_pos']
                iso_poly = self.world[grid_pos[0]][grid_pos[1]]['iso_poly']
                collision = self.world[grid_pos[0]][grid_pos[1]]['collision']

                self.temp_tile = {
                    'image': img,
                    'render_pos': render_pos,
                    'iso_poly': iso_poly,
                    'collision': collision
                }

                # Left click
                if mouse_action[0] and not collision:
                    self.world[grid_pos[0]][grid_pos[1]]['tile'] = self.hud.selected_tile['name']
                    self.world[grid_pos[0]][grid_pos[1]]['collision'] = True
                    self.hud.selected_tile = None

        # If the tile we select has an object on it, make it our examined tile
        else:
            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)

            if self.can_place_tile(grid_pos):
                # Check if tile contains an object
                collision = self.world[grid_pos[0]][grid_pos[1]]['collision']

                if mouse_action[0] and collision:
                    self.examine_tile = grid_pos
                    self.hud.examined_tile = self.world[grid_pos[0]][grid_pos[1]]





    def draw(self, screen, camera):
        # With draw the world where the camera scroll is currently at, so the world moves with the camera
        screen.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))

        for x in range(self.grid_lenth_x):
            for y in range(self.grid_lenth_y):
                # This draws the original cartesion grid
                # sq = self.world.world[x][y]['cart_rect']
                # rect = pg.Rect(sq[0][0], sq[0][1], TILE_SIZE, TILE_SIZE)
                # pg.draw.rect(self.screen, (0, 0, 255), rect, 1)

                # Gets the minx, miny for each polygon. This is the top left corner of the square around the polygon
                render_pos = self.world[x][y]['render_pos']

                # We are no longer drawing each grass block iteratively, instead we draw a surface shown before this nested loop
                # self.screen.blit(self.world.tiles['block'], (render_pos[0] + self.width/2, render_pos[1] + self.height/4))

                # Gets the rock or tree image for the current tile and draws that image if its not blank over the block
                tile = self.world[x][y]['tile']
                if tile != '':
                    # Offsets the rock or tree image to draw the objects on top of the grass blocks
                    # And also offsets them based on the camera's scroll position
                    screen.blit(self.tiles[tile],
                                     (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                      render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))

                    # Draws the outline of selected objects
                    if self.examine_tile is not None:
                        if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                            mask = pg.mask.from_surface(self.tiles[tile]).outline()
                            mask = [(x + render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                     y + render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y) for x, y in mask]
                            pg.draw.polygon(screen, (255, 255, 255), mask, 3)


                # Extracts polygon coords from world and offsets them to the middle of the screen and draws them
                # Drawing an outline of the iso grid, no longer needed
                # poly = self.world.world[x][y]['iso_poly']
                # poly = [(x + self.width/2, y + self.height/4) for x, y in poly]
                # pg.draw.polygon(self.screen, (255, 0, 0), poly, 1)

        if self.temp_tile is not None:
            iso_poly = self.temp_tile['iso_poly']
            iso_poly = [(x + self.grass_tiles.get_width()/2 + camera.scroll.x, y + camera.scroll.y) for x, y in iso_poly]
            if self.temp_tile['collision']:
                pg.draw.polygon(screen, (255, 0, 0), iso_poly, 3)
            else:
                pg.draw.polygon(screen, (255, 255, 255), iso_poly, 3)
            render_pos = self.temp_tile['render_pos']
            screen.blit(self.temp_tile['image'],
                        (render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x,
                         render_pos[1] - (self.temp_tile['image'].get_height() - TILE_SIZE)+ camera.scroll.y))

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
            'tile': tile,  # image
            'collision': False if tile == '' else True
        }

        return out

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y

    def mouse_to_grid(self, x, y, scroll):
        # transform to world position (removing camera scroll and offset)
        world_x = x - scroll.x - self.grass_tiles.get_width()/2
        world_y = y - scroll.y
        # transform to cart (inverse of cart_to_iso)
        cart_y = (2 * world_y - world_x)/2
        cart_x = (cart_y + world_x)
        # transform to grid coords
        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)
        return grid_x, grid_y

    def load_images(self):
        block = pygame.image.load('assets/graphics/block.png').convert_alpha()
        # Read images
        building1 = pg.image.load('assets/graphics/building01.png').convert_alpha()
        building2 = pg.image.load('assets/graphics/building02.png').convert_alpha()
        tree = pg.image.load('assets/graphics/tree.png').convert_alpha()
        rock = pg.image.load('assets/graphics/rock.png').convert_alpha()

        images = {
            'building1': building1,
            'building2': building2,
            'tree': tree,
            'rock': rock,
            'block': block
        }
        return images

    def can_place_tile(self, grid_pos):
        mouse_on_panel = False
        for rect in [self.hud.resources_rect, self.hud.build_rect, self.hud.select_rect]:
            if rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = True

        world_bounds = (0 <= grid_pos[0] <= self.grid_lenth_x) and (0 <= grid_pos[1] <= self.grid_lenth_y)

        if world_bounds and not mouse_on_panel:
            return True
        else:
            return False