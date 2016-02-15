#  TODO: validate cropped rect for bliting area when object has y or x negatives

from pygame import Rect
from temdisponivellib.game import Game
from temdisponivellib.configuration import Configuration
from temdisponivellib.contracts import IDrawer
from temdisponivellib.contracts import IDrawable
from temdisponivellib.component import Component


class Camera(Component, IDrawer):
    """
    Class that represents a camera in game. This class is a initial simple camera. In future, hopefully,
    this will have lots of more features.
    A camera is used to draw just a portion of a level or object. A scene can have multiple Cameras.
    A camera will draw all objects that it is on sight (inside the rect that represents this camera).
    The camera itself doesn't have to fill all screen (it does by default), it can fill just a portion of the screen
    by changing its size and position.
    """

    def __init__(self, size=(0, 0)):
        super(Camera, self).__init__()
        self._rect = Rect((0, 0), size)
        self._rect.size = size

    def in_sight(self, game_object):

        """
        Validate if a game object is visible by this camera.
        :param game_object: Game object to validate if it is on sight
        :return: True if it is visible. False otherwise.
        """

        return game_object.get_component(IDrawable) is not None and self._rect.collidedict(
            game_object.get_component(IDrawable).get_rect)

    def update(self):
        self._rect.x = self.transform.x
        self._rect.y = self.transform.y

    def draw(self):
        """
        Draws a game object (only when 'in_camera' is true) using this camera.
        """
        game_objects_drawable = Game.instance().scene.get_drawables
        for game_object in game_objects_drawable:
            self.draw_game_object(game_object, True)

    def draw_game_object(self, game_object, validate_in_camera=True):
        """
        Draw a game object using this camera.
        :param game_object: Game object to be draw.
        :param validate_in_camera: If true, only draws the object if 'in_sight' is True.
        """
        if not validate_in_camera and self.in_sight(game_object) and game_object.get_component(IDrawable).is_drawing:
            return
        position = (game_object.transform.x, game_object.transform.y)
        component = game_object.get_component(IDrawable)
        clipped = component.drawable.get_rect(topleft=position).clip(self._rect)
        Game.instance().surface.blit(component.drawable,
                                     position,
                                     (0, 0, clipped.width, clipped.height))

    @property
    def size(self):
        return self._rect.size

    @size.setter
    def size(self, size):
        self._rect = size

    def full_surface(self):
        self.transform.x = 0
        self.transform.y = 0
        self._rect.width = Configuration.instance().screen_size.width
        self._rect.height = Configuration.instance().screen_size.height