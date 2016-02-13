from pygame import *
from gameobject import IUpdatable
from temdisponivellib_pygame.time import Time


class Game(object, IUpdatable):

    """
    A class that represents a game.
    It has the surface on which the game will be draw and all thing related with the game itself.
    It also handles the game loops, swaps the scenes and that kind of thing.
    """

    instance = None

    def __init__(self,
                 screen_size=pygame.rect(640, 480),
                 full_screen=False,
                 surface_flags=0,
                 title="Game",
                 frame_cap=100,
                 mouse_visible=False):
        if Game.instance is None:
            Game.instance = self
        else:
            pass
        super(IUpdatable, self).__init__()
        self._surface = None
        self._screen_size = screen_size
        self._title = title
        self._frame_cap = frame_cap
        self._mouse_visible = mouse_visible
        self._full_screen = full_screen
        self._running = False
        self._paused = False
        self._events = {}
        self._current_scene = None
        self._next_scene = None
        self._time = Time()

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
        self.surface = pygame.display.set_mode(self.screen_size)

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
        self._full_screen = full_screen
        self._update_surface_mode()

    def _update_surface_mode(self):
        attributes = 0
        if self.full_screen:
            attributes = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        pygame.display.set_mode(self.screen_size, attributes)

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
            if self._paused:
                continue
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

    def quit(self):
        """
        Close and finish the game
        :return: None
        """
        self._running = False
        self.pause(True)
        self.finish()

    @property
    def pause(self):
        return self._paused

    @property.setter
    def pause(self, pause):
        self._paused = pause

    @property
    def scene(self):
        return self._current_scene

    @property.setter
    def scene(self, scene):
        self._next_scene = scene

    @property
    def events(self):
        return self._events

    def _handle_event(self):
        self._events.clear()
        for event in pygame.event.get():
            if event.type == pygame.event.QUIT:
                self._running = False
                self.quit()
            else:
                self._events[event.type] = event