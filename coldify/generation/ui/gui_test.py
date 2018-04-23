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
        grid.setMargin(10)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)
        self.setLayout(grid)

        self.title = QtGui.QLabel("Cold Recorder")

        self.path = QtGui.QLineEdit()
        self.path.setFixedWidth(300)
        self.path.setText("C:\\Users\\Sharon\\Desktop\\")

        self.record = QtGui.QPushButton("Start Recording")
        self.record.setStyleSheet("border-radius: 2px;" +
                                  "background-color: #98B475;"
                                  "font-weight: bold;" +
                                  "font-size: 18;" +
                                  "border-color: black;" +
                                  "border-width: 1px;" +
                                  "border-style: outset;")
        self.record.setFixedHeight(40)
        self.record.clicked.connect(self.recordClicked)

        grid.addWidget(self.title, 0, 0)
        grid.addWidget(QtGui.QLabel("Save recording to:"), 1, 0)
        grid.addWidget(self.path, 2, 0)
        grid.addWidget(self.record, 3, 0)

        self.move(300, 300)
        self.setWindowTitle('Cold Recorder')

    def recordClicked(self):
        if "Start" in self.record.text():
            self.record.setText("Stop Recording")
            self.record.setStyleSheet("border-radius: 2px;" +
                                    "background-color: #AB4441;"
                                    "font-weight: bold;" +
                                    "font-size: 18;" +
                                    "border-color: black;" +
                                    "border-width: 1px;" +
                                    "border-style: outset;")
            self.recorder.startRecording()
        elif "Stop" in self.record.text():
            self.record.setText("Start Recording")
            self.record.setStyleSheet("border-radius: 2px;" +
                                    "background-color: #98B475;"
                                    "font-weight: bold;" +
                                    "font-size: 18;" +
                                    "border-color: black;" +
                                    "border-width: 1px;" +
                                    "border-style: outset;")
            self.recorder.stopRecording(self.path.text())


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
