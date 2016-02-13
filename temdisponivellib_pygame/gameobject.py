from pygame import Rect
from pygame import error


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

    def update(self):
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


class IDrawable(object):
    """
    Class that defines something that can be draw (or draw something else) in screen.
    """
    def __init__(self):
        self._is_drawing = True

    def draw(self):
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


class GameObject(object, IUpdatable, IDrawable, IResource):
    """
    Class that represents a game object.

    A game object is a object in the game (dãã). This object can contain multiples components.
    This components are hooked in the lifecycle of the game object, so when the game object update, all its components
    that are marked as updatable are updated with it. Same for draw.

    This allow the components to control and manipulate properties of the game object and others components.
    """

    _id = 0
    _loaded_game_object_by_tag = {}
    _loaded_game_object_by_id = {}
    _loaded_game_object_by_name = {}

    def __init__(self):
        super(IUpdatable, self).__init__()
        super(IDrawable, self).__init__()
        super(IResource, self).__init__()
        self._id = GameObject._id + 1
        self._tag = self.__class__.__name__
        self._name = "GameObject " + self._tag + " " + self._id
        GameObject._id += 1
        self._components = {}
        self._components_by_flag = {}
        self._loaded = False
        self.load()

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
    def loaded(self):
        return self._loaded

    def update(self):
        for component in self._components_by_flag[Component.TO_UPDATE]:
            component.update()

    def draw(self):
        for component in self._components_by_flag[Component.TO_DRAW]:
            component.draw()

    def load(self):
        GameObject._loaded_game_object_by_tag.setdefault(self.tag, [])
        GameObject._loaded_game_object_by_name.setdefault(self.name, [])
        GameObject._loaded_game_object_by_tag[self.tag].insert(self)
        GameObject._loaded_game_object_by_name[self.name].insert(self)
        GameObject._loaded_game_object_by_id[self._id] = self
        for component in self._components.values():
            component.load()
        self.loaded = True

    def unload(self):
        if self.tag in GameObject._loaded_game_object_by_tag:
            if self in GameObject._loaded_game_object_by_tag:
                GameObject._loaded_game_object_by_tag[self.tag].remove(self)

        if self.name in GameObject._loaded_game_object_by_name:
            if self in GameObject._loaded_game_object_by_name:
                GameObject._loaded_game_object_by_name[self.name].remove(self)

        if self.id in GameObject._loaded_game_object_by_id:
            del GameObject._loaded_game_object_by_id[self.id]

        for component in self._components.values():
            component.unload()

    def add_component(self, component):
        """
        Adds a component to this game object. From now on, this component will be update or draw (or both, depending
        on the flags of the component)
        within the lifecycle of this game object
        Raise a exception if the component class is marked as unique and this object already  has a instance
        of the same class

        This method sets the 'game_object' instance of the component to this game object. It algo call the load
        method of the component.
        """
        if component.is_unique:
            if component.__class__ in self._components:
                raise error("Try to add a duplicate component marked as unique.")
            self._components[component.__class__] = component
        else:
            self._components.setdefault(component.__class__, [])
            self._components[component.__class__].insert(component)
        self._components_by_flag.setdefault(component.flags, [])
        self._components_by_flag[component.flags].insert(component)
        component.game_object = self
        component.load()

    def remove_component(self, component):
        """
        Remove a component from this game object. From now on, this component won't be update or draw (or both)
        within the lifecycle of this game object
        This function sets the 'game_object' property of the component to None. It also call the 'unload' method of
        the component
        """
        if type(self._components[component.__class__]) is list:
            self._components[component.__class__].remove(component)
        else:
            del self._components[component.__class__]
        self._components_by_flag[component.flags].remove(component)
        component.game_object(None)
        component.unload()

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
        Return a list of all loaded (that wasn't unloaded yet) that have a given name
        If no game object has this name, it return None
        """
        if name not in GameObject._loaded_game_object_by_name:
            return None
        return GameObject._loaded_game_object_by_name[name]

    @staticmethod
    def get_game_object_by_tag(tag):
        """
        Return a list of all loaded (that wasn't unloaded yet) that have a given tag
        If no game object has this tag, it return None
        """
        if tag not in GameObject._loaded_game_object_by_tag:
            return None
        return GameObject._loaded_game_object_by_tag[tag]

    @staticmethod
    def get_game_object_by_id(game_object_id):
        """
        Return a game object that has a given id
        If no game object has this tag, it return None
        """
        if game_object_id not in GameObject._loaded_game_object_by_id:
            return None
        return GameObject._loaded_game_object_by_tag[game_object_id]


class Component(object, IResource):
    """
    Represents a component that can be attached to a game object and be part of its lifecycle
    """

    TO_UPDATE, TO_DRAW = 1, 2

    def __init__(self):
        self._game_object = None

    @property
    def game_object(self):
        return self._game_object

    @property.setter
    def game_object(self, game_object):
        self._game_object = game_object

    def load(self):
        pass

    def unload(self):
        pass

    @staticmethod
    @property
    def is_unique():
        """
        :return: If a game object can have more than one instance of this component.
        """
        return False

    @staticmethod
    @property
    def flags():
        """
        :return: If should be draw or updated. Use | to sum to flags.
        """
        return Component.TO_DRAW | Component.TO_UPDATE