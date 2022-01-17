import pygame as pg
from game.game import Game

def main() -> None:
    # Differentiates between being at the loading menu (running) and the game running (playing)
    running = True
    playing = True

    # Initialize pygame
    pg.init()
    pg.mixer.init()

    screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
    clock = pg.time.Clock()

    # implement menus

    # implement game
    game = Game(screen, clock)

    while running:
        # start menu here

        while playing:
            # game loop here
            game.run()

if __name__ == '__main__':
    main()


