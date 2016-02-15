from timeutils import Time
from configuration import Configuration
import pygame
import errorutils


class Game(object):

    """
    A class that represents a game.
    It has the surface on which the game will be draw and all thing related with the game itself.
    It also handles the game loops, swaps the scenes and that kind of thing.
    """

    _instance = None

    def __init__(self):
        if Game._instance is None:
            Game._instance = self
        else:
            pass
        self._surface = None
        self._running = False
        self._events = {}
        self._current_scene = None
        self._next_scene = None

    def start(self):
        try:
            pygame.init()
            self.set_configuration()
        except:
            errorutils.handle_exception()

    def finish(self):
        try:
            if self._current_scene is not None:
                self._current_scene.finish()
            pygame.quit()
        except:
            errorutils.handle_exception()

    def play(self):
        """
        Start the game loop.
        This function only return when the quit method is called.
        :return:
        """
        self._running = True
        while self._running:
            try:
                Time.instance().update()
                self._handle_event()
                # just for safety
                if self.scene is not None:
                    self.scene.update()
                    self.scene.draw()
                    pygame.display.flip()
                    self.surface.fill(self.scene.background_color)

                if self._next_scene is not None:
                    if self.scene is not None:
                        self.scene.finish()
                    self._next_scene.start()
                    self._current_scene = self._next_scene
                    self._next_scene = None
            except:
                errorutils.handle_exception()
        try:
            self.quit()
        except:
            errorutils.handle_exception()


    def quit(self):
        """
        Close and finish the game
        :return: None
        """
        self._running = False
        self.finish()

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, surface):
        self._surface = surface

    @property
    def scene(self):
        """
        :return: Returns the current scene
        """
        return self._current_scene

    @scene.setter
    def scene(self, scene):
        """
        Set the next scene.
        :param scene: Scene to set.
        :return: None
        """
        self._next_scene = scene

    @property
    def events(self):
        """
        :return: A dictionary where the key is the type of the event and value is a list with all events
        of that type that occurs in this frame.
        """
        return self._events

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, surface):
        self._surface = surface

    def _handle_event(self):
        self._events.clear()
        for pyevent in pygame.event.get():
            if pyevent.type == pygame.QUIT:
                self._running = False
            else:
                self._events.setdefault(pyevent.type, [])
                self._events[pyevent.type].append(pyevent)

    def draw_something(self, drawable, position, area):
        """
        Draw something in screen. This function must be called inside "draw" lifecycle hook
        :param drawable: Something to draw
        :return: None
        """
        self.surface.blit(drawable, position, area)

    @staticmethod
    def instance():
        if Game._instance is None:
            Game()
        return Game._instance

    def set_configuration(self):
        """
        Updated screen and stuff based on the current configuration
        """
        self.surface = pygame.display.set_mode(Configuration.instance().screen_size,
                                                               Configuration.instance().surface_flags)