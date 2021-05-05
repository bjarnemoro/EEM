import numpy as np
class Joint(object):
    def __init__(self, x: float, y: float, radius: float = 10, anchor: bool = False):
        self.__x = x
        self.__y = y
        self.__radius = radius

        self.__x_displacement = 0
        self.__y_displacement = 0

        self.__anchor = anchor

    def get_position(self) -> np.ndarray:
        return np.array((self.__x + self.__x_displacement, self.__y + self.__y_displacement))

    def get_only_position(self) ->np.ndarray:
        return np.array((self.__x, self.__y))

    def get_radius(self):
        return self.__radius

    def set_position(self, x: float, y: float):
        self.__x = x
        self.__y = y

    def set_anchor(self, anchor: bool) -> None:
        self.__anchor = anchor

    @property
    def anchor(self):
        return self.__anchor

    def set_displacement(self, x: float, y: float) -> None:
        self.__x_displacement = x
        self.__y_displacement = y