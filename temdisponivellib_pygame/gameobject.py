from pygame import sprite

from temdisponivellib_pygame.loader import Loader


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
        pass

    def update(self):
        pass


class GameObject(object, IUpdatable, sprite.Sprite, IResource):
    """
    Class that defines a game object.
    A game object is something that can be drawn on screen, updated and loaded/undloaded.
    It also have a position.
    """
    def __init__(self, image=""):
        super(IUpdatable, self).__init__()
        super(sprite.Sprite, self).__init__()
        super(IResource, self).__init__()
        self.image, self.rect = Loader.load_image(image)