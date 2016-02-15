from temdisponivellib.contracts import IDrawable
from temdisponivellib.component import Component
from temdisponivellib.loader import Loader


class SpriteRenderer(Component, IDrawable):
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
        super(SpriteRenderer, self).__init__()
        self._image_path = path
        self._image = None

    def drawable(self):
        return self._image

    def load(self):
        if self._image_path != "":
            self._image = Loader.load_image(self._image_path)

    def unload(self):
        self._image = None

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        self._image = image

    def get_rect(self):
        if self._image is None:
            return self.transform
        return self._image.get_rect(topleft=(self.transform.x, self.transform.y))