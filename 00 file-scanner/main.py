# coding: utf-8
import Queue
import time
import os
import threading

from PySide.QtGui import *
from PySide.QtCore import *

from scanner import Scanner

class Widget(QDialog):

    SCAN_BUTTON_TEXT = '&Scan'
    SCAN_BUTTON_PAUSE_TEXT = '&Pause'
    SCAN_BUTTON_RESUME_TEXT = '&Resume'
    INIT_PATH = 'E:/Movie'
    #INIT_PATH = '.'

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.setWindowTitle('File Scanner')

        self.scanningList = QTextEdit()
        self.dirEdit = QLineEdit()
        self.openButton = QPushButton('&Open')
        self.scanButton = QPushButton(self.SCAN_BUTTON_TEXT)
        self.stopButton = QPushButton('Stop')

        self.scanningList.setReadOnly(True)
        self.dirEdit.setEnabled(False)
        self.scanButton.setEnabled(False)
        self.stopButton.setEnabled(False)

        self.openButton.clicked.connect(self.openDir)
        self.scanButton.clicked.connect(self.onScanButtonClicked)
        self.stopButton.clicked.connect(self.stopScan)

        lt = QVBoxLayout()
        lt.addWidget(self.scanningList)

        lt_ = QHBoxLayout()
        lt_.addWidget(self.dirEdit)
        lt_.addWidget(self.openButton)
        lt_.addWidget(self.scanButton)
        lt_.addWidget(self.stopButton)
        lt.addLayout(lt_)

        self.setLayout(lt)

        self.controlEvent = threading.Condition()
        self.status = ['stopped']

        self.idleTimer = QTimer()
        self.idleTimer.setInterval(0)
        self.idleTimer.timeout.connect(self.onIdle)

        if not os.path.exists(self.INIT_PATH):
            self.INIT_PATH = '.'
        self.openDir(QDir(self.INIT_PATH).canonicalPath())

    def onScanButtonClicked(self):
        if self.status[0] == 'stopped':
            self.scanDir()
        elif self.status[0] == 'running':
            self.pauseScan()
        elif self.status[0] == 'paused':
            self.resumeScan()

    def openDir(self, path=None):
        if path is None:
            path = QFileDialog.getExistingDirectory()
        if path:
            self.dirEdit.setText(path)
            self.scanButton.setEnabled(True)

    def scanDir(self):
        self.scanningList.clear()
        path = self.dirEdit.text()

        # construct a new scanner every time
        # so we won't bother ungot items if we do a premature stop
        self.scanner = Scanner(path, self.controlEvent, self.status)
        self.fpathsQueue = self.scanner.queue

        self.status[0] = 'running'
        self.scanButton.setText(self.SCAN_BUTTON_PAUSE_TEXT)
        self.stopButton.setEnabled(True)

        self.idleTimer.start()
        self.scanner.start()

    def pauseScan(self):
        with self.controlEvent:
            self.status[0] = 'paused'
            self.idleTimer.stop()
        self.scanButton.setText(self.SCAN_BUTTON_RESUME_TEXT)

    def resumeScan(self):
        with self.controlEvent:
            self.status[0] = 'running'
            self.idleTimer.start()
            self.controlEvent.notifyAll()
        self.scanButton.setText(self.SCAN_BUTTON_PAUSE_TEXT)

    def stopScan(self):
        # stop idle so we won't get item from the fpathQueue anymore
        self.idleTimer.stop()
        # trigger the event
        with self.controlEvent:
            self.status[0] = 'stopped'
        # set ui state
        self.scanButton.setText(self.SCAN_BUTTON_TEXT)
        self.stopButton.setEnabled(False)

    def onIdle(self):
        try:
            for _ in xrange(10):
                fpath = self.fpathsQueue.get(False)
                if fpath is None:
                    self.stopScan()
                    break
                self.scanningList.append(fpath)
        except Queue.Empty:
            pass

app = QApplication([])
w = Widget()
w.resize(800, 480)
w.show()
app.exec_()
