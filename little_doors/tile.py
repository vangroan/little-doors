class Tile(object):

    def __init__(self, index, name='Tile', resource_filename=''):
        self.index = index
        self.name = name
        self.resource_filename = resource_filename
        self.image = None

