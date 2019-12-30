# TODO: Weak references to handlers


class EventError(Exception):
    pass


class EventMixin(object):
    """
    Adds event emitting to a class, turning it into an observable.

    This class will hold references to handlers.
    """

    def __init__(self):
        self.__event_handlers = dict()

    def register_event_types(self, *event_types):
        for event in event_types:
            if event not in self.__event_handlers:
                self.__event_handlers[event] = []

    def handle(self, event_name, handler):
        """
        Registers a function to receive events with the given name.

        :param event_name: Name of events that the handler will receive.
        :param handler: Function that will receive the specified events.
        """
        if event_name not in self.__event_handlers:
            self.__event_handlers[event_name] = []

        self.__event_handlers[event_name].append(handler)

    def remove_handler(self, event_name, handler):
        """
        Unregisters the given handler.
        """
        if event_name in self.__event_handlers:
            handlers = self.__event_handlers[event_name]
            handlers.remove(handler)

    @property
    def event_handler_count(self):
        """
        The total number of handlers currently registered.
        """
        agg = 0
        for event_name in self.__event_handlers:
            agg += len(self.__event_handlers[event_name])
        return agg

    def trigger(self, event_name, *args, **kwargs):
        """
        Emits an event, dispatching it to all handlers that have been registered
        against the event name.

        The given arguments and keyword arguments will be passed to each handler.
        """
        for handler in self.__event_handlers[event_name]:
            handler(*args, **kwargs)
