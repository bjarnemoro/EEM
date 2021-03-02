import pygame

from configuration.configuration import Screens
from screens.abstract_screen import AbstractScreen
from widgets.button import Button

class MenuScreen(AbstractScreen):
    def __init__(self, graphics_manager):
        self.__graphics_manager = graphics_manager

        self.__objects = (
            Button(200, 200, 100, 50),
            Button(500, 200, 100, 50),
            Button(500, 500, 100, 50))

    def draw(self):
        for obj in self.__objects:
            self.__graphics_manager.draw(obj)

    def mouse_input(self, pos, button):
        for obj in self.__objects:
            if obj.get_clicked(pos):
                obj.run_command()
            
    def set_commands(self, idxs: list, commands: list):
        for idx, command in zip(idxs, commands):
            self.__objects[idx].set_command(command)
