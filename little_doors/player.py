import pyglet

from little_doors.iso import cart_to_iso


class Player(object):

    def __init__(self, pos3d=(0.0, 0.0, 0.0), tile_size=(32.0, 32.0, 16.0)):
        """
        :param pos3d: 3D cartesian coordinates.
        :param tile_size: Tuple of the tile 2D size. Width and height; the third coordinate
                          is the virtual "depth" of the isometric tile on the 2D screen.
        """

        self._pos3d = (0.0, 0.0, 0.0)
        self._tile_size = tile_size
        self._anchor = (24.0, 8.0)

        self.walk_speed = 4.0
        self.mode = 0

        tex = pyglet.image.atlas.TextureAtlas()
        base_tex = tex.add(pyglet.image.load('resources/art/player.png'))

        self.sprite = pyglet.sprite.Sprite(base_tex)
        self.pos3d = pos3d

    @property
    def pos3d(self):
        return self._pos3d

    @pos3d.setter
    def pos3d(self, val):
        """
        Sets the player's position in 3D space, and its sprite in 2D space.
        """
        (i, j, k) = cart_to_iso(*val)
        (ti, tj, tk) = self._tile_size
        (ax, ay) = self._anchor
        self.sprite.x = (i * ti) - ax
        self.sprite.y = (j * tj + k * tk) - ay
        self._pos3d = val

    def update(self, dt):
        p = self._pos3d
        diff = self.walk_speed * dt

        # TODO: Remove
        # Just makes the player move around the map
        if self.mode == 0:
            self.pos3d = (p[0] + diff, p[1], p[2])
            if self._pos3d[0] >= 7.0:
                self.mode = 1
        elif self.mode == 1:
            self.pos3d = (p[0], p[1] + diff, p[2])
            if self._pos3d[1] >= 7.0:
                self.mode = 2
        elif self.mode == 2:
            self.pos3d = (p[0] - diff, p[1], p[2])
            if self._pos3d[0] <= 0.0:
                self.mode = 3
        elif self.mode == 3:
            self.pos3d = (p[0], p[1] - diff, p[2])
            if self._pos3d[1] <= 0.0:
                self.mode = 0

    def draw(self):
        self.sprite.draw()
