import sys
import os
from PyQt4 import QtGui
from random import shuffle
from coldify.generation.recorder import Recorder


class Window(QtGui.QWidget):
    DEFAULT_BUTTON_STYLE = "border-radius: 2px;" + \
        "font-weight: bold;" + \
        "font-size: 14px;" + \
        "border-color: black;" + \
        "border-width: 1px;" + \
        "border-style: outset;"

    def __init__(self):
        super(Window, self).__init__()

        self.recorder = Recorder()
        self.dictPath = os.path.dirname(os.path.realpath(__file__))
        self.__generate_sequence()
        self.initUI()

    def initUI(self):
        grid = QtGui.QGridLayout()
        grid.setMargin(10)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)
        self.setLayout(grid)

        nameLabel = QtGui.QLabel("Name (in English):")
        nameLabel.setStyleSheet("font-weight: bold; font-size: 16px;")

        self.name = QtGui.QLineEdit()
        self.name.setFixedWidth(300)
        self.name.setStyleSheet("font-size: 16px;")

        explanationLabel = QtGui.QLabel(
            "When you are ready, press Start, read the following message from left to right and then hit Stop")
        nameLabel.setStyleSheet("font-weight: bold; font-size: 16px;")

        self.recordingLabel = QtGui.QLabel()
        self.recordingLabel.setStyleSheet(
            "font-weight: bold; font-size: 16px; padding: 20px 20px 20px 20px")
        self.recordingLabel.setText("    ".join(
            [str(num) for num in self.sequence]))

        self.record = QtGui.QPushButton("Start Recording")
        self.record.setStyleSheet(self.DEFAULT_BUTTON_STYLE +
                                  "background-color: #98B475;")
        self.record.setFixedHeight(40)
        self.record.clicked.connect(self.recordClicked)

        grid.addWidget(nameLabel, 0, 0)
        grid.addWidget(self.name, 1, 0)
        grid.addWidget(explanationLabel, 2, 0)
        grid.addWidget(self.recordingLabel, 3, 0)
        grid.addWidget(self.record, 4, 0)

        self.move(300, 300)
        self.setWindowTitle('Cold Recorder')

    def __generate_sequence(self):
        self.sequence = list(range(0, 25))
        shuffle(self.sequence)

    def recordClicked(self):
        if "Start" in self.record.text():
            self.record.setText("Stop Recording")
            self.record.setStyleSheet(self.DEFAULT_BUTTON_STYLE +
                                      "background-color: #AB4441;")
            self.recorder.startRecording()
        elif "Stop" in self.record.text():
            self.record.setText("Start Recording")
            self.record.setStyleSheet(self.DEFAULT_BUTTON_STYLE +
                                      "background-color: #98B475;")
            self.recorder.stopRecording(os.path.join(self.dictPath, self.name.text(
            ) + "-6-" + "-".join([str(num) for num in self.sequence]) + ".wav"))
            self.__generate_sequence()
            self.recordingLabel.setText("    ".join(
                [str(num) for num in self.sequence]))


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
