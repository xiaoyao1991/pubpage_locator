
class Queue(object):
    def __init__(self):
        super(Queue, self).__init__()
        self.queue = []

    def push(self, obj):
        self.queue.append(obj)

    def pop(self):
        return self.queue.pop(0)

    def size(self):
        return len(self.queue)

    def is_empty(self):
        return len(self.queue) == 0
        