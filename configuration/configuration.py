class Screens:
    MENU = 0
    SIMULATION = 1
    SANDBOX = 2
    SETTINGS = 3
    

    def get_tuple(self) -> tuple:
        return (self.SIMULATION, self.SANDBOX, self.SETTINGS, self.MENU)

class Configuration:
    SCR_WIDTH = 900
    SCR_HEIGHT = 600

    FRAME_RATE_WAIT = 10

    #colors
    BACKGROUND_COLOR = (153, 186, 186)

    def __init__(self):
        pass