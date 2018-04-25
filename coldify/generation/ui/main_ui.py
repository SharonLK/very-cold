import os
import random
import sys
from collections import namedtuple

from PyQt4 import QtGui

from coldify.generation.recorder import Recorder

Data = namedtuple("Data", ["sentence", "postfix"])


class Colors:
    START = "98B475"  # Green
    STOP = "F9C991"  # Orange
    CANCEL = "AB4441"  # Red
    CANCEL_DISABLED = "585548"  # Gray
    PROCESS = "79B0C0"  # Blue


class SentenceWidget(QtGui.QWidget):
    def __init__(self, sentence):
        super().__init__()

        self.sentence = sentence

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(QtGui.QLabel(sentence.sentence))

        self.setLayout(hbox)
        self.resize(90, 20)


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
        self.process_button = None
        self.status = None
        self.list_widget = None
        self.list_model = None
        self.male_radio = None
        self.female_radio = None
        self.init_ui()

    def init_sentences(self):
        # Iterate over all odd number between 1 and 24 for type 1 sentence
        for i in range(0, 25, 1):
            self.sentences.append(Data("העבר מודול {} לשידור".format(i), "-1-{}".format(i)))

        # Iterate over all even number between 0 and 24 for type 2 sentence
        for i in range(0, 25, 1):
            self.sentences.append(Data("העבר מודול {} להאזנה".format(i), "-2-{}".format(i)))

        # Iterate over all odd number between 1 and 24 for type 3 sentence
        for i in range(0, 25, 1):
            d1, d2, d3, d4 = random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)
            self.sentences.append(Data("בצע הקצאה במודול {} לערוץ {}, {}, {}, {}".format(i, d1, d2, d3, d4),
                                       "-3-{}-{}-{}-{}-{}".format(i, d1, d2, d3, d4)))

        # Iterate the numbers 1, 2 & 3 for type 4 sentence
        for i in range(1, 4):
            self.sentences.append(Data("עבור לגיבוי {}".format(i), "-4-{}".format(i)))

        # Record 5 times the user saying all numbers between 0 and 24, shuffled each time differently
        for _ in range(5):
            nums = list(range(0, 25))
            random.shuffle(nums)
            nums = [str(num) for num in nums]
            self.sentences.append(Data("➡➡➡ {}".format(", ".join(nums)), "-5-{}".format("-".join(nums))))

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

        radio_group = QtGui.QButtonGroup()
        self.male_radio = QtGui.QRadioButton("Male")
        self.male_radio.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.female_radio = QtGui.QRadioButton("Female")
        self.female_radio.setStyleSheet("font-weight: bold; font-size: 16px;")
        radio_group.addButton(self.male_radio)
        radio_group.addButton(self.female_radio)
        self.male_radio.setChecked(True)

        explanation = QtGui.QLabel("Press on the Record button, read the text and then press it again")
        explanation.setStyleSheet("font-weight: bold; font-size: 16px;")

        self.record_text = QtGui.QLabel()
        self.record_text.setStyleSheet("font-weight: bold; font-size: 16px; padding: 20px 20px 20px 20px; color: red;")
        self.__set_sentence()

        # Button used to start and stop recordings
        self.record_button = QtGui.QPushButton("התחל להקליט")
        self.record_button.setStyleSheet(self.DEFAULT_BUTTON_STYLE + "background-color: #{};".format(Colors.START))
        self.record_button.setFixedHeight(40)
        self.record_button.clicked.connect(self.record_clicked)

        # Button to cancel recordings midway
        self.cancel_button = QtGui.QPushButton("בטל הקלטה")
        self.cancel_button.setStyleSheet(
            self.DEFAULT_BUTTON_STYLE + "background-color: #{}".format(Colors.CANCEL_DISABLED))
        self.cancel_button.setFixedHeight(40)
        self.cancel_button.setDisabled(True)
        self.cancel_button.clicked.connect(self.cancel_clicked)

        self.process_button = QtGui.QPushButton("Process with Kaldi")
        self.process_button.setStyleSheet(self.DEFAULT_BUTTON_STYLE + "background-color: #{};".format(Colors.PROCESS))
        self.process_button.setFixedHeight(40)
        self.process_button.clicked.connect(self.process_clicked)

        self.status = QtGui.QLabel("Status: {}\{}".format(self.current_index, len(self.sentences)))
        self.status.setStyleSheet("font-weight: bold; font-size: 16px;")

        grid.addWidget(name_label, 0, 0, 1, 2)
        grid.addWidget(self.name, 1, 0, 1, 2)
        grid.addWidget(self.male_radio, 2, 0, 1, 2)
        grid.addWidget(self.female_radio, 3, 0, 1, 2)
        grid.addWidget(explanation, 4, 0, 1, 2)
        grid.addWidget(self.record_text, 5, 0, 1, 2)
        grid.addWidget(self.status, 6, 0)
        grid.addWidget(self.cancel_button, 7, 0)
        grid.addWidget(self.record_button, 7, 1)
        grid.addWidget(self.process_button, 8, 0, 1, 2)

        self.move(300, 300)
        self.setWindowTitle('Cold Recorder')

    def __set_sentence(self):
        self.record_text.setText(self.sentences[self.current_index].sentence)
        if self.status is not None:
            self.status.setText("Status: {}\{}".format(self.current_index, len(self.sentences)))

    def record_clicked(self):
        if "התחל" in self.record_button.text():
            # Change button to its Stop version
            self.record_button.setText("סיים הקלטה")
            self.record_button.setStyleSheet(self.DEFAULT_BUTTON_STYLE + "background-color: #{};".format(Colors.STOP))

            # Start recordings
            self.recorder.startRecording()

            # Enable the Cancel button
            self.cancel_button.setDisabled(False)
            self.cancel_button.setStyleSheet(self.DEFAULT_BUTTON_STYLE + "background-color: #{}".format(Colors.CANCEL))
        elif "סיים" in self.record_button.text():
            # Change button to its Start version
            self.record_button.setText("התחל להקליט")
            self.record_button.setStyleSheet(self.DEFAULT_BUTTON_STYLE + "background-color: #{};".format(Colors.START))

            # Stop recording
            self.recorder.stopRecording(
                os.path.join(self.dictPath, self.name.text() + self.sentences[self.current_index].postfix + ".wav"))

            # Disable the Cancel button
            self.cancel_button.setDisabled(True)
            self.cancel_button.setStyleSheet(
                self.DEFAULT_BUTTON_STYLE + "background-color: #{}".format(Colors.CANCEL_DISABLED))

            # Generate a new text for the user to record
            self.current_index += 1
            self.__set_sentence()

    def cancel_clicked(self):
        # Change button to its Start version
        self.record_button.setText("התחל להקליט")
        self.record_button.setStyleSheet(self.DEFAULT_BUTTON_STYLE + "background-color: #{};".format(Colors.START))

        # Disable the Cancel button
        self.cancel_button.setDisabled(True)
        self.cancel_button.setStyleSheet(
            self.DEFAULT_BUTTON_STYLE + "background-color: #{}".format(Colors.CANCEL_DISABLED))

        # Stop recording without saving
        self.recorder.stopRecording("", save=False)

    def process_clicked(self):
        # TODO: Chen
        pass

    def on_item_clicked(self):
        pass


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
