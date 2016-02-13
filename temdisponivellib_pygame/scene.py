from gameobject import GameObject
from gameobject import IDrawer
from gameobject import IDrawable
from gameobject import IResource
from pygame import error as err


class Scene(object, GameObject, IDrawer):
    """
    Class that represents a scene in the game.
    It is a game object because it behaves like one, so...
    """

    def __init__(self, background_color, *game_objects):
        super(GameObject, self).__init__()
        self._game_objects = {}
        self._game_objects_drawable = {}
        self._game_objects_drawer = []
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
        game_objects = self._layers.values()
        for game_object in game_objects:
            if not game_object.is_updating:
                continue
            try:
                game_object.update()
                index += 1
            except err, message:
                print err, message
                raise err

        for game_object in self._included:
            self._game_objects[game_object.id] = game_object
            if game_object.get_component(IDrawable) is not None:
                comp = game_object.get_component(IDrawable)
                self._game_objects_drawer[comp.layer, comp.order_in_layer, game_object.id] = game_object
            if game_object.get_component(IDrawer) is not None:
                self._game_objects_drawer.insert(game_object)

        for game_object in self._removed:
            if game_object.id not in self._game_objects:
                pass

            del self._game_objects[game_object.id]

            comp = game_object.get_component(IDrawable)
            if game_object.get_component(IDrawable) is not None:
                del self._game_objects_drawable[comp.layer, comp.order_in_layer, game_object.id]

            if game_object.get_component(IDrawer) is not None:
                self._game_objects_drawer.remove(game_object)

            game_object.finish()
        self._included.clear()
        self._removed.clear()

    def draw(self):
        if not self.is_drawing:
            pass
        for drawer in self._game_objects_drawer:
            if not drawer.is_drawing:
                continue
            try:
                drawer.draw()
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

    @property
    def get_drawables(self):
        """
        :return: A list with all drawables in this scene.
        """
        return sorted(self._game_objects_drawable).values()

    def get_objects_area(self, rect):
        """
        Return a list with all game object within (or intersecting) the rect
        :param rect: Rect to validate game object in collision.
        :return: List with all matches.
        """
        pass

    def _place_game_object_area(self, game_object):
        """
        Update the area of which a game object is placed
        :param game_object: Game object to update the area
        """
        pass

    def change_layer_or_order(self, game_object, last_layer, last_order):
        """
        Callback for when a game_object change layer or order. The game object must have the values already updated
        :param game_object: Game object that change
        :param last_layer: Last layer
        :param last_order: Last order
        """
        del self._game_objects_drawable[last_layer, last_order]
        if game_object.get_component(IDrawable) is not None:
                comp = game_object.get_component(IDrawable)
                self._game_objects_drawable[comp.layer, comp.order_in_layer] = game_object

    def game_object_moved(self, game_object, last_position):
        """
        Callback for when a game object move. Game object must have the values already updated.
        :param game_object: Game object that move.
        :param last_position: Last position of the object.
        :return:
        """
        self._place_game_object_area(game_object)