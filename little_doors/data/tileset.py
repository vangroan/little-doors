import pyglet

from little_doors.tile import Tile


def create_tile_set():
    tiles = [
        Tile(1, "template", resource_filename='./resources/art/tile-template.png', anchor=(16.0, 8.0), depth=2.0,
             dimension=(1.0, 1.0, 1.0), tile_size=(32.0, 32.0)),
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
