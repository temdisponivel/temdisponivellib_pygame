import pygame
from game import Game

class Configuration(object):
    """
    Class that contains useful configuration of the game.
    """

    instance = None

    def __init__(self,
                 screen_size=pygame.rect(640, 480),
                 full_screen=False,
                 surface_flags=0,
                 title="Game",
                 frame_cap=100,
                 mouse_visible=False):
        if Configuration.intance is None:
            Configuration.instance = self
        else:
            pass
        self._length_world_area = 100
        self._screen_size = screen_size
        self._title = title
        self._frame_cap = frame_cap
        self._mouse_visible = mouse_visible
        self._full_screen = full_screen
        self._surface_flags = surface_flags

    @property
    def title(self, title):
        return self._title

    @property.setter
    def title(self, title):
        self._title = title

    @property
    def screen_size(self):
        return self._screen_size

    @property.setter
    def screen_size(self, size):
        self._screen_size = size
        self.surface = pygame.display.set_mode(self.screen_size, self._surface_flags)

    @property
    def surface(self):
        return self._surface

    @property.setter
    def surface(self, surface):
        self._surface = surface

    @property
    def mouse_visible(self):
        return self._mouse_visible

    @property.setter
    def mouse_visible(self, mouse_visible):
        self._mouse_visible = mouse_visible
        pygame.mouse.set_visible(self.mouse_visible)

    @property
    def frame_cap(self):
        return self._frame_cap

    @property.setter
    def frame_cap(self, frame_cap):
        self._frame_cap = frame_cap

    @property
    def full_screen(self):
        return self._full_screen

    @property.setter
    def full_screen(self, full_screen):
        if full_screen:
            self._surface_flags |= pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        else:
            self._surface_flags &= ~pygame.FULLSCREEN | ~pygame.HWSURFACE | ~pygame.DOUBLEBUF
        self._full_screen = full_screen
        self._update_surface_mode()

    @property
    def surface_flags(self):
        return self._surface_flags

    @property.setter
    def surface_flags(self, flags):
        self._surface_flags = flags
        self._update_surface_mode()

    @property
    def length_world_area(self):
        return self._length_world_area

    def _update_surface_mode(self):
        Game.instance.surface = pygame.display.set_mode(self.screen_size, self.surface_flags)