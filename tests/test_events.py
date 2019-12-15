from little_doors.event import EventMixin


class Subject(EventMixin, object):
    pass


class Observer(object):

    def __init__(self):
        self.invocations = []

    def on_test(self, one, two, three):
        self.invocations.append((one, two, three))


def test_trigger():
    """
    Should call handler when triggered.
    """
    # assume
    subject = Subject()
    observer = Observer()
    subject.handle('test', observer.on_test)

    # act
    subject.trigger('test', 1, 'one', True)

    # assert
    assert observer.invocations[0] == (1, 'one', True), "observer did not receive event"


def test_remove_handler():
    """
    Should remove handler.
    """
    # assume
    subject = Subject()
    observer = Observer()
    subject.handle('test', observer.on_test)

    # act
    subject.remove_handler('test', observer.on_test)

    # assert
    assert subject.event_handler_count == 0, "subject still have an event handler registered"
