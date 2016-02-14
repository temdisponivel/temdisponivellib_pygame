import game
from pygame import error
from builtin_components.transform import Transform
from contracts import *


class GameObject(IUpdatable):

    """
    Class that represents a game object.

    A game object is a object in the game. This object can contain multiples components.
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
        self._persistent = False
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

    def start(self):
        GameObject._started_game_object_by_tag.setdefault(self.tag, [])
        GameObject._started_game_object_by_name.setdefault(self.name, [])
        GameObject._started_game_object_by_tag[self.tag].append(self)
        GameObject._started_game_object_by_name[self.name].append(self)
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
        game.Game.instance.scene.remove_game_object(self)

    def _update_component_list(self):
        for component in self._components_remove:
            self._remove_component(component)

        for component in self._components_add:
            self._add_component(component)

        self._components_add = []
        self._components_remove = []

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
        self._components_add.append(component)

    def remove_component(self, component):
        """
        Remove a component from this game object. From now on, this component won't be update or draw (or both)
        within the lifecycle of this game object
        This function sets the 'game_object' property of the component to None. It also call the 'finish' method of
        the component
        """
        self._components_remove.append(component)

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
                self._components[component.__class__].append(component)

        if isinstance(component, IResource):
            component.load()

        if self.started:
            game.Game.instance.scene.game_object_add_component(self, component)

        component.game_object = self
        component.start()

    def _remove_component(self, component):
        if component.__class__ not in self._components:
            pass

        if type(self._components[component.__class__]) is list:
            if component in self._components[component.__class__]:
                self._components[component.__class__].remove(component)
        else:
            if isinstance(IDrawable, component):
                self._components[IDrawable] = None
            else:
                del self._components[component.__class__]

        if isinstance(component, IResource):
            component.unload()

        if self.started:
            game.Game.instance.scene.game_object_remove_component(self, component)

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

    @property
    def persistent(self):
        """
        Return whether this game object will be destroyed when whe scene finish.
        """
        return self._persistent

    @persistent.setter
    def persistent(self, persistent):
        """
        Defines whether this game object will be destroyed when whe scene finish.
        """
        self._persistent = persistent

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