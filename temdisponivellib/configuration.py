from pygame import Rect
import pygame
import game


class Configuration(object):
    """
    Class that contains useful configuration of the game.
    """

    _instance = None

    def __init__(self,
                 screen_size=Rect(640, 480, 0, 0),
                 full_screen=False,
                 surface_flags=0,
                 title="Game",
                 frame_cap=100,
                 mouse_visible=False,
                 collision_check_rate=3):
        if Configuration._instance is None:
            Configuration._instance = self
        else:
            pass
        self._length_world_area = 100
        self._screen_size = screen_size
        self._title = title
        self._frame_cap = frame_cap
        self._mouse_visible = mouse_visible
        self._full_screen = full_screen
        self._surface_flags = surface_flags
        self._collision_check_rate = collision_check_rate
        self._frame_cap = 100

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title
        pygame.display.set_caption(self.title)

    @property
    def screen_size(self):
        return self._screen_size

    @screen_size.setter
    def screen_size(self, size):
        self._screen_size = size
        Configuration._instance.set_configuration()

    @property
    def mouse_visible(self):
        return self._mouse_visible

    @mouse_visible.setter
    def mouse_visible(self, mouse_visible):
        self._mouse_visible = mouse_visible
        pygame.mouse.set_visible(self.mouse_visible)

    @property
    def frame_cap(self):
        return self._frame_cap

    @frame_cap.setter
    def frame_cap(self, frame_cap):
        self._frame_cap = frame_cap

    @property
    def full_screen(self):
        return self._full_screen

    @full_screen.setter
    def full_screen(self, full_screen):
        if full_screen:
            self._surface_flags |= pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        else:
            self._surface_flags &= ~pygame.FULLSCREEN | ~pygame.HWSURFACE | ~pygame.DOUBLEBUF
        self._full_screen = full_screen
        Configuration._instance.set_configuration()

    @property
    def surface_flags(self):
        return self._surface_flags

    @surface_flags.setter
    def surface_flags(self, flags):
        self._surface_flags = flags
        Configuration._instance.set_configuration()

    @property
    def collision_check_rate(self):
        return self._collision_check_rate

    @collision_check_rate.setter
    def collision_check_rate(self, rate):
        self._collision_check_rate = rate

    @property
    def length_world_area(self):
        return self._length_world_area

    @property
    def frame_cap(self):
        """
        :return: Frame cap. The frame  cap determines the maximum of cycles that the game perform in one second
        """
        return self._frame_cap

    @frame_cap.setter
    def frame_cap(self, frame_cap):
        self.frame_cap = frame_cap

    @staticmethod
    def instance():
        if Configuration._instance is None:
            Configuration()
        return Configuration._instance

    @staticmethod
    def set_configuration():
        """
        Updated screen and stuff based on the current configuration
        """
        game.Game.instance().surface = pygame.display.set_mode(Configuration._instance.screen_size,
                                                               Configuration._instance.surface_flags)