class MyQueue:
    def __init__(self):
        self._queue = []

    def enqueue(self, node):
        self._queue.append(node)

    def dequeue(self):
        first = self._queue[0]
        self._queue.pop(0)
        return first

    def is_empty(self):
        if len(self._queue) == 0:
            return True
        else:
            return False