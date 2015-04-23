import os
import threading
import Queue

class Scanner(threading.Thread):

    def __init__(self, path, start=False):
        super(Scanner, self).__init__()
        self.path = path
        self.queue = Queue.Queue()
        if start:
            self.start()

    def run(self):
        for dirpath, dirnames, filenames in os.walk(self.path):
            for filename in filenames:
                fpath = os.path.join(dirpath, filename)
                self.queue.put(fpath)
        self.queue.put(None)
