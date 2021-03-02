from configuration.configuration import Screens
from screens.abstract_screen import AbstractScreen

class ScreenManager:
    def __init__(self, config, 
                 beam_handler, 
                 joint_handler, 
                 kinetic_simulator, 
                 stress_simulator, 
                 menu_screen: AbstractScreen, 
                 sandbox_screen: AbstractScreen, 
                 simulation_screen: AbstractScreen,
                 settings_screen: AbstractScreen,
                 graphics_manager):
        #self.__simulation_screen = simulation_screen(config, kinetic_simulator, stress_simulator, graphics_manager)
        #self.__sandbox_screen = sandbox_screen(config, graphics_manager)
        
        #screens
        self.__menu_screen = menu_screen #AbstractScreen
        self.__sandbox_screen = sandbox_screen #AbstractScreen
        self.__simulation_screen = simulation_screen #AbstractScreen
        self.__settings_screen = settings_screen #AbstractScreen

        self.__config = config
        self.__graphics_manager = graphics_manager

        self.__screens = (
            self.__menu_screen,
            self.__simulation_screen,
            self.__sandbox_screen,
            self.__settings_screen,)

        #set current screen to the menu
        self.__current_screen = self.__screens[Screens.MENU]

    def draw(self) -> None:
        self.__current_screen.draw()

    def update(self, dt) -> None:
        self.__current_screen.update(dt)

    def key_input(self, key: int) -> None:
        self.__current_screen.key_input(key)

    def mouse_input(self, pos: tuple, button: int) -> None:
        self.__current_screen.mouse_input(pos, button)

    def set_screens(self, idx) -> None:
        if idx in Screens().get_tuple():
            self.__current_screen = self.__screens[idx]
        else:
            raise ValueError("{} not in the available screens".format(idx))