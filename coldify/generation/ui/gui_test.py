import sys
from PyQt4 import QtGui
from coldify.generation.recorder import Recorder


class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.recorder = Recorder()
        self.initUI()

    def initUI(self):
        grid = QtGui.QGridLayout()
        self.setLayout(grid)

        self.title = QtGui.QLabel("Cold Recorder")
        self.record = QtGui.QPushButton("Start Recording")
        self.record.clicked.connect(self.recordClicked)
        self.stop = QtGui.QPushButton("Stop Recording")
        self.stop.clicked.connect(self.stopClicked)
        self.stop.setEnabled(False)

        grid.addWidget(self.title, 0, 0)
        grid.addWidget(self.record, 1, 0)
        grid.addWidget(self.stop, 2, 0)

        self.move(300, 300)
        self.setWindowTitle('Cold Recorder')

    def recordClicked(self):
        print("Start Clicked")
        self.record.setEnabled(False)
        self.stop.setEnabled(True)
        self.recorder.startRecording()

    def stopClicked(self):
        print("Stop Clicked")
        self.record.setEnabled(True)
        self.stop.setEnabled(False)
        self.recorder.stopRecording()


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
