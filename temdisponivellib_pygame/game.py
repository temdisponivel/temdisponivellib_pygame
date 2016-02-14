from pygame import *
from gameobject import IUpdatable
from temdisponivellib_pygame.time import Time
from configuration import Configuration
from physics import Physics


class Game(object, IUpdatable):

    """
    A class that represents a game.
    It has the surface on which the game will be draw and all thing related with the game itself.
    It also handles the game loops, swaps the scenes and that kind of thing.
    """

    instance = None

    def __init__(self, configuration=Configuration):
        if Game.instance is None:
            Game.instance = self
        else:
            pass
        super(IUpdatable, self).__init__()
        self._surface = None
        self._running = False
        self._events = {}
        self._current_scene = None
        self._next_scene = None
        self._time = Time()
        self._frame_count = 0

    def start(self):
        pygame.init()
        self._update_surface_mode()

    def finish(self):
        if self._current_scene is not None:
            self._current_scene.finish()
        pygame.quit()

    def play(self):
        """
        Start the game loop.
        This function only return when the quit method is called.
        :return:
        """
        self._running = True
        while self._running:
            self._time.update()
            self._handle_event()
            # just for safety
            if self._current_scene is not None:
                try:
                    self._current_scene.update()
                    self.surface.fill(self.scene.background_color)
                    self._current_scene.draw()
                    pygame.display.flip()
                except error, message:
                    print error, message
            if self._next_scene is not None:
                try:
                    self._current_scene.finish()
                except error, message:
                    print error, message
                try:
                    self._next_scene.start()
                except error, message:
                    print error, message
                self._current_scene = self._next_scene
                self._next_scene = None
            self._frame_count += 1

    def quit(self):
        """
        Close and finish the game
        :return: None
        """
        self._running = False
        self.finish()

    @property
    def scene(self):
        return self._current_scene

    @property.setter
    def scene(self, scene):
        self._next_scene = scene

    @property
    def events(self):
        return self._events

    @property
    def surface(self):
        return self._surface

    @property.setter
    def surface(self, surface):
        self._surface = surface

    @property
    def frame_count(self):
        return self._frame_count

    def _handle_event(self):
        self._events.clear()
        for event in pygame.event.get():
            if event.type == pygame.event.QUIT:
                self._running = False
                self.quit()
            else:
                self._events[event.type] = event

    def draw_something(self, drawable, position, area):
        """
        Draw shomething in screen. This function must be called inside "draw" lifecycle hook
        :param drawable: Something to draw
        :return: None
        """
        self.surface.blit(drawable, position, area)