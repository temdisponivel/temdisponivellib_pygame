from pygame import image as pyimage
from pygame import mixer
from pygame import error as err


class Loader(object):
    """
    Helper class to load stuff.
    """
    @staticmethod
    def load_sound(path):
        """
        Load and returns a sound by a given name
        :param path: Path of the sound.
        :return: A sound.
        """
        try:
            sound = mixer.Sound(path)
        except err, message:
            print err, message
            raise err
        return sound

    @staticmethod
    def load_image(path):
        """
        Load a image and returns it.
        :param path: Name of the image.
        :return: A image.
        """
        try:
            image = pyimage.load(path)
            image.convert()
            return image, image.get_rect()
        except err, message:
            print err, message
            raise err