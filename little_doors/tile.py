class Tile(object):
    __slots__ = ('index', 'name', 'resource_filename', 'image', 'size', 'anchor', 'depth')

    def __init__(self, index, name='Tile', resource_filename='', size=None, anchor=(0.0, 0.0), depth=0.0):
        self.index = index
        self.name = name
        self.resource_filename = resource_filename
        self.image = None
        self.size = (0.0, 0.0, 0.0) if size is None else size
        self.anchor = anchor
        self.depth = depth
