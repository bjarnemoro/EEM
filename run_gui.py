#Bjarne Moro
#
#In this project I will try to implement e.e.m
#It contains an editor to create beam structures
#It will also contain a simulator in order to 
#simulate stress and movement on those beam structures
#
#e.e.m works as follows
#   1. seperate the construction into subsections
#   2. try to fomulate the movements that can happen within those subsections
#   3. Formulate the coordinates with freedom of movement as a parameter
#   4. use hookes law to 
#   5.
#
#EI/l * K = u * f
#
#
#http://www.mate.tue.nl/~devree/Eem_diktaat.pdf

import numpy as np
import pygame

from screen_manager import ScreenManager
from configuration.configuration import Configuration, Screens
from material_handlers.joint_handler import JointHandler
from material_handlers.beam_handler import BeamHandler
from screens.menu_screen import MenuScreen
from screens.abstract_screen import AbstractScreen
from screens.sandbox_screen import SandboxScreen
from screens.simulation_screen import SimulationScreen
from graphics.graphics_manager import GraphicsManager


def main():
    #define all major classes
    config = Configuration()
    beam_handler = BeamHandler()
    joint_handler = JointHandler()
    kinetic_simulator = None
    stress_simulator = None
    
    screen = pygame.display.set_mode((config.SCR_WIDTH, config.SCR_HEIGHT))
    graphics_manager = GraphicsManager(screen)

    menu_screen = MenuScreen(graphics_manager)
    sandbox_screen = SandboxScreen(graphics_manager)
    simulation_screen = SimulationScreen(graphics_manager, kinetic_simulator)
    settings_screen = AbstractScreen()
    
    screen_manager = ScreenManager(config,
                                   beam_handler,
                                   joint_handler,
                                   kinetic_simulator, 
                                   stress_simulator, 
                                   menu_screen,
                                   sandbox_screen, 
                                   simulation_screen,
                                   settings_screen,
                                   graphics_manager)

    menu_screen.set_commands((0,1,2), (lambda: screen_manager.set_screens(1), lambda: screen_manager.set_screens(2), lambda: screen_manager.set_screens(3)))


    #define the main pygame cycle
    done = False
    dt = 0
    while not done:
        #calculate delta time
        current_time = pygame.time.get_ticks()

        #get all values of the callback functions
        events = pygame.event.get()
        for event in events:
            if pygame.QUIT == event.type:
                done = True
            elif pygame.KEYUP == event.type:
                screen_manager.key_input(event.key)
            elif pygame.MOUSEBUTTONDOWN == event.type:
                screen_manager.mouse_input(event.pos, event.button)

        #update your current screen
        screen_manager.update(dt)

        #draw your current screen
        screen.fill(config.BACKGROUND_COLOR)
        screen_manager.draw()

        #pygame updates
        pygame.display.update()
        pygame.time.wait(config.FRAME_RATE_WAIT)

        #calculate delte time
        dt = pygame.time.get_ticks() - current_time
        

if __name__ == "__main__":
    main()