import numpy as np
from materials.joint import Joint

class Beam:
    max_stress = 1e-7

    def __init__(self, joint1: Joint, joint2: Joint):
        self.__E_modulus = 210e3 #MPa
        """stores the parent beams"""
        if type(joint1) == Joint and type(joint2) == Joint:
            self.__joints = (joint1, joint2)
        else:
            raise ValueError("both parameters should be of type Joint")

    def get_positions(self) -> (np.ndarray, np.ndarray):
        return [self.__joints[i].get_position() for i in (0, 1)]

    def get_only_positions(self) -> (np.ndarray, np.ndarray):
        return [self.__joints[i].get_only_position() for i in (0, 1)]

    def get_positions_xxyy(self) -> (np.ndarray, np.ndarray):
        return [(e1, e2) for e1, e2 in zip(self.__joints[0].get_position(), self.__joints[1].get_position())]

    def get_joints(self) -> (Joint, Joint):
        return self.__joints

    def get_stress(self):
        pos1, pos2 = self.get_positions()
        opos1, opos2 = self.get_only_positions()

        regular_length = np.sqrt(np.sum((opos1 - opos2)**2))
        stressed_length = np.sqrt(np.sum((pos1 - pos2)**2))

        e = (stressed_length / regular_length) - 1
        stress = e * self.__E_modulus #MPa
        return abs(stress)