import pygame

from widgets.button import Button
from materials.joint import Joint
from materials.beam import Beam

class GraphicsManager:
    def __init__(self, screen: pygame.display):
        self.__screen = screen

    def draw(self, obj):
        if Button in obj.__class__.__mro__:
            pygame.draw.rect(self.__screen, (50, 200, 130), obj.get_rect())

        if Joint in obj.__class__.__mro__:
            pygame.draw.circle(self.__screen, (50, 200, 130), obj.get_position(), obj.get_radius())

        if Beam in obj.__class__.__mro__:
            pygame.draw.line(self.__screen, (23, 68, 213), *obj.get_positions())