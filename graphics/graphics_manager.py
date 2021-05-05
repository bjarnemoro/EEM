import pygame
import numpy as np

from widgets.button import Button
from materials.joint import Joint
from materials.beam import Beam

class GraphicsManager:
    def __init__(self, screen: pygame.display):
        self.__screen = screen

        self.__stressed = np.array([201, 66, 24])
        self.__not_stressed = np.array((23, 68, 213))

    def draw(self, obj):
        if Button in obj.__class__.__mro__:
            pygame.draw.rect(self.__screen, (50, 200, 130), obj.get_rect())

        if Joint in obj.__class__.__mro__:
            if obj.anchor != True:
                pygame.draw.circle(self.__screen, (50, 200, 130), obj.get_position().astype(int), obj.get_radius())
            else:
                pygame.draw.circle(self.__screen, (201, 66, 24), obj.get_position().astype(int), obj.get_radius())

        if Beam in obj.__class__.__mro__:
            stress = obj.get_stress()
            norm_stress = stress / Beam.max_stress
            color = self.__not_stressed + norm_stress * (self.__stressed - self.__not_stressed)
            pygame.draw.line(self.__screen, color, *obj.get_positions())