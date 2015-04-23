# coding: utf-8
# TODO: 解决扫描大量文件时GUI假死现象
# 比如扫描 D:/Books
# 猜测原因是太多 message 被塞进GUI的event loop
from PySide.QtGui import *
from PySide.QtCore import *

from scanner import Scanner

class Widget(QDialog):

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.setWindowTitle('File Scanner')

        self.scannerThread = Scanner()
        self.scannerThread.fileScanned.connect(self.onFileScanned)

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

        self.openDir(QDir().canonicalPath())

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
        self.scannerThread.path = path
        self.scannerThread.start()

    def onFileScanned(self, path):
        self.scanningList.append(path)

    # override `done` rather than `closeEvent`
    # because otherwise the escape key press will not
    # trigger the `closeEvent`
    def done(self, r):
        if self.scannerThread.isRunning():
            self.scannerThread.terminate()
        super(Widget, self).done(r)

app = QApplication([])
w = Widget()
w.resize(800, 480)
w.show()
app.exec_()
