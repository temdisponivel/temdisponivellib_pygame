from gameobject import GameObject
from gameobject import IDrawable
from pygame import error as err


class Scene(object, GameObject, IDrawable):
    """
    Class that represents a scene in the game.
    It is a game object because it behaves like one, so...
    """

    def __init__(self, background_color, *game_objects):
        super(GameObject, self).__init__()
        self._game_objects = {}
        self._cameras = {}
        self._areas = {}
        self._included = []
        self._removed = []
        self._background_color = background_color
        for game_object in game_objects:
            self.add_game_object(game_object)

    def update(self):
        if not self.is_updating:
            pass
        index = 0
        for game_object in self._game_objects.values():
            if not game_object.is_updating:
                continue
            try:
                game_object.update()
                self._place_game_object_area(game_object)
                index += 1
            except err, message:
                print err, message
                raise err

        for game_object in self._included:
            self._game_objects[game_object.id] = game_object
        for game_object in self._included:
            if game_object.id in self._game_objects:
                del self._game_objects[game_object.id]
        self._included.clear()
        self._removed.clear()

    def draw(self):
        if not self.is_drawing:
            pass
        for camera in self._cameras.values():
            if not camera.is_drawing:
                continue
            try:
                camera.draw()
            except err, message:
                print err, message
                raise err

    @property
    def game_objects(self):
        return self._game_objects

    def add_game_object(self, game_object):
        """
        Add a game object to the scene. From now on, this game object will be draw and updated.
        :param game_object: Game object to add
        :return: None
        """
        self._included.insert(game_object)

    def remove_game_object(self, game_object):
        """
        Remove a game object from the scene. From now on, this game object won't be drawn or updated anymore.
        :param game_object:
        :return:
        """
        self._removed.insert(game_object)

    def _place_game_object_area(self, game_object):
        """
        Update the area of which a game object is placed
        :param game_object: Game object to update the area
        """
        pass