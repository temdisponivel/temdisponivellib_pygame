from pygame.time import Clock

from gameobject import IUpdatable
from temdisponivellib_pygame.game import Game


class Time(IUpdatable, Clock):
    """
    A helper class for dealing with time.
    """
    instance = None

    def __init__(self):
        if Time.instance is None:
            Time.instance = self
        else:
            pass
        super(IUpdatable, self).__init__()
        super(Clock, self).__init__()
        self._delta_time = 0
        self._time_scale = 1

    def update(self):
        self._delta_time = self.tick(Game.instance.frame_cap)

    @property
    def delta_time(self):
        return self._delta_time / self.time_scale

    @property
    def time_scale(self):
        return self._time_scale

    @property
    def time_scale(self, time_scale):
        self._time_scale = time_scale