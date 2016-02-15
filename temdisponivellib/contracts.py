from game import Game


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

    def start(self):
        pass

    def update(self):
        pass

    def finish(self):
        pass

    @property
    def is_updating(self):
        """
        Whether this game object should be updated
        :return: True if it is.
        """
        return self._is_updating

    @is_updating.setter
    def is_updating(self, is_updating):
        """
        Set if this game object should be updated or not
        :param is_updating:
        :return:
        """
        self._is_updating = is_updating


class IDrawer(object):
    """
    Class that defines something that perform drawings into the surface.
    """

    def __init__(self):
        self._is_drawing = True

    def draw(self):
        """
        This method is called when this object should draw whatever if supposed to.
        """
        pass

    @property
    def is_drawing(self):
        """
        Whether or not this game object should be drawn
        :return:
        """
        return self._is_drawing

    @is_drawing.setter
    def is_drawing(self, is_drawing):
        """
        Set if this game object should be drawn
        :return:
        """
        self._is_drawing = is_drawing


class IDrawable(IResource):
    """
    Class that defined something that will be drawn into a surface.
    """

    _order_in_layer = 0

    def __init__(self):
        super(IDrawable, self).__init__()
        self._is_drawing = True
        self._layer = 0
        self._order_in_layer = IDrawable._order_in_layer + 1
        IDrawable._order_in_layer += 1

    @property
    def drawable(self):
        """
        This method must return something that can be drawn into a surface. This object must have a 'get_rect'
        method for the rect representing the area of it.
        :return: Something to drawn into a surface.
        """
        return None

    @property
    def get_rect(self):
        """
        Method that return the rect to use as destination on 'Surface.blit'
        :return: Rect to use as destination in the main surface.
        """
        return None

    @property
    def is_drawing(self):
        """
        Whether or not this game object should be drawn
        :return:
        """
        return self._is_drawing

    @is_drawing.setter
    def is_drawing(self, is_drawing):
        """
        Set if this game object should be drawn
        :return:
        """
        self._is_drawing = is_drawing

    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, layer):
        last_layer = self._layer
        self._layer = layer
        Game.instance().scene.change_layer_or_order(self, last_layer, self.order_in_layer)

    @property
    def order_in_layer(self):
        return self._order_in_layer

    @order_in_layer.setter
    def order_in_layer(self, order):
        last_order = self.order_in_layer
        self._order_in_layer = order
        Game.instance().scene.current.change_layer_or_order(self, self.layer, last_order)