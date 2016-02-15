from contracts import IUpdatable
from temdisponivellib import callback_functions


class Component(IUpdatable):
    """
    Represents a component that can be attached to a game object and be part of its lifecycle.
    """

    _class_by_callback_function = {}
    _validated_classes = []

    def __init__(self):
        super(Component, self).__init__()
        self._game_object = None
        if self.__class__ not in Component._validated_classes:
            Component._validated_classes.append(self.__class__)
            for callback in callback_functions:
                if not hasattr(self, callback):
                    continue
                Component._class_by_callback_function.setdefault(callback, [])
                Component._class_by_callback_function[callback].append(self.__class__)

    @property
    def game_object(self):
        return self._game_object

    @game_object.setter
    def game_object(self, game_object):
        self._game_object = game_object

    @property
    def transform(self):
        return self.game_object.transform

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

    @staticmethod
    def get_class_by_callback(callback_name):
        """
        :param callback_name: Name of the callback to look for classes that have it
        :return: List of all classes that have this callback
        """
        if callback_name not in Component._class_by_callback_function:
            return []
        else:
            return Component._class_by_callback_function[callback_name]