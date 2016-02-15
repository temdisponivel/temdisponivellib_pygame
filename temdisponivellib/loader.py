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

    def __init__(self):
        super(Loader, self).__init__()

    @staticmethod
    def load_sound(path, concat=True):
        """
        Load a sound and returns it. If Loader.concat_base_path is true and concat parameter is true (it is by default)
        the path passed will be concatenated with the base_path of this class
        :param path: Name of the sound file.
        :return: A sound
        """
        sound = mixer.Sound(path)
        return sound

    @staticmethod
    def load_image(path, concat=True):
        """
        Load a image and returns it. If Loader.concat_base_path is true and concat parameter is true (it is by default)
        the path passed will be concatenated with the base_path of this class
        :param path: Name of the image file.
        :return: A tuple containing a image returned from convert_alpha, its rect and the original image
        """
        if Loader.concat_base_path and concat:
            full_path = os.path.join(Loader.base_path, path)
        else:
            full_path = path
        image = pyimage.load(full_path)
        return image.convert_alpha(), image.get_rect(), image