#  TODO: make all methods static

from pygame.time import Clock
from configuration import Configuration


class Time(object):
    """
    A helper class for dealing with time.
    """
    _instance = None

    def __init__(self):
        if Time._instance is None:
            Time._instance = self
        else:
            return
        self._delta_time = 0.0
        self._time_scale = 1.0
        self._clock = Clock()

    def update(self):
        self._delta_time = self._clock.tick(Configuration.instance().frame_cap) / 1000.0

    @property
    def delta_time(self):
        return self._delta_time

    @property
    def time_scale(self):
        return self._time_scale

    @time_scale.setter
    def time_scale(self, time_scale):
        self._time_scale = time_scale

    @property
    def clock(self):
        return self._clock

    @property
    def frame_rate(self):
        """
        :return: The frame rate which the game is current running.
        """
        return self._clock.get_fps()

    @staticmethod
    def instance():
        if Time._instance is None:
            Time._instance = Time()
        return Time._instance