from pygame import Rect
from ..gameobject import Component
from ..configuration import Configuration

class Transform(object, Component, Rect):
    """
    Component that every game object has. It contains the position of the game object and some useful
    function for movimentation.
    """
    def __init__(self):
        super(Component, self).__init__()
        super(Rect, self).__init__()