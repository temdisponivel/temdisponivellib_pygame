#  TODO: remove hard coded types from what we consider drawable and drawer

from builtincomponents.transform import Transform
from contracts import *
import errorutils


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

    def __init__(self):
        super(GameObject, self).__init__()
        self._id = GameObject._id + 1
        self._tag = self.__class__
        self._name = "GameObject " + str(self._id)
        GameObject._id += 1
        self._components = {}
        self._components_remove = []
        self._components_add = []
        self._started = False
        self._persistent = False
        self._add_component(Transform())

    @property
    def id(self):
        return self._id

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, tag):
        if self._tag in self._started_game_object_by_tag:
            self._started_game_object_by_tag[self._tag].remove(self)
        self._tag = tag
        if self._tag in self._started_game_object_by_tag:
            self._started_game_object_by_tag.setdefault(self._tag, [])
        self._started_game_object_by_tag[self._tag].append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if self._name in self._started_game_object_by_name:
            self._started_game_object_by_name[self._name].remove(self)
        self._name = name
        if self._name in self._started_game_object_by_name:
            self._started_game_object_by_name.setdefault(self._name, [])
        self._started_game_object_by_name[self._name].append(self)

    @property
    def started(self):
        return self._started

    @property
    def transform(self):
        return self.get_component(Transform)

    def start(self):
        GameObject._started_game_object_by_tag.setdefault(self.tag, [])
        GameObject._started_game_object_by_name.setdefault(self.name, [])
        GameObject._started_game_object_by_tag[self.tag].append(self)
        GameObject._started_game_object_by_name[self.name].append(self)
        GameObject._started_game_object_by_id[self._id] = self
        self._update_component_list()
        self._started = True

    def update(self):
        if not self.is_updating:
            return
        for component in self._components.values():
            try:
                component.update()
            except:
                errorutils.handle_exception()
        self._update_component_list()

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
        self._update_component_list()

    def destroy(self):
        Game.instance().scene.remove_game_object(self)

    def _update_component_list(self):
        for component in self._components_remove:
            self._remove_component(component)

        for component in self._components_add:
            self._add_component(component)

        self._components_add = []
        self._components_remove = []

    def add_component(self, component):
        """
        Adds a component to this game object. From now on, this component will be update or draw (or both)
        within the lifecycle of this game object
        This method sets the 'game_object' instance of the component to this game object. It also call the start
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
                raise Exception("Try to add a duplicate component marked as unique. " + str(component.__class__))
            if isinstance(component, IDrawable):
                self._components[IDrawable] = component
            elif isinstance(component, IDrawer):
                self._components[IDrawer] = component
            else:
                self._components[component.__class__] = component
        else:
            self._components.setdefault(component.__class__, [])
            if component not in self._components[component.__class__]:
                self._components[component.__class__].append(component)

        if isinstance(component, IResource):
            try:
                component.load()
            except:
                errorutils.handle_exception()

        if self._started:
            Game.instance().scene.game_object_add_component(self, component)

        component.game_object = self
        try:
            component.start()
        except:
                errorutils.handle_exception()

    def _remove_component(self, component):
        if component.__class__ not in self._components:
            return

        if type(self._components[component.__class__]) is list:
            if component in self._components[component.__class__]:
                self._components[component.__class__].remove(component)
        else:
            if isinstance(component, IDrawable):
                self._components[IDrawable] = None
            elif isinstance(component, IDrawer):
               self._components[IDrawer] = None
            else:
                del self._components[component.__class__]

        if isinstance(component, IResource):
            try:
                component.unload()
            except:
                errorutils.handle_exception()

        if self._started:
            Game.instance().scene.game_object_remove_component(self, component)

        component.game_object = None
        try:
            component.finish()
        except:
                errorutils.handle_exception()

    def get_component(self, key):
        """
        Return only one component of a given type.
        If this game object has more than one, it will return the first
        """
        if key not in self._components:
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
        if key not in self._components:
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