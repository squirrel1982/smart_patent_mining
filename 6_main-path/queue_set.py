class Queue_Set(object):
    def __init__(self):
        self.queue = []
        self.size = 0
    def put(self,i):
        if i in self.queue:
            return False
        else:
            self.queue.insert(0,i)
            self.size = len(self.queue)
            return True
    def get(self):
        a = self.queue.pop()
        self.size = len(self.queue)
        return a
    def isEmpty(self):
        if self.size==0:
            return True
        else:
            return False
    def getSize(self):
        return self.size
        