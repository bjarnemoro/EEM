import pygame
import numpy as np

from configuration.configuration import Screens
from configuration.configuration import Configuration as c
from screens.abstract_screen import AbstractScreen
from widgets.button import Button

from materials.joint import Joint
from materials.beam import Beam
from material_handlers.beam_handler import BeamHandler
from material_handlers.joint_handler import JointHandler

class SimulationScreen(AbstractScreen):
    def __init__(self, graphics_manager, kinetic_simulator):
        self.__graphics_manager = graphics_manager

        self.__beam_handler = BeamHandler()
        self.__joint_handler = JointHandler()

        joint1 = Joint(c.SCR_WIDTH//2, 100, c.JOINT_RADIUS)
        self.__joint2 = Joint(c.SCR_WIDTH//2 - 200, 100 + 200, c.JOINT_RADIUS)
        self.__joint_handler.add_joint(joint1)
        self.__joint_handler.add_joint(self.__joint2)

        self.__theta = np.pi/4
        self.__alpha = 0.001
        self.__nu = 0

    def draw(self):
        for joint in self.__joint_handler.get_joints():
            self.__graphics_manager.draw(joint)

        for beam in self.__beam_handler.get_beams():
            self.__graphics_manager.draw(beam)

    def update(self, dt):
        self.__nu, self.__theta = numeriek(self.__alpha, self.__nu, self.__theta, dt/10)
        self.__alpha = np.cos(self.__theta)*0.01

        self.__joint2.set_position(int(100 * np.cos(self.__theta) + c.SCR_WIDTH//2), int(100 * np.sin(self.__theta) + 100))
        print(self.__joint2.get_position())

    def mouse_input(self, pos, button):
        pass

def numeriek(alpha, nu, theta, dt):
    _nu = nu + alpha * dt
    _theta = theta + _nu*dt

    return _nu, _theta