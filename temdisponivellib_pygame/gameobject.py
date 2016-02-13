from game import Game
from pygame import error
from builtin_components.transform import Transform

class IResource(object):
    """
    Class that defines something that must be loaded and unloaded.
    """

    def __init__(self):
        pass

    def load(self):
        """
        Method called when this resource is supposed to load itself.
        """
        pass

    def unload(self):
        """
        Method called when this resource should unload itself.
        """
        pass


class IUpdatable(object):
    """
    Class that defines something that will be updated in game.
    """
    def __init__(self):
        self._is_updating = True

    def start(self):
        pass

    def update(self):
        pass

    def finish(self):
        pass

    @property
    def is_updating(self):
        """
        Whether this game object should be updated
        :return: True if it is.
        """
        return self._is_updating

    @property.setter
    def is_updating(self, is_updating):
        """
        Set if this game object should be updated or not
        :param updatable:
        :return:
        """
        self._is_updating = is_updating


class IDrawer(object):

    """
    Class that defines something that perform drawings into the surface.
    """

    def __init__(self):
        self._is_drawing = True

    def draw(self):
        """
        This method is called when this object should draw whatever if supposed to.
        """
        pass

    @property
    def is_drawing(self):
        """
        Whether or not this game object should be drawn
        :return:
        """
        return self._is_drawing

    @property.setter
    def is_drawing(self, is_drawing):
        """
        Set if this game object should be drawn
        :return:
        """
        self._is_drawing = is_drawing


class IDrawable(object, IResource):
    """
    Class that defined something that will be drawn into a surface.
    """

    _order_in_layer = 0

    def __init__(self):
        super(IResource, self).__init__()
        self._is_drawing = True
        self._layer = 0
        self._order_in_layer = IDrawable._order_in_layer + 1
        IDrawable._order_in_layer += 1

    def get_drawable(self):
        """
        This method must return something that can be drawn into a surface. This object must have a 'get_rect'
        method for the rect representing the area of it.
        :return: Something to drawn into a surface.
        """
        pass

    @property
    def is_drawing(self):
        """
        Whether or not this game object should be drawn
        :return:
        """
        return self._is_drawing

    @property.setter
    def is_drawing(self, is_drawing):
        """
        Set if this game object should be drawn
        :return:
        """
        self._is_drawing = is_drawing

    @property
    def layer(self):
        return self._layer

    @property.setter
    def layer(self, layer):
        last_layer = self._layer
        self._layer = layer
        Game.instance.scene.change_layer_or_order(self, last_layer, self.order_in_layer)

    @property
    def order_in_layer(self):
        return self._order_in_layer

    @property.setter
    def order_in_layer(self, order):
        last_order = self.order_in_layer
        self._order_in_layer = order
        Game.instance.scene.change_layer_or_order(self, self.layer, last_order)


