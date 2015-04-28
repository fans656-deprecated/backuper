import os
import threading
import Queue
import time

class Scanner(threading.Thread):

    def __init__(self, path, controlEvent, status):
        super(Scanner, self).__init__()
        self.path = path
        self.queue = Queue.Queue()
        self.controlEvent = controlEvent
        self.status = status

    def run(self):
        for dirpath, dirnames, filenames in os.walk(self.path):
            for filename in filenames:
                # check for pause/stop
                with self.controlEvent:
                    while True:
                        if self.status[0] == 'paused':
                            self.controlEvent.wait()
                        elif self.status[0] == 'running':
                            break
                        elif self.status[0] == 'stopped':
                            return
                # report file path
                fpath = os.path.join(dirpath, filename)
                self.queue.put(fpath)
        self.queue.put(None)
