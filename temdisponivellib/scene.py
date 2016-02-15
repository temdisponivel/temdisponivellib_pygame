#  TODO: remove hard coded types from what we consider drawable and drawer
#  TODO: implement sorted drawables by layer

from contracts import *
import errorutils
from physics import Physics


class Scene(IUpdatable, IDrawer):
    """
    Class that represents a scene in the game.
    It is a game object because it behaves like one, so...
    """

    _persistent_game_objects = []
    _current = None

    def __init__(self):
        super(Scene, self).__init__()
        self._game_objects = {}
        self._game_objects_drawable = {}
        self._game_objects_drawer = []
        self._included = []
        self._removed = []
        self._background_color = (0, 0, 0, 0)

    def start(self):
        for game_object in Scene._persistent_game_objects:
            self.add_game_object(game_object)
        Scene._persistent_game_objects = []
        self._update_list_game_object()

    def update(self):
        Physics.instance().update()
        if not self.is_updating:
            return
        index = 0
        self._update_list_game_object()
        for game_object in self._game_objects.values():
            if not game_object.is_updating:
                continue
            try:
                game_object.update()
            except:
                errorutils.handle_exception()
            index += 1

    def finish(self):
        for game_object in self._game_objects.values():
            if game_object.persistent:
                Scene._persistent_game_objects.append(game_object)
            self.remove_game_object(game_object)
        self._update_list_game_object()

    def draw(self):
        if not self.is_drawing:
            return
        for drawer in self._game_objects_drawer:
            if not drawer.get_component(IDrawer).is_drawing:
                continue
            try:
                drawer.get_component(IDrawer).draw()
            except:
                errorutils.handle_exception()

    def _update_list_game_object(self):
        for game_object in self._included:
            try:
                game_object.start()
            except:
                errorutils.handle_exception()

            self._game_objects[game_object.id] = game_object
            if game_object.get_component(IDrawable) is not None:
                comp = game_object.get_component(IDrawable)
                self._game_objects_drawable[comp.layer, comp.order_in_layer, game_object.id] = game_object
            if game_object.get_component(IDrawer) is not None:
                if game_object not in self._game_objects_drawer:
                    self._game_objects_drawer.append(game_object)

        for game_object in self._removed:
            if game_object.id not in self._game_objects:
                continue

            del self._game_objects[game_object.id]

            comp = game_object.get_component(IDrawable)
            if game_object.get_component(IDrawable) is not None:
                if (comp.layer, comp.order_in_layer, game_object.id) in self._game_objects_drawable:
                    del self._game_objects_drawable[comp.layer, comp.order_in_layer, game_object.id]

            if game_object.get_component(IDrawer) is not None:
                if game_object in self._game_objects_drawer:
                    self._game_objects_drawer.remove(game_object)

            try:
                game_object.finish()
            except:
                errorutils.handle_exception()

        self._included = []
        self._removed = []

    @property
    def game_objects(self):
        """
        :return: Dictionary containing all game objects (key: game_object.id, value: game_object)
        """
        return self._game_objects

    def add_game_object(self, game_object):
        """
        Add a game object to the scene. From now on, this game object will be draw and updated.
        :param game_object: Game object to add
        :return: None
        """
        self._included.append(game_object)

    def remove_game_object(self, game_object):
        """
        Remove a game object from the scene. From now on, this game object won't be drawn or updated anymore.
        :param game_object:
        :return:
        """
        self._removed.append(game_object)

    @property
    def get_drawables(self):
        """
        :return: A list with all drawables in this scene.
        """
        return self._game_objects_drawable.values()

    @property
    def background_color(self):
        return self._background_color

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

    def game_object_add_component(self, game_object, component):
        if isinstance(component, IDrawable):
            self._game_objects_drawable[component.layer, component.order_in_layer, game_object.id] = game_object
        if isinstance(component, IDrawer):
            if game_object not in self._game_objects_drawer:
                self._game_objects_drawer.append(game_object)

    def game_object_remove_component(self, game_object, component):
        if isinstance(component, IDrawable):
            if (component.layer, component.order_in_layer, game_object.id) in self._game_objects_drawable:
                del self._game_objects_drawable[component.layer, component.order_in_layer, game_object.id]
        if isinstance(component, IDrawer):
            if game_object in self._game_objects_drawer:
                self._game_objects_drawer.remove(game_object)