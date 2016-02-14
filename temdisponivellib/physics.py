"""
This is a temporary class. In future, hopefully, we will integrate a physics engine (box2d most probably)
"""

from builtin_components.collider import Collider
from gameobject import IUpdatable
from gameobject import IDrawable
from game import Game
from configuration import Configuration
from component import Component
from pygame import draw


class Physics(IUpdatable, IDrawable):

    """
    Class that handles some physics functions.
    """

    _instance = None

    def __init__(self):
        super(IUpdatable, self).__init__()
        super(IDrawable, self).__init__()
        if Physics._instance is None:
            Physics._instance = self
        else:
            pass
        self._draw_colliders = False
        self._active_collisions = {}
        self._debug_color = (1, 0, 0)

    def update(self):
        if Game.instance().frame_count % Configuration.instance().collision_check_rate == 0:
            self.check_collision()

    def draw(self):
        if not self.draw_colliders:
            pass
        colliders = Collider.get_colliders()
        for collider in colliders:
            if collider.collider_type == Collider.BOX:
                draw.rect(Game.instance().surface, self._debug_color, collider.as_rect, 5)
            else:
                draw.circle(Game.instance().surface, self._debug_color, (collider.x, collider.y), collider.radius, 5)

    def check_collision(self):
        """
        Collides all colliders that ara in same region
        :return:
        """
        colliders = Collider.get_colliders()
        for list_colliders in colliders:
            length = len(list_colliders)
            for i in range(length):
                if i >= length:
                    break
                collider_a = list_colliders[i]
                collider_b = list_colliders[i + 1]
                key_a = (collider_a.game_object.id, collider_b.game_object.id)
                key_b = (collider_b.game_object.id, collider_a.game_object.id)
                if collider_a.check_collision(collider_b):
                    if key_a in self._active_collisions:
                        callback = "collision_stay"
                    elif key_b in self._active_collisions:
                        callback = "collision_stay"
                    else:
                        callback = "collision_enter"
                        self._active_collisions[key_a] = (collider_a, collider_b)
                else:
                    if key_a in self._active_collisions:
                        callback = "collision_exit"
                        del self._active_collisions[key_a]
                    elif key_b in self._active_collisions:
                        callback = "collision_exit"
                        del self._active_collisions[key_b]
                if callback is None:
                    self._call_callback(callback, collider_a, collider_b)

    def _call_callback(self, callback, collider_a, collider_b):
        for cls in Component.get_class_by_callback(callback):
            comp_a = collider_a.get_component(cls)
            comp_b = collider_b.get_component(cls)
            if comp_a is not None:
                if callback == "collider_enter":
                    comp_a.collider_enter(collider_b)
                elif callback == "collider_stay":
                    comp_a.collider_stay(collider_b)
                elif callback == "collider_exit":
                    comp_a.collider_exit(collider_b)
            if comp_b is not None:
                if callback == "collider_enter":
                    comp_b.collider_enter(comp_a)
                elif callback == "collider_stay":
                    comp_b.collider_stay(comp_a)
                elif callback == "collider_exit":
                    comp_b.collider_exit(comp_a)

    @property
    def draw_colliders(self):
        return self._draw_colliders

    @draw_colliders.setter
    def draw_colliders(self, draw_colliders):
        self._draw_colliders = draw_colliders

    @property
    def debug_color(self):
        return self._debug_color

    @debug_color.setter
    def debug_color(self, color):
        self._debug_color = color

    @property
    def active_collision(self):
        """
        :return: A dict (key: game_object_a.id, game_object_b.id, value: game_object_a, game_object_b) containing
        all active collisions
        """
        return self._active_collisions

    @staticmethod
    def instance():
        if Physics._instance is None:
            Physics._instance = Game()
        return Physics._instance