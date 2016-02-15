from pygame.rect import Rect
from temdisponivellib.component import Component


class Point(object):

    def __init__(self):
        super(Point, self).__init__()
        self._x = 0
        self._y = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self,  x):
        self._x =  x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y


class Transform(Point, Component):

    """
    Component that every game object has. It contains the position of the game object and some useful
    function for movimentation.
    """

    def __init__(self):
        super(Transform, self).__init__()