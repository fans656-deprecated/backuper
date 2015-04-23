import time
import os

from PySide.QtCore import *

class Scanner(QThread):

    fileScanned = Signal(unicode)

    def run(self):
        for dirpath, dirnames, filenames in os.walk(self.path):
            for filename in filenames:
                fpath = os.path.join(dirpath, filename)
                self.fileScanned.emit(fpath)
