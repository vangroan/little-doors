class Tile(object):
    __slots__ = ('index', 'name', 'resource_filename', 'image', 'size')

    def __init__(self, index, name='Tile', resource_filename='', size=None):
        self.index = index
        self.name = name
        self.resource_filename = resource_filename
        self.image = None
        self.size = (0.0, 0.0, 0.0) if size is None else size
