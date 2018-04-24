import os
import random
import sys
from random import shuffle

from PyQt4 import QtGui

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

        nameLabel = QtGui.QLabel("שם (באנגלית)")
        nameLabel.setStyleSheet("font-weight: bold; font-size: 16px;")

        self.name = QtGui.QLineEdit()
        self.name.setFixedWidth(300)
        self.name.setStyleSheet("font-size: 16px;")

        # Aaver Shidur

        aaverShidurExpLabel = QtGui.QLabel(
            r"כשאת\ה מוכן, לחץ על הכפתור ואמור את המשפט הבא, לאחר מכן לחץ על הכפתור פעם נוספת")
        aaverShidurExpLabel.setStyleSheet("font-weight: bold; font-size: 16px;")

        self.aaverShidurRecordLabel = QtGui.QLabel()
        self.aaverShidurRecordLabel.setStyleSheet(
            "font-weight: bold; font-size: 16px; padding: 20px 20px 20px 20px")
        self.aaverShidurNumber = random.randint(0, 24)
        self.aaverShidurRecordLabel.setText("העבר מודול {} לשידור".format(self.aaverShidurNumber))

        self.aaverShidurButton = QtGui.QPushButton("Start Recording")
        self.aaverShidurButton.setStyleSheet(self.DEFAULT_BUTTON_STYLE +
                                             "background-color: #98B475;")
        self.aaverShidurButton.setFixedHeight(40)
        self.aaverShidurButton.clicked.connect(self.recordAaverShidurClicked)

        # Number Sequence

        numSeqExpLabel = QtGui.QLabel(
            r"כשאת\ה מוכן, לחץ על הכפתור ואמור את המפרים משמאל לימין, לאחר מכן לחץ על הכפתור פעם נוספת")
        numSeqExpLabel.setStyleSheet("font-weight: bold; font-size: 16px;")

        self.numSeqRecordLabel = QtGui.QLabel()
        self.numSeqRecordLabel.setStyleSheet("font-weight: bold; font-size: 16px; padding: 20px 20px 20px 20px")
        self.numSeqRecordLabel.setText("    ".join([str(num) for num in self.sequence]))

        self.numSeqButton = QtGui.QPushButton("Start Recording")
        self.numSeqButton.setStyleSheet(self.DEFAULT_BUTTON_STYLE +
                                        "background-color: #98B475;")
        self.numSeqButton.setFixedHeight(40)
        self.numSeqButton.clicked.connect(self.recordNumberSequenceClicked)

        grid.addWidget(nameLabel, 0, 0)
        grid.addWidget(self.name, 1, 0)
        grid.addWidget(aaverShidurExpLabel, 2, 0)
        grid.addWidget(self.aaverShidurRecordLabel, 3, 0)
        grid.addWidget(self.aaverShidurButton, 4, 0)
        grid.addWidget(numSeqExpLabel, 5, 0)
        grid.addWidget(self.numSeqRecordLabel, 6, 0)
        grid.addWidget(self.numSeqButton, 7, 0)

        self.move(300, 300)
        self.setWindowTitle('Cold Recorder')

    def __generate_sequence(self):
        self.sequence = list(range(0, 25))
        shuffle(self.sequence)

    def recordAaverShidurClicked(self):
        if "Start" in self.aaverShidurButton.text():
            self.aaverShidurButton.setText("Stop Recording")
            self.aaverShidurButton.setStyleSheet(self.DEFAULT_BUTTON_STYLE +
                                                 "background-color: #AB4441;")
            self.recorder.startRecording()
        elif "Stop" in self.aaverShidurButton.text():
            self.aaverShidurButton.setText("Start Recording")
            self.aaverShidurButton.setStyleSheet(self.DEFAULT_BUTTON_STYLE +
                                                 "background-color: #98B475;")
            self.recorder.stopRecording(
                os.path.join(self.dictPath, self.name.text() + "-1-" + str(self.aaverShidurNumber) + ".wav"))
            self.aaverShidurNumber = random.randint(0, 24)
            self.aaverShidurRecordLabel.setText("העבר מודול {} לשידור".format(self.aaverShidurNumber))

    def recordAaverAazanaClicked(self):
        pass

    def recordAktzaaClicked(self):
        pass

    def recordGibuiClicked(self):
        pass

    def recordNumberSequenceClicked(self):
        if "Start" in self.numSeqButton.text():
            self.numSeqButton.setText("Stop Recording")
            self.numSeqButton.setStyleSheet(self.DEFAULT_BUTTON_STYLE +
                                            "background-color: #AB4441;")
            self.recorder.startRecording()
        elif "Stop" in self.numSeqButton.text():
            self.numSeqButton.setText("Start Recording")
            self.numSeqButton.setStyleSheet(self.DEFAULT_BUTTON_STYLE +
                                            "background-color: #98B475;")
            self.recorder.stopRecording(os.path.join(self.dictPath, self.name.text() + "-6-" + "-".join(
                [str(num) for num in self.sequence]) + ".wav"))
            self.__generate_sequence()
            self.numSeqRecordLabel.setText("    ".join(
                [str(num) for num in self.sequence]))


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
