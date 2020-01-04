from pyglet.gl import *

from little_doors.context import Context


# noinspection PyMethodMayBeStatic
class PixelCamera(object):

    def __init__(self):
        self._x = 0.0
        self._y = 0.0
        self._width = 640 * 0.5
        self._height = 480 * 0.5
        self._size_factor = 0.5

    @property
    def left(self):
        return self._x

    @property
    def bottom(self):
        return self._y

    @property
    def right(self):
        ctx = Context.current()
        width = ctx.window.width * self._size_factor
        return self._x + width

    @property
    def top(self):
        ctx = Context.current()
        height = ctx.window.height * self._size_factor
        return self._y + height

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def set_position(self, x, y):
        self._x = x
        self._y = y

    def window_to_world(self, x, y):
        """
        Takes coordinates on the window and transforms them to a point in the world's space.

        :returns: A tuple with the new x and y values
        """
        return self._x + x * self._size_factor, self._y + y * self._size_factor

    def clear(self):
        glClear(gl.GL_COLOR_BUFFER_BIT)

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

    def pop_state(self):
        glPopMatrix()
