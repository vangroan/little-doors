from little_doors.event import EventMixin


class MenuError(Exception):
    pass


class MenuButton(EventMixin, object):
    def __init__(self, label="Button"):
        super().__init__()
        self.label = label


class Menu(object):
    def __init__(self):
        pass

    def add(self, button):
        pass