class GameObject(object, IUpdatable):
    """
    Class that represents a game object.

    A game object is a object in the game (dãã). This object can contain multiples components.
    This components are hooked in the lifecycle of the game object, so when the game object update, all its components
    that are marked as updatable are updated with it. Same for draw.

    This allow the components to control and manipulate properties of the game object and others components.
    """

    _id = 0
    _started_game_object_by_tag = {}
    _started_game_object_by_id = {}
    _started_game_object_by_name = {}

    def __init__(self, name="GameObject", tag="Tag"):
        super(IUpdatable, self).__init__()
        self._id = GameObject._id + 1
        self._tag = tag
        self._name = name
        GameObject._id += 1
        self._components = {}
        self._components_remove = []
        self._components_add = []
        self.is_drawing = False
        self._started = False
        self.add_component(Transform())

    @property
    def id(self):
        return self._id

    @property
    def tag(self):
        return self._tag

    @property
    def name(self):
        return self._name

    @property
    def started(self):
        return self._started

    @property
    def transform(self):
        return self.get_component(Transform)

    def update(self):
        if not self.is_updating:
            pass
        for component in self._components:
            component.update()
        self._update_component_list()

    def get_drawable(self):
        if self.is_drawing and self._drawable_component.is_drawing:
            return self._drawable_component.get_drawable

    def start(self):
        GameObject._started_game_object_by_tag.setdefault(self.tag, [])
        GameObject._started_game_object_by_name.setdefault(self.name, [])
        GameObject._started_game_object_by_tag[self.tag].insert(self)
        GameObject._started_game_object_by_name[self.name].insert(self)
        GameObject._started_game_object_by_id[self._id] = self
        self._update_component_list()
        self._started = True

    def finish(self):
        if self.tag in GameObject._started_game_object_by_tag:
            if self in GameObject._started_game_object_by_tag:
                GameObject._started_game_object_by_tag[self.tag].remove(self)

        if self.name in GameObject._started_game_object_by_name:
            if self in GameObject._started_game_object_by_name:
                GameObject._started_game_object_by_name[self.name].remove(self)

        if self.id in GameObject._started_game_object_by_id:
            del GameObject._started_game_object_by_id[self.id]

        for component in self._components.values():
            self.remove_component(component)

    def destroy(self):
        Game.instance.scene.remove_game_object(self)

    def _update_component_list(self):
        for component in self._components_remove:
            self._remove_component(component)

        for component in self._components_add:
            self._add_component(component)

        self._components_add.cler()
        self._components_remove.clear()

    def add_component(self, component):
        """
        Adds a component to this game object. From now on, this component will be update or draw (or both, depending
        on the flags of the component)
        within the lifecycle of this game object
        Raise a exception if the component class is marked as unique and this object already  has a instance
        of the same class

        This method sets the 'game_object' instance of the component to this game object. It algo call the start
        method of the component.
        """
        self._components_add.insert(component)

    def remove_component(self, component):
        """
        Remove a component from this game object. From now on, this component won't be update or draw (or both)
        within the lifecycle of this game object
        This function sets the 'game_object' property of the component to None. It also call the 'finish' method of
        the component
        """
        self._components_remove.insert(component)

    def _add_component(self, component):
        if component.is_unique:
            if component.__class__ in self._components:
                raise error("Try to add a duplicate component marked as unique.")
            if isinstance(component, IDrawable):
                self._components[IDrawable] = component
            else:
                self._components[component.__class__] = component
        else:
            self._components.setdefault(component.__class__, [])
            if component not in self._components[component.__class__]:
                self._components[component.__class__].insert(component)

        if isinstance(component, IResource):
            component.load()

        if self.started:
            Game.instance.scene.game_object_add_component(self, component)

        component.game_object = self
        component.start()

    def _remove_component(self, component):
        if component.__class__ not in self._components:
            pass

        if type(self._components[component.__class__]) is list:
            if component in self._components[component.__class__]:
                self._components[component.__class__].remove(component)
        else:
            if isinstance(IDrawable):
                self._components[IDrawable] = None
            else:
                del self._components[component.__class__]

        if isinstance(component, IResource):
            component.unload()

        if self.started:
            Game.instance.scene.game_object_remove_component(self, component)

        component.game_object(None)
        component.finish()

    def get_component(self, key):
        """
        Return only one component of a given type.
        If this game object has more than one, it will return the first
        """
        if type not in self._components:
            return None
        if type(self._components[key]) is list:
            return self._components[key][0]
        else:
            return self._components[key]

    def get_components(self, key):
        """
        Return a list of components of a given type.
        If this game object has just one, it will return a list with just one
        """
        if type not in self._components:
            return None
        if type(self._components[key]) is list:
            return self._components[key]
        else:
            return [self._components[key]]

    @staticmethod
    def get_game_object_by_name(name):
        """
        Return a list of all started (that wasn't finished yet) that have a given name
        If no game object has this name, it return None
        """
        if name not in GameObject._started_game_object_by_name:
            return None
        return GameObject._started_game_object_by_name[name]

    @staticmethod
    def get_game_object_by_tag(tag):
        """
        Return a list of all started (that wasn't finished yet) that have a given tag
        If no game object has this tag, it return None
        """
        if tag not in GameObject._started_game_object_by_tag:
            return None
        return GameObject._started_game_object_by_tag[tag]

    @staticmethod
    def get_game_object_by_id(game_object_id):
        """
        Return a game object that has a given id
        If no game object has this tag, it return None
        """
        if game_object_id not in GameObject._started_game_object_by_id:
            return None
        return GameObject._started_game_object_by_tag[game_object_id]

    @IDrawable.is_drawing.getter
    def is_drawing(self):
        return super(self, IDrawable).is_drawing and self.get_component(IDrawable) is not None and \
            self.get_component(IDrawable).is_drawing


class Component(object, IUpdatable):

    """
    Represents a component that can be attached to a game object and be part of its lifecycle.
    """

    def __init__(self):
        super(IUpdatable, self)._init__()
        self._game_object = None

    @property
    def game_object(self):
        return self._game_object

    @property.setter
    def game_object(self, game_object):
        self._game_object = game_object

    @property
    def transform(self):
        return self.get_component(Transform)

    def add_component(self, component):
        """
        Just a shortcut for the 'game_object'.add_component
        """
        return self._game_object.remove_component(component)

    def remove_component(self, component):
        """
        Just a shortcut for the 'game_object'.remove_component
        """
        return self._game_object.remove_component(component)

    def get_component(self, key):
        """
        Just a shortcut for the 'game_object'.get_component
        """
        return self._game_object.get_component(key)

    def get_components(self, key):
        """
        Just a shortcut for the 'game_object'.get_components
        """
        return self._game_object.get_components(key)

    @property
    def is_unique(self):
        """
        :return: If a game object can have more than one instance of this component. Note that a game object
        can have only ONE drawable component attached to, so if this class inherits from IDrawable, make sure
        that this method always return true.
        """
        return True