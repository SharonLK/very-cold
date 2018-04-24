import os
import random
import sys
from collections import namedtuple

from PyQt4 import QtGui

from coldify.generation.recorder import Recorder

Data = namedtuple("Data", ["sentence", "postfix"])


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

        self.current_index = 0
        self.sentences = []
        self.init_sentences()
        
        self.name = None
        self.record_text = None
        self.record_button = None
        self.init_ui()

    def init_sentences(self):
        for i in range(1, 24, 2):
            self.sentences.append(Data("העבר מודול {} לשידור".format(i), "-1-{}".format(i)))
        for i in range(0, 24, 2):
            self.sentences.append(Data("העבר מודול {} להאזנה".format(i), "-2-{}".format(i)))
        for i in range(1, 24, 2):
            d1, d2, d3, d4 = random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)
            self.sentences.append(Data("בצע הקצאה במודול {} לערוץ {}, {}, {}, {}".format(i, d1, d2, d3, d4),
                                       "-3-{}-{}-{}-{}-{}".format(i, d1, d2, d3, d4)))
        for i in range(1, 3):
            self.sentences.append(Data("העבר לגיבוי {}".format(i), "-4-{}".format(i)))
        for i in range(1, 3):
            self.sentences.append(Data("העבר לגיבוי {}".format(i), "-4-{}".format(i)))
        for _ in range(5):
            nums = list(range(0, 25))
            random.shuffle(nums)
            nums = [str(num) for num in nums]
            self.sentences.append(Data("➡➡➡ {}".format(" ".join(nums)), "-5-{}".format(" ".join(nums))))

    def init_ui(self):
        # Set the Grid Layout as the layout for this GUI
        grid = QtGui.QGridLayout()
        grid.setMargin(10)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)
        self.setLayout(grid)

        name_label = QtGui.QLabel("Name (in English)")
        name_label.setStyleSheet("font-weight: bold; font-size: 16px;")

        self.name = QtGui.QLineEdit()
        self.name.setFixedWidth(300)
        self.name.setStyleSheet("font-size: 16px;")

        explanation = QtGui.QLabel("Press on the Record button, read the text and then press it again")
        explanation.setStyleSheet("font-weight: bold; font-size: 16px;")

        self.record_text = QtGui.QLabel()
        self.record_text.setStyleSheet("font-weight: bold; font-size: 16px; padding: 20px 20px 20px 20px")
        self.__set_sentence()

        self.record_button = QtGui.QPushButton("Start Recording")
        self.record_button.setStyleSheet(self.DEFAULT_BUTTON_STYLE + "background-color: #98B475;")
        self.record_button.setFixedHeight(40)
        self.record_button.clicked.connect(self.record_clicked)

        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name, 1, 0)
        grid.addWidget(explanation, 2, 0)
        grid.addWidget(self.record_text, 3, 0)
        grid.addWidget(self.record_button, 4, 0)

        self.move(300, 300)
        self.setWindowTitle('Cold Recorder')

    def __set_sentence(self):
        self.record_text.setText(self.sentences[self.current_index].sentence)

    def record_clicked(self):
        if "Start" in self.record_button.text():
            self.record_button.setText("Stop Recording")
            self.record_button.setStyleSheet(self.DEFAULT_BUTTON_STYLE + "background-color: #AB4441;")
            self.recorder.startRecording()
        elif "Stop" in self.record_button.text():
            self.record_button.setText("Start Recording")
            self.record_button.setStyleSheet(self.DEFAULT_BUTTON_STYLE + "background-color: #98B475;")
            self.recorder.stopRecording(
                os.path.join(self.dictPath, self.sentences[self.current_index].postfix + ".wav"))

            self.current_index += 1
            self.__set_sentence()


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
