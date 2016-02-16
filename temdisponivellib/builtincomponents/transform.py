#  TODO: make the transform have a vec2d, not be one. Also make some properties like forward and such

from temdisponivellib.component import Component
from temdisponivellib.mathutils import *


class Transform(Vec2d, Component):

    """
    Component that every game object has. It contains the position of the game object and some useful
    function for movimentation.
    """

    def __init__(self):
        super(Transform, self).__init__()