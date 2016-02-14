from pygame import Rect
from ..gameobject import Component
from ..configuration import Configuration
import math


class Collider(object, Component):
    """
    Base class  for all current colliders. This is temporary, the intention is to integrate a Physics engine
    (like Box2D)
    """

    BOX = 1
    CIRCLE = 2

    _colliders_by_area = {}

    def __init__(self, x=0, y=0, width=0, height=0):
        super(Component, self).__init__()
        self._type = None
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    def start(self):
        self._insert_in_area()

    def finish(self):
        self._remove_from_area()

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

    @property
    def x(self):
        return self._x

    @property.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @property.setter
    def y(self, y):
        self._y = y

    @property
    def width(self):
        return self._width

    @property.setter
    def width(self, width):
        self._width = width

    @property
    def height(self):
        return self._height

    @property.setter
    def height(self, height):
        self._height = height

    @property
    def left(self):
        return self.x

    @property
    def top(self):
        return self.y

    @property
    def right(self):
        return self.x + self.width

    @property
    def bottom(self):
        return self.y + self.height

    def _insert_in_area(self):
        """
        Insert this collider into the list of colliders by area
        """
        for area in Collider._get_areas_of_collider(self):
            Collider._colliders_by_area.setdefault(area, [])
            if self not in Collider._colliders_by_area[area]:
                Collider._colliders_by_area[area].insert(self)

    def _remove_from_area(self):
        """
        Remove this collider from the list of colliders by area
        """
        for area in Collider._get_areas_of_collider(self):
            if area not in Collider._get_areas_of_collider:
                continue
            if self in Collider._colliders_by_area[area]:
                Collider._colliders_by_area[area].insert(self)

    @staticmethod
    def _get_areas_of_collider(collider):
        areas = []
        if collider.width > Configuration.instance.lenght_world_area:
            for i in range(0, collider.left / Configuration.instance.lenght_world_area):
                areas.insert(((collider.left % Configuration.instance.lenght_world_area) + i,
                              collider.top % Configuration.instance.lenght_world_area))
        if collider.height > Configuration.instance.lenght_world_area:
            for i in range(0, collider.top / Configuration.instance.lenght_world_area):
                areas.insert((collider.left % Configuration.instance.lenght_world_area,
                              (collider.top % Configuration.instance.lenght_world_area) + i))
        else:
            return [(collider.transform.left % Configuration.instance.lenght_world_area,
                     collider.top % Configuration.instance.lenght_world_area)]


class BoxCollider(object, Collider):
    """
    A box collider. This validate collision with another box collider or a circle collider.
    The x y of ths collider is on top left corner and will be the top left corner of the transform of the game object.
    Note that, as this collider is temporary, the collision with the box only occurs if the box is axis-aligned
    to the circle.
    """

    def __init__(self, position=(0, 0), size=(0, 0)):
        super(Collider, self).__init__()
        super(Rect, self).__init__(position, size)
        self._type = Collider.BOX

    def update(self):
        super(Collider, self).update()
        self.x = self.transform.left
        self.y = self.transform.top

    def validate_collision(self, collider):
        if collider.collider_type == Collider.BOX:
            return (math.fabs(self.x - collider.x) * 2 < (self.width + collider.width)) and \
                   (math.fabs(self.y - collider.y) * 2 < (self.height + collider.height))
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
        self.x = center[0]
        self.y = center[1]

    def update(self):
        super(Collider, self).update()
        self.x, self.y = self.transform.centerx, self.transform.centery

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
        distancex = math.fabs(self.x - collider.centerx)
        distancey = math.fabs(self.y - collider.centery)

        if distancex > (collider.width / 2) + self.radius:
            return False
        if distancey > (collider.height / 2) + self.radius:
            return False

        if distancex <= (collider.width / 2):
            return True
        if distancey <= (collider.height / 2):
            return True

        corner_distance_sq = math.pow((distancex - collider.width / 2), 2) + \
                             math.pow((distancey - collider.height / 2), 2)

        return corner_distance_sq <= math.pow(self.radius, 2);

    def _collide_with_circle(self, collider):
        distancex = math.fabs(self.x - collider.x)
        distancey = math.fabs(self.y - collider.y)

        real_distance = (math.pow(distancex, 2) + math.pow(distancey, 2))

        return real_distance <= math.pow(self.radius + collider.radius, 2)
