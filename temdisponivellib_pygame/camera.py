from pygame import Rect
from game import Game
from gameobject import IDrawable
from pygame import error as err


class Camera(object, Rect, IDrawable):
    """
    Class that represents a camera in game.
    A camera is used to draw just a portion of a level or object. A scene can have multiple Cameras.
    A camera will draw all objects that it is on sight (inside the rect that represents this camera).
    The camera itself doesn't have to fill all screen (it does by default), it can fill just a portion of the screen
    by changing its size and position.
    """

    def __init__(self, position=(0, 0), size=(Game.instance.screen_size.width, Game.instance.screen_size.height)):
        super(Rect, self).__init__(position, size)
        super(IDrawable, self).__init__()

    def in_sight(self, game_object):
        """
        Validate if a game object (or anything that have a Rect) is visible by this camera.
        :param object: Object (as a Rect) to validate visibility
        :return: True if it is visible. False otherwise.
        """
        return self.colliderect(game_object.rect)

    def draw(self):
        """
        Draws a game object (only when 'in_camera' is true) using this camera.
        :param source: Game object to draw.
        """
        game_objects = Game.instance.scene.get_objects_area(self)
        for game_object in game_objects:
            try:
                self.draw_game_object(game_object, False)
            except err, message:
                print err, message
                raise err

    def draw_game_object(self, game_object, validate_in_camera=True):
        """
        Draw a game object using this camera.
        :param game_object: Game object to be draw.
        :param validate_in_camera: If true, only draws the object if 'in_sight' is True.
        """
        if validate_in_camera and self.in_sight(game_object) \
                and game_object.is_drawing and game_object.image is not None:
            Game.instance.surface.blit(game_object.image, game_object.rect, game_object.rect.clip(self))