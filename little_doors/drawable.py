from typing_extensions import Protocol


class Drawable(Protocol):
    """
    An entity that can br drawn to a render target.
    """

    def draw(self):
        """
        Delegates draw call to drawable children.
        """
        raise NotImplementedError()
