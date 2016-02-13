from pygame import Rect
from ..game import Game
from ..gameobject import IDrawer
from ..gameobject import IDrawable
from ..gameobject import Component


class Camera(object, Component, Rect, IDrawer):
    """
    Class that represents a camera in game. This class is a initial simple camera. In future, hopefully,
    this will have lots of more features.
    A camera is used to draw just a portion of a level or object. A scene can have multiple Cameras.
    A camera will draw all objects that it is on sight (inside the rect that represents this camera).
    The camera itself doesn't have to fill all screen (it does by default), it can fill just a portion of the screen
    by changing its size and position.
    """

    def __init__(self, position=(0, 0), size=(Game.instance.screen_size.width, Game.instance.screen_size.height)):
        super(Component, self).__init__()
        super(Rect, self).__init__(position, size)
        super(IDrawer, self).__init__()

    def in_sight(self, game_object):
        """
        Validate if a game object (or anything that have a Rect) is visible by this camera.
        :param object: Object (as a Rect) to validate visibility
        :return: True if it is visible. False otherwise.
        """
        return game_object.get_component(IDrawable) is not None and self.colliderect(game_object.get_drawable.get_rect)

    def draw(self):
        """
        Draws a game object (only when 'in_camera' is true) using this camera.
        :param source: Game object to draw.
        """
        game_objects_drawable = Game.instance.scene.get_drawables
        for game_object in game_objects_drawable:
            self.draw_game_object(game_object, True)

        # Waiting to integrate with a physics engine to get object in area of collision and draw only them
        #
        # game_objects_area = Game.instance.scene.get_objects_area(self)
        # game_objects_drawable = Game.instance.scene.get_drawables
        #
        # for game_object_a, game_object_d in zip(game_objects_area, game_objects_drawable):
        #     try:
        #         self.draw_game_object(game_object_d, False)
        #     except err, message:
        #         print err, message
        #         raise err
        #

    def draw_game_object(self, game_object, validate_in_camera=True):
        """
        Draw a game object using this camera.
        :param game_object: Game object to be draw.
        :param validate_in_camera: If true, only draws the object if 'in_sight' is True.
        """
        if validate_in_camera and self.in_sight(game_object) and game_object.is_drawing:
            drawable = game_object.get_drawable
            Game.instance.surface.blit(game_object.get_drawable, game_object.rect, game_object.rect.clip(self))

    def full_surface(self):
        self.width = Game.instance.screen_size.width
        self.height = Game.instance.screen_size.height
        self.top = 0
        self.left = 0