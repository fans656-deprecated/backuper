# coding: utf-8
import Queue
import time

from PySide.QtGui import *
from PySide.QtCore import *

from scanner import Scanner

class Widget(QDialog):

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.setWindowTitle('File Scanner')

        self.scanningList = QTextEdit()
        self.dirEdit = QLineEdit()
        self.openButton = QPushButton('&Open')
        self.scanButton = QPushButton('&Scan')
        # TODO: add pause/stop
        #self.stopButton = QPushButton('Stop')

        self.scanningList.setReadOnly(True)
        self.dirEdit.setEnabled(False)
        self.scanButton.setEnabled(False)

        self.openButton.clicked.connect(self.openDir)
        self.scanButton.clicked.connect(self.scanDir)

        lt = QVBoxLayout()
        lt.addWidget(self.scanningList)

        lt_ = QHBoxLayout()
        lt_.addWidget(self.dirEdit)
        lt_.addWidget(self.openButton)
        lt_.addWidget(self.scanButton)
        lt.addLayout(lt_)

        self.setLayout(lt)

        self.idleTimer = QTimer()
        self.idleTimer.setInterval(0)
        self.idleTimer.timeout.connect(self.onIdle)

        self.openDir(QDir('D:/Books').canonicalPath())

        self.idleI = 0
        self.totFiles = 0

    def openDir(self, path=None):
        if path is None:
            path = QFileDialog.getExistingDirectory()
        if path:
            self.dirEdit.setText(path)
            self.scanButton.setEnabled(True)
        else:
            self.scanButton.setEnabled(False)

    def scanDir(self):
        self.scanningList.clear()
        path = self.dirEdit.text()

        self.scanner = Scanner(path)
        self.fpathsQueue = self.scanner.queue

        self.idleTimer.start()
        self.scanner.start()

        self.beg = time.time()

    def onIdle(self):
        try:
            for _ in xrange(10):
                fpath = self.fpathsQueue.get(False)
                if fpath is None:
                    self.idleTimer.stop()
                    elapsed = time.time() - self.beg
                    s = 'scan finished. {} files in {} onIdle, in {:.1f}s'.format(self.totFiles, self.idleI, elapsed)
                    QMessageBox.information(self, 'Result', s)
                    break
                self.scanningList.append(fpath)
                self.totFiles += 1
        except Queue.Empty:
            pass
        self.idleI += 1

app = QApplication([])
w = Widget()
w.resize(800, 480)
w.show()
app.exec_()
