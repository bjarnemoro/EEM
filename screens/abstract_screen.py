from abc import abstractmethod

class AbstractScreen:
    def __init__(self):
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def update(self, dt) -> None:
        pass

    @abstractmethod
    def key_input(self, key: int) -> None:
        pass

    @abstractmethod
    def mouse_input(self, pos: tuple, button: int) -> None:
        pass