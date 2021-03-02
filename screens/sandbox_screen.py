import pygame
import numpy as np

from configuration.configuration import Screens
from screens.abstract_screen import AbstractScreen
from widgets.button import Button

from materials.joint import Joint
from materials.beam import Beam
from material_handlers.beam_handler import BeamHandler
from material_handlers.joint_handler import JointHandler

class SandboxScreen(AbstractScreen):
    def __init__(self, graphics_manager):
        self.__graphics_manager = graphics_manager
        self.__beam_handler = BeamHandler()
        self.__joint_handler = JointHandler()
        self.selected_joint = None

        self.__objects = (
            Button(500, 500, 100, 50),)

    def draw(self):
        for obj in self.__objects:
            self.__graphics_manager.draw(obj)

        for joint in self.__joint_handler.get_joints():
            self.__graphics_manager.draw(joint)

        for beam in self.__beam_handler.get_beams():
            self.__graphics_manager.draw(beam)

    def mouse_input(self, pos, button):
        """
        place joints and anchors on clicked position, expected behaviour is 
        placing joint when clicked. Place beam between newly placed joint and selected joint
        use right mouse button to unselect a joint or make joint an anchor
        """
        for obj in self.__objects:
            if obj.get_clicked(pos):
                obj.run_command()
        
        if button in (1, 2):
            clicked_joint = self.click_joint(pos)
            if clicked_joint is None:
                new_joint = Joint(*pos, 10)
                self.__joint_handler.add_joint(new_joint)
                if self.selected_joint is not None:
                    self.__beam_handler.add_beam(Beam(new_joint, self.selected_joint))
                self.selected_joint = new_joint
            else:
                if self.selected_joint is not None:
                    self.__beam_handler.add_beam(Beam(self.selected_joint, clicked_joint))
                self.selected_joint = clicked_joint
        elif button == 3:
            self.selected_joint = None

    def key_input(self, key: int) -> None:
        chr_key = chr(key)
        if chr_key == 'z':
            joint = self.__joint_handler.pop(-1)
            self.__beam_handler.delete_by_joint(joint)
            self.selected_joint = None
                
    def set_commands(self, idxs: list, commands: list):
        for idx, command in zip(idxs, commands):
            self.__objects[idx].set_command(command)

    def click_joint(self, pos) -> (Joint, None):
        for joint in self.__joint_handler.get_joints():
            if np.sqrt(np.sum((joint.get_position() - pos)**2)) < 10:
                return joint

        return None