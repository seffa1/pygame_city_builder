import pygame as pg


class Camera:
    def __init__(self, width, height):
        # Screen settings to detect when to move the camera
        self.width = width
        self.height = height

        # Keeps track of how much the camera moved so the rest of the game world can move with it
        # In the opposite direction
        self.scroll = pg.Vector2(0, 0)
        self.dx = 0
        self.yx = 0
        self.speed = 25

    def update(self):
        # Extract the mouse's positions
        mouse_pos = pg.mouse.get_pos()

        # If the x pos of the mouse is within 3% of the right edge of the screen
        if mouse_pos[0] > self.width * 0.97:
            # Change in x will be in the opposite direction at the speed
            self.dx = -self.speed
        # If the x pos of the mouse is within 3% of the left edge of the screen
        elif mouse_pos[0] < self.width * 0.03:
            # Change in x will be in the opposite direction at the speed
            self.dx = self.speed
        # If the mouse is not at the left or right edge, the change is x will be 0
        else:
            self.dx = 0

        # Same logic as above but for y
        if mouse_pos[1] > self.height * 0.97:
            self.dy = -self.speed
        elif mouse_pos[1] < self.height * 0.03:
            self.dy = self.speed
        else:
            self.dy = 0

        # Update the camera scroll
        self.scroll.x += self.dx
        self.scroll.y += self.dy

