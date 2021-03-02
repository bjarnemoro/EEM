
class Button(object):
    def __init__(self, x, y, width, height, command=None):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__command = command

    def get_clicked(self, pos: tuple) -> bool:
        x, y = pos
        return (abs(self.__x - x) < self.__width // 2) and (abs(self.__y - y) < self.__height // 2)
            
    def get_rect(self) -> tuple:
        return (self.__x - self.__width//2, self.__y - self.__height//2, self.__width, self.__height)

    def set_command(self, command):
        self.__command = command

    def run_command(self):
        if self.__command is not None:
            self.__command()
        else:
            raise ValueError("the command has not been set")