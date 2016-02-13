from pygame import Rect
from ..gameobject import Component
import math


class Collider(object, Component):

    """
    Base class  for all current colliders. This is temporary, the intention is to integrate a Physics engine
    (like Box2D)
    """

    BOX = 1
    CIRCLE = 2

    def __init__(self):
        super(Component, self).__init__()
        self._type = None

    def validate_collision(self, other):
        """
        Must return true if collides with the other
        :param other: Other collider to validate collision
        :return: True if it collides
        """
        return False

    @property
    def collider_type(self):
        return self._type


class BoxCollider(object, Collider, Rect):
    """
    A box collider. This validate collision with another box collider or a circle collider.
    The top left corner of this box collider will be the top left corner of the transform of the game object.
    Note that, as this collider is temporary, the collision with the box only occurs if the box is axis-aligned
    to the circle.
    """

    def __init__(self, position=(0, 0), size=(0, 0)):
        super(Collider, self).__init__()
        super(Rect, self).__init__(position, size)
        self._type = Collider.BOX

    def update(self):
        self.top = self.transform.top
        self.left = self.transform.left


    def validate_collision(self, collider):
        if collider.collider_type == Collider.BOX:
            return self.colliderect(collider)
        elif collider.collider_type == Collider.CIRCLE:
            return collider.validate_collision(self)


class CircleCollider(object, Collider):
    """
    A circle collider. This validate collision with another circle collider or a box collider.
    The center of this circle collider will be the center of the transform of the game object.
    Note that, as this collider is temporary, the collision with the box only occurs if the box is axis-aligned
    to the circle
    """

    def __init__(self, radius, center=(0, 0)):
        super(Collider, self).__init__()
        self._radius = radius
        self._center.x = center[0]
        self._center.y = center[1]

    def update(self):
        self.center = self.transform.centerx, self.transform.centery

    @property
    def center(self):
        return self._center

    @property.setter
    def center(self, center=(0, 0)):
        self._center.x = center[0]
        self._center.y = center[1]

    @property
    def radius(self):
        return self._radius

    @property.setter
    def radius(self, radius):
        self._radius = radius

    def validate_collision(self, collider):
        if collider.collider_type == Collider.CIRCLE:
            return self._collide_with_circle(collider)
        elif collider.collider_type == Collider.BOX:
            return self._collide_with_box(collider)

    def _collide_with_box(self, collider):
        distancex = math.fabs(self.center.x - collider.centerx)
        distancey = math.fabs(self.center.y - collider.centery)

        if distancex > (collider.width/2) + self.radius:
            return False
        if distancey > (collider.height/2) + self.radius:
            return False

        if distancex <= (collider.width/2):
            return True
        if distancey <= (collider.height/2):
            return True

        cornerDistance_sq = math.pow((distancex - collider.width/2), 2) + \
                            math.pow((distancey - collider.height/2), 2)

        return cornerDistance_sq <= math.pow(self.radius, 2);


    def _collide_with_circle(self, collider):
        distancex = math.fabs(self.center.x - collider.center.x)
        distancey = math.fabs(self.center.y - collider.center.y)

        real_distance = (math.pow(distancex, 2) + math.pow(distancey, 2))

        return real_distance <= math.pow(self.radius + collider.radius, 2)
