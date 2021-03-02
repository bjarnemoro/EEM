import numpy as np
class Joint(object):
    def __init__(self, x: float, y: float, radius: float):
        self.__x = x
        self.__y = y
        self.__radius = radius

    def get_position(self) -> np.ndarray:
        return np.array((self.__x, self.__y))

    def get_radius(self):
        return self.__radius