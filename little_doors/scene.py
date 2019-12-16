from abc import ABC, abstractmethod


class Scene(ABC):
    def start(self, context):
        pass

    def stop(self, context):
        pass

    def pause(self, context):
        pass

    def resume(self, context):
        pass

    def on_update(self, dt):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_motion(self, context, x, y, dx, dy):
        pass

    def on_draw(self, context):
        pass


class SceneStack(object):
    def __init__(self):
        self._scenes = []

    @property
    def top(self):
        if self._scenes:
            return self._scenes[len(self._scenes) - 1]
        return None

    def push(self, scene):
        if self._scenes:
            self._scenes[len(self._scenes) - 1].stop(None)
            self._scenes.pop(len(self._scenes) - 1)

        self._scenes.append(scene)
        self._scenes[len(self._scenes) - 1].start(None)

    def pop(self):
        raise NotImplementedError()

    def replace(self, scene):
        raise NotImplementedError()

    def _switch_to(self, scene):
        raise NotImplementedError()
