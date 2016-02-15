"""
This is a temporary class. In future, hopefully, we will integrate a physics engine (box2d most probably)
"""

from builtincomponents.collider import Collider
from configuration import Configuration
from component import Component


class Physics(object):

    """
    Class that handles some physics functions.
    """

    _instance = None

    def __init__(self):
        if Physics._instance is None:
            Physics._instance = self
        else:
            pass
        self._active_collisions = {}
        self._frame_count = 0

    def update(self):
        if self._frame_count % Configuration.instance().collision_check_rate == 0:
            self.check_collision()
        self._frame_count += 1

    def check_collision(self):
        """
        Collides all colliders that ara in same region
        :return:
        """
        print "COLLING"
        print "---------------------------------------------------------------------------"
        colliders = Collider.get_colliders()
        for list_colliders in colliders:
            print "COLLING ANOTHER AREA"
            print "---------------------------------------------------------------------------"
            length = len(list_colliders)
            for i in range(length):
                for j in range(i + 1, length):
                    if j == length - 1:
                        break
                    collider_a = list_colliders[i]
                    collider_b = list_colliders[j]
                    key_a = (collider_a.game_object.id, collider_b.game_object.id)
                    key_b = (collider_b.game_object.id, collider_a.game_object.id)
                    callback = None
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
                    if callback is not None:
                        self._call_callback(callback, collider_a, collider_b)

    def _call_callback(self, callback, collider_a, collider_b):
        for cls in Component.get_class_by_callback(callback):
            comp_a = collider_a.get_component(cls)
            comp_b = collider_b.get_component(cls)
            if comp_a is not None:
                getattr(comp_a, callback)(collider_b.game_object)
            if comp_b is not None:
                getattr(comp_b, callback)(collider_a.game_object)

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
            Physics._instance = Physics()
        return Physics._instance