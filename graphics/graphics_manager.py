import pygame

from widgets.button import Button

class GraphicsManager:
    def __init__(self, screen: pygame.display):
        self.__screen = screen

    def draw(self, obj):
        if Button in obj.__class__.__mro__:
            pygame.draw.rect(self.__screen, (50, 200, 130), obj.get_rect())