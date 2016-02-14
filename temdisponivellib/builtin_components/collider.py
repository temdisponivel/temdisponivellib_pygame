from pygame import Rect
from temdisponivellib.component import Component
from temdisponivellib import length_area_world
import math


class Collider(Component):
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
        self._changed = False
        self._areas = []
        self._last_values = [0, 0, 0, 0]

    def start(self):
        self._update_areas()

    def finish(self):
        self._remove_from_area(self._areas)

    def check_collision(self, other):
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

    @x.setter
    def x(self, x):
        self._last_values[0] = self.x
        self._changed = True
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._last_values[1] = self.y
        self._changed = True
        self._y = y

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._last_values[2] = self.width
        self._changed = True
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._last_values[3] = self.height
        self._changed = True
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

    def update(self):
        if not self._changed:
            pass
        self._update_areas()
        self._changed = False

    def _update_areas(self):
        last_areas = self._areas
        current_areas = self._get_areas_of_region(self)
        to_remove = list(set(last_areas) - set(current_areas))
        to_insert = list(set(current_areas) - set(last_areas))
        self._remove_from_area(to_remove)
        self._insert_in_area(to_insert)
        self._areas = current_areas

    def _insert_in_area(self, areas):
        """
        Insert this collider into the list of colliders by area
        """
        for area in areas:
            if area not in Collider._get_areas_of_region:
                continue
            Collider._colliders_by_area.setdefault(area, [])
            if self not in Collider._colliders_by_area[area]:
                Collider._colliders_by_area[area].append(self)

    def _remove_from_area(self, areas):
        """
        Remove this collider from the list of colliders by area
        """
        for area in areas:
            if area not in Collider._get_areas_of_region:
                continue
            if self in Collider._colliders_by_area[area]:
                Collider._colliders_by_area[area].remove(self)

    def get_colliders_my_region(self):
        """
        :return: List of lists of colliders containing all colliders in the areas of this one. If there is none,
        returns empty list
        """
        colliders = []
        for area in self._areas:
            colliders.append(Collider._colliders_by_area[area])
        return colliders

    @property
    def as_rect(self):
        """
        :return: This collider as a rect
        """
        return Rect(self.x, self.y, self.width, self.height)

    @staticmethod
    def _get_areas_of_region(rect):
        if rect.width < length_area_world and rect.height < length_area_world:
            return [(rect.transform.left % length_area_world, rect.top % length_area_world)]

        areas = []
        if rect.width > length_area_world:
            for i in range(0, rect.left / length_area_world):
                areas.append(((rect.left % length_area_world) + i, rect.top % length_area_world))
        if rect.height > length_area_world:
            for i in range(0, rect.top / length_area_world):
                areas.append((rect.left % length_area_world,
                              (rect.top % length_area_world) + i))
        return areas

    @staticmethod
    def get_colliders():
        """
        Return a list of lists containing all colliders.
        Colliders in the same list are in the same area. There's no need to validate collision between game objects
         of different areas (lists)
        """
        return Collider._colliders_by_area.values()

    @staticmethod
    def get_colliders_by_area(area):
        """
        Return all colliders in the specified area.
        If the area doesn't have any colliders, return a empty list
        """
        if area in Collider._colliders_by_area:
            return Collider._colliders_by_area[area]
        else:
            return []

    @staticmethod
    def get_colliders_in_region(rect):
        """
        Return a list of lists containing all colliders in the given rect
        Colliders in the same list are in the same area. There's no need to validate collision between game objects
         of different areas (lists)
        """
        colliders = []
        for area in Collider._get_areas_of_region(rect):
            colliders.append(Collider._colliders_by_area[area])
        return colliders


class BoxCollider(Collider):
    """
    A box collider. This validate collision with another box collider or a circle collider.
    The x y of ths collider is on top left corner and will be the top left corner of the transform of the game object.
    Note that, as this collider is temporary, the collision with the box only occurs if the box is axis-aligned
    to the circle.
    """

    def __init__(self, position=(0, 0), size=(0, 0)):
        super(Collider, self).__init__()
        self._type = Collider.BOX
        self.x = position[0]
        self.y = position[1]
        self.width = size[0]
        self.height = size[1]

    def update(self):
        self.x = self.transform.left
        self.y = self.transform.top
        super(Collider, self).update()

    def check_collision(self, collider):
        if collider.collider_type == Collider.BOX:
            return (math.fabs(self.x - collider.x) * 2 < (self.width + collider.width)) and \
                   (math.fabs(self.y - collider.y) * 2 < (self.height + collider.height))
        elif collider.collider_type == Collider.CIRCLE:
            return collider.check_collision(self)


class CircleCollider(Collider):
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
        self.x, self.y = self.transform.centerx, self.transform.centery
        super(Collider, self).update()

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = radius

    def check_collision(self, collider):
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

        real_distancex = distancex - collider.width / 2
        real_distancey = distancey - collider.height / 2
        corner_distance_sq = math.pow(real_distancex, 2) + math.pow(real_distancey, 2)
        return corner_distance_sq <= math.pow(self.radius, 2)

    def _collide_with_circle(self, collider):
        distancex = math.fabs(self.x - collider.x)
        distancey = math.fabs(self.y - collider.y)

        real_distance = (math.pow(distancex, 2) + math.pow(distancey, 2))

        return real_distance <= math.pow(self.radius + collider.radius, 2)

    def width(self):
        return self.radius

    def height(self):
        return self.radius
