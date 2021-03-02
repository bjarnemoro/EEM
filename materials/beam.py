from materials.joint import Joint

class Beam:
    def __init__(self, joint1: Joint, joint2: Joint):
        """stores the parent beams"""
        if type(joint1) == Joint and type(joint2) == Joint:
            self.__joints = (joint1, joint2)
        else:
            raise ValueError("both parameters should be of type Joint")