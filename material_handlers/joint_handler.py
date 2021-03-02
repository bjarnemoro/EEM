from materials.joint import Joint

class JointHandler:
    def __init__(self):
        self.__joints = []

    def add_joint(joint: Joint):
        if Joint in joint.__mro__:
            self.__joints.append(joint)
        else:
            raise ValueError("parameter supposed to be of type Joint")

    def get_joints(self) -> list:
        return self.__joints