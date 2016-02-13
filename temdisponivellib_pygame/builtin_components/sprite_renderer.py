from pygame.sprite import Sprite
from ..gameobject import IDrawable, Component
from ..loader import Loader


class SpriteRenderer(object, Component, IDrawable):
    """
    Class that holds a sprite that will be drawn into a surface.
    """

    def __init__(self, path=""):
        """
        Create a sprite renderer. If passed path parameter, this will load the image by its path
        (using Loader.load_image(path, true))
        :param path: Path of the sprite. If None or blank, nothing is  loaded.
        :return:
        """
        super(Sprite, self).__init__()
        self._image_path = path
        self._image = None

    def get_drawable(self):
        return self._image

    def load(self):
        if self._image_path != "":
            self._image = Loader.load_image(self._image_path)

    def unload(self):
        self._image = None

    @property
    def image(self):
        return self._image

    @property.setter
    def image(self, image):
        self._image = image


class SpriteRendererAnimaton(object, Component):
    pass