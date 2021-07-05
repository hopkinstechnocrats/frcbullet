class EventLoop:

    def __init__(self):
        self.queues = []
        self.values = []

    def consume(self, queues):

