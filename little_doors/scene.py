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

    def update(self, context):
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
