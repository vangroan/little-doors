import pyglet

from little_doors.tile import Tile


def create_tile_set():
    tiles = [
        Tile(1, "template-1-1-1", resource_filename='./resources/art/tile-template.png', anchor=(16.0, 8.0), depth=1.0,
             dimension=(1.0, 1.0, 1.0), tile_size=(32.0, 32.0)),
        Tile(2, "template-2-1-1", resource_filename='./resources/art/tile-template-2-1-1.png', anchor=(16.0, 8.0), depth=1.0,
             dimension=(2.0, 1.0, 1.0), tile_size=(48.0, 40.0)),
        Tile(3, "template-1-2-1", resource_filename='./resources/art/tile-template-1-2-1.png', anchor=(32.0, 8.0), depth=1.0,
             dimension=(1.0, 2.0, 1.0), tile_size=(48.0, 40.0)),
        Tile(4, "template-1-1-2", resource_filename='./resources/art/tile-template-1-1-2.png', anchor=(16.0, 8.0), depth=1.0,
             dimension=(1.0, 1.0, 2.0), tile_size=(32.0, 48.0)),
        Tile(5, "template-2-2-1", resource_filename='./resources/art/tile-template-2-2-1.png', anchor=(32.0, 8.0), depth=1.0,
             dimension=(2.0, 2.0, 1.0), tile_size=(64.0, 48.0)),
    ]

    images = dict()

    # Load resources
    for tile in tiles:
        # Don't load the same images multiple times
        if tile.resource_filename in images:
            image = images[tile.resource_filename]
        else:
            image = pyglet.image.load(tile.resource_filename)

        tile.image = image

    return {tile.index: tile for tile in tiles}
