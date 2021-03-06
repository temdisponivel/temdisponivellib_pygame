from pygame import image as pyimage
from pygame import mixer
import traceback
import os


class Loader(object):
    """
    Helper class to load stuff.
    """

    base_path = "data"
    concat_base_path = True

    @staticmethod
    def load_sound(path):
        """
        Load and returns a sound by a given name
        :param path: Path of the sound.
        :return: A sound.
        """
        sound = mixer.Sound(path)
        return sound

    @staticmethod
    def load_image(path, concat=True):
        """
        Load a image and returns it. If Loader.concat_base_path is true and concat parameter is true (it is by default)
        the path passed will be concatenated with the base_path of this class, unless
        :param path: Name of the image.
        :return: A tuple containing a image and the rect of it.
        """
        if Loader.concat_base_path and concat:
            full_path = os.path.join(Loader.base_path, path)
        else:
            full_path = path
        image = pyimage.load_basic(full_path)
        image.convert()
        return image, image.get_rect()