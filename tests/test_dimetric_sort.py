from little_doors import data
from little_doors.tile import Tile
from little_doors.terrain import Terrain
from little_doors.iso import create_dimetric_cmp


def test_dimetric_sort():
    # assume
    terrain = Terrain((8, 8))
    terrain.load_tile_set(data.tileset.create_tile_set())
    terrain.load_tile_data([
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 0, 0, 1, 1, 0, 0, 1,
        1, 0, 1, 1, 1, 1, 0, 1,
        1, 1, 1, 0, 0, 1, 1, 1,
        1, 1, 1, 0, 0, 1, 1, 1,
        1, 0, 1, 1, 1, 1, 0, 1,
        1, 0, 0, 1, 1, 0, 0, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
    ])

    # act
    tiles = filter(lambda e: terrain.get_sprite(e[1], e[2]),
                   ((idx, coord[0], coord[1]) for idx, coord in enumerate(terrain)))
    tiles = list(tiles)
    tiles.sort(key=create_dimetric_cmp(terrain), reverse=True)

    # assert
    print(tiles)
    assert False

