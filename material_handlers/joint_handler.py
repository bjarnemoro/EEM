from materials.joint import Joint

class JointHandler:
    def __init__(self):
        self.__joints = []

    def add_joint(self, joint: Joint):
        if Joint in joint.__class__.__mro__:
            self.__joints.append(joint)
        else:
            raise ValueError("parameter supposed to be of type Joint")

    def get_joints(self) -> list:
        return self.__joints

    def pop(self, idx) -> Joint:
        return self.__joints.pop(idx)