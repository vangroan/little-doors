import pyglet
from pyglet.image.atlas import TextureBin

from little_doors.event import EventMixin


class MenuError(Exception):
    pass


class MenuButton(EventMixin, object):
    def __init__(self, label="Button", x=0, y=0, on_release=None):
        super().__init__()
        self.register_event_types('press', 'release')

        self.label = pyglet.text.Label(text=label, x=x + 64, y=y + 8, anchor_x='center', align='center')
        self.hovering = False
        self.enabled = True
        self.pressed = False

        tex_bin = TextureBin()
        self.up_tex = tex_bin.add(pyglet.image.load('./resources/art/btn-default-up-1.png'))
        self.down_tex = tex_bin.add(pyglet.image.load('./resources/art/btn-default-down-1.png'))
        self.hover_tex = tex_bin.add(pyglet.image.load('./resources/art/btn-default-hover-1.png'))
        self.disable_tex = tex_bin.add(pyglet.image.load('./resources/art/btn-default-disable-1.png'))
        self.tex_bin = tex_bin

        self.background = pyglet.sprite.Sprite(self.up_tex)

        if on_release:
            self.handle('release', on_release)

        self.x = x
        self.y = y

    @property
    def x(self):
        return self.background.x

    @x.setter
    def x(self, val):
        self.background.x = val
        self.label.x = val + (self.background.width / 2)

    @property
    def y(self):
        return self.background.y

    @y.setter
    def y(self, val):
        self.background.y = val
        self.label.y = val + 8

    @property
    def height(self):
        return self.background.height

    def intersects(self, x, y):
        bx = self.background.x
        by = self.background.y
        bw = self.background.width
        bh = self.background.height
        return (bx <= x <= bx + bw) and (by <= y <= by + bh)

    def set_hover_over(self):
        self.hovering = True
        self.background.image = self.hover_tex

    def set_hover_out(self):
        self.hovering = False
        self.background.image = self.up_tex

    def set_down(self):
        self.pressed = True
        self.background.image = self.down_tex

    def set_up(self):
        self.pressed = False
        self.background.image = self.up_tex

    def on_draw(self):
        self.background.draw()
        self.label.draw()


class Menu(object):
    def __init__(self):
        self._buttons = []

    def add(self, button):
        self._buttons.append(button)

    def on_mouse_press(self, x, y, button, modifiers):
        for button in self._buttons:  # type: MenuButton
            if button.intersects(x, y) and button.enabled:
                button.trigger('press', x, y, button, modifiers)
                button.set_down()
                break

    def on_mouse_release(self, x, y, button, modifiers):
        for button in self._buttons:  # type: MenuButton
            if button.intersects(x, y) and button.enabled:
                if not button.pressed:
                    continue
                button.trigger('release', x, y, button, modifiers)
                button.set_up()
                break
        else:
            # Unhandled
            for button in self._buttons:
                if button.pressed:
                    button.set_up()

    def on_mouse_motion(self, x, y, dx, dy):
        for button in self._buttons:  # type: MenuButton
            if button.intersects(x, y) and button.enabled:
                if button.pressed:
                    continue
                if not button.hovering:
                    button.set_hover_over()
            else:
                if button.hovering:
                    button.set_hover_out()

    def on_draw(self):
        for button in self._buttons:
            button.on_draw()
