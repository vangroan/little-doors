from pyglet.gl import *
import pyglet


class PixelCamera(object):

    def __init__(self):
        self._x = 0.0
        self._y = 0.0
        self._width = 640 * 0.5
        self._height = 480 * 0.5

    @property
    def left(self):
        return self._x

    @property
    def bottom(self):
        return self._y

    @property
    def right(self):
        return self._x + self._width

    @property
    def top(self):
        return self._y + self._height

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def set_position(self, x, y):
        self._x = x
        self._y = y

    def push_state(self):
        # Save the current matrix
        glPushMatrix()

        # Initialize projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Initialize model view matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Set orthographic projection matrix
        glOrtho(self.left, self.right, self.bottom, self.top, 1, -1)

        # Pixelate
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    # noinspection PyMethodMayBeStatic
    def pop_state(self):
        glPopMatrix()
