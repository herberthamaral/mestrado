# encoding: utf-8

class PriorityQueue(object):
    items = []
    def put(self, item):
        self.items.append(item)

    def get(self):
        if not self.items:
            raise StopIteration
        item = sorted(self.items, key=lambda x: x[0])[0]
        self.items.remove(item)
        return item
