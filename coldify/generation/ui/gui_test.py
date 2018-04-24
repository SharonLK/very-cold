import os
import random
import sys
from collections import namedtuple

from PyQt4 import QtGui

from coldify.generation.recorder import Recorder

Data = namedtuple("Data", ["sentence", "postfix"])


class Colors:
    START = "98B475"
    STOP = "F9C991"
    CANCEL = "AB4441"
    CANCEL_DISABLED = "585548"


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
        self.cancel_button = None
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

        self.record_button = QtGui.QPushButton("התחל להקליט")
        self.record_button.setStyleSheet(self.DEFAULT_BUTTON_STYLE + "background-color: #{};".format(Colors.START))
        self.record_button.setFixedHeight(40)
        self.record_button.clicked.connect(self.record_clicked)

        self.cancel_button = QtGui.QPushButton("בטל הקלטה")
        self.cancel_button.setStyleSheet(self.DEFAULT_BUTTON_STYLE + "background-color: #{}".format(Colors.CANCEL_DISABLED))
        self.cancel_button.setFixedHeight(40)
        self.cancel_button.setDisabled(True)
        self.cancel_button.clicked.connect(self.cancel_clicked)

        grid.addWidget(name_label, 0, 0, 1, 2)
        grid.addWidget(self.name, 1, 0, 1, 2)
        grid.addWidget(explanation, 2, 0, 1, 2)
        grid.addWidget(self.record_text, 3, 0, 1, 2)
        grid.addWidget(self.cancel_button, 4, 0)
        grid.addWidget(self.record_button, 4, 1)

        self.move(300, 300)
        self.setWindowTitle('Cold Recorder')

    def __set_sentence(self):
        self.record_text.setText(self.sentences[self.current_index].sentence)

    def record_clicked(self):
        if "התחל" in self.record_button.text():
            self.record_button.setText("סיים הקלטה")
            self.record_button.setStyleSheet(self.DEFAULT_BUTTON_STYLE + "background-color: #{};".format(Colors.STOP))
            self.recorder.startRecording()

            self.cancel_button.setDisabled(False)
            self.cancel_button.setStyleSheet(self.DEFAULT_BUTTON_STYLE + "background-color: #{}".format(Colors.CANCEL))
        elif "סיים" in self.record_button.text():
            self.record_button.setText("התחל להקליט")
            self.record_button.setStyleSheet(self.DEFAULT_BUTTON_STYLE + "background-color: #{};".format(Colors.START))
            self.recorder.stopRecording(
                os.path.join(self.dictPath, self.sentences[self.current_index].postfix + ".wav"))
            self.cancel_button.setDisabled(True)
            self.cancel_button.setStyleSheet(self.DEFAULT_BUTTON_STYLE + "background-color: #{}".format(Colors.CANCEL_DISABLED))

            self.current_index += 1
            self.__set_sentence()

    def cancel_clicked(self):
        self.record_button.setText("התחל להקליט")
        self.record_button.setStyleSheet(self.DEFAULT_BUTTON_STYLE + "background-color: #{};".format(Colors.START))
        self.cancel_button.setStyleSheet(self.DEFAULT_BUTTON_STYLE + "background-color: #{}".format(Colors.CANCEL_DISABLED))
        self.recorder.stopRecording("", save=False)


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
