import pygame
import pygame as pg
import sys
from .world import World
from .settings import TILE_SIZE

# LEFT OFF AT PART 2: 11:40
# MAKE  SURE TO PUSH CHANGES!!!!!

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.world = World(10, 10, self.width, self.height)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        for x in range(self.world.grid_lenth_x):
            for y in range(self.world.grid_lenth_y):
                sq = self.world.world[x][y]['cart_rect']
                rect = pg.Rect(sq[0][0], sq[0][1], TILE_SIZE, TILE_SIZE)
                pg.draw.rect(self.screen, (0, 0, 255), rect, 1)

                # Gets the minx, miny for each polygon. This is the top left corner of the square around the polygon
                render_pos = self.world.world[x][y]['render_pos']

                # Draws the block image at the render position, with the needed offset
                self.screen.blit(self.world.tiles['block'], (render_pos[0] + self.width/2, render_pos[1] + self.height/4))

                # Gets the tile (image) for the current tile and draws that image if its not blank over the block
                tile = self.world.world[x][y]['tile']
                if tile != '':
                    # Offsets the images to draw the objects on top of the screen
                    self.screen.blit(self.world.tiles[tile],
                                    (render_pos[0] + self.width/2,
                                     render_pos[1] + self.height/4 - (self.world.tiles[tile].get_height() - TILE_SIZE)))

                # Extracts polygon coords from world and offsets them to the middle of the screen and draws them
                poly = self.world.world[x][y]['iso_poly']
                poly = [(x + self.width/2, y + self.height/4) for x, y in poly]
                pg.draw.polygon(self.screen, (255, 0, 0), poly, 1)


        pg.display.flip()