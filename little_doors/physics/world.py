class PhysicsWorld3D(object):
    def __init__(self):
        pass

    def add_body(self, body):
        raise NotImplementedError()

    def step(self, delta_time):
        raise NotImplementedError()
