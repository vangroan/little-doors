"""
Miscellaneous mix-ins.
"""

from abc import ABC, abstractmethod

from little_doors.aabb import AABB3D


# noinspection PyAttributeOutsideInit
class MapObjectMixin(ABC):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)

        # 3D map index
        instance.__map_pos = (0, 0, 0)

        return instance

    @property
    def map_pos(self):
        return self.__map_pos

    @map_pos.setter
    def map_pos(self, pos):
        self.__map_pos = pos


class Box3DMixin(ABC):
    """
    Objects that can collide in 3-dimensional space.
    """

    @abstractmethod
    @property
    def aabb3d(self) -> AABB3D:
        """
        Bounding box that reflects the object's position and size in 3-dimensional space.

        Should return a reference to the bounding box object, and not a copy, because the reference is
        used as the box's identity in collections and spatial indexes.

        The position of the box should be kept up to date with the object's position in 3D space.

        :return: Reference 3D bounding box.
        """
        raise NotImplementedError()


class DrawableMixin(ABC):
    """
    Objects that contain drawable primitives, like sprites.
    """

    @abstractmethod
    def draw(self):
        """
        Delegates draw call to drawable children.
        """
        raise NotImplementedError()
