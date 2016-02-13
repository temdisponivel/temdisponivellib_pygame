from pygame import Rect
from ..gameobject import Component


class Transform(object, Component, Rect):

    def __init__(self):
        super(Component, self).__init__()
        super(Rect, self).__init__()