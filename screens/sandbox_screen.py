import pygame
import numpy as np
import copy

from configuration.configuration import Screens
from screens.abstract_screen import AbstractScreen
from widgets.button import Button

from materials.joint import Joint
from materials.beam import Beam
from material_handlers.beam_handler import BeamHandler
from material_handlers.joint_handler import JointHandler

from tests.xy_movement_test import FEA

class SandboxScreen(AbstractScreen):
    def __init__(self, graphics_manager):
        self.__graphics_manager = graphics_manager
        self.__beam_handler = BeamHandler()
        self.__joint_handler = JointHandler()
        self.selected_joint = None

        self.__objects = (
            Button(500, 500, 100, 50, lambda: print("hello")),)

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
        
        if button == 1:
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
        if button == 2:
            clicked_joint = self.click_joint(pos)
            if clicked_joint is not None:
                clicked_joint.set_anchor(True)
        elif button == 3:
            self.selected_joint = None

    def key_input(self, key: int) -> None:
        chr_key = chr(key)
        if chr_key == 'z':
            joint = self.__joint_handler.pop(-1)
            self.__beam_handler.delete_by_joint(joint)
            self.selected_joint = None

        #simulate
        if chr_key == 's':
            beams = self.__beam_handler.get_beams()
            joints = self.__joint_handler.get_joints()

            #joints_copy = copy.deepcopy(joints)
            [joint.set_position(*(joint.get_only_position() / 100)) for joint in joints]

            anchor_indices = [i for i, joint in enumerate(joints) if joint.anchor == True]

            loads = np.zeros(shape=(len(joints)*2))
            loads[5] = 1e7 #N

            displacements_obj = FEA(joints, beams, anchor_indices, loads)

            [joint.set_displacement(*displacements_obj[i*2:(i+1)*2]*100) for i, joint in enumerate(joints)]
            [joint.set_position(*(joint.get_only_position() * 100)) for joint in joints]

            Beam.max_stress = max([b.get_stress() for b in beams]) + 1e-7

        if chr_key == 'r':
            joints = self.__joint_handler.get_joints()
            [joint.set_displacement(0, 0) for joint in joints]
                
    def set_commands(self, idxs: list, commands: list):
        for idx, command in zip(idxs, commands):
            self.__objects[idx].set_command(command)

    def click_joint(self, pos) -> (Joint, None):
        for joint in self.__joint_handler.get_joints():
            if np.sqrt(np.sum((joint.get_position() - pos)**2)) < 10:
                return joint

        return None