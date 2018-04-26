import os
import random
import shutil
import subprocess
import tkinter as tk
import logging
from collections import namedtuple
from tkinter import Tk, Label, Entry, Button

from coldify.generation.recorder import Recorder

Data = namedtuple("Data", ["sentence", "postfix"])

DEFAULT_BUTTON_STYLE = "border-radius: 2px;" + \
                       "font-weight: bold;" + \
                       "font-size: 14px;" + \
                       "border-color: black;" + \
                       "border-width: 1px;" + \
                       "border-style: outset;"


class Colors:
    START = "#98B475"  # Green
    STOP = "#F9C991"  # Orange
    CANCEL = "#AB4441"  # Red
    CANCEL_DISABLED = "#585548"  # Gray
    PROCESS = "#79B0C0"  # Blue


class Window:
    def __init__(self, master):
        self.master = master
        master.title("Coldifier")

        self.recorder = Recorder()
        self.dictPath = os.path.dirname(os.path.realpath(__file__))

        self.current_index = 0
        self.sentences = []
        self.init_sentences()

        # Initialize elements
        name_label = Label(master,
                           text="Name (in English)",
                           font="Arial 16 bold")
        self.name = Entry(master,
                          font="Arial 16")
        explanation = Label(master,
                            text="Press on the Record button, read the text out loud and then press it again",
                            font="Arial 16 bold")
        self.record_text = Label(master,
                                 text="Test",
                                 fg="red",
                                 font="Arial 16 bold")
        self.status = Label(master,
                            text="Status: {}\{}".format(self.current_index, len(self.sentences)),
                            font="Arial 16 bold")
        self.record_button = Button(master,
                                    text="התחל להקליט",
                                    command=self.record_clicked,
                                    font="Arial 12 bold",
                                    height=2,
                                    bg=Colors.START)
        self.cancel_button = Button(master, text="בטל הקלטה",
                                    command=self.cancel_clicked,
                                    font="Arial 12 bold",
                                    height=2,
                                    state=tk.DISABLED,
                                    bg=Colors.CANCEL_DISABLED)
        self.process_button = Button(master,
                                     command=self.process_clicked,
                                     text="Process with Kaldi",
                                     font="Arial 12 bold",
                                     height=2,
                                     bg=Colors.PROCESS)

        # Set the current sentence the speaker should say out loud
        self.__set_sentence()

        # Place elements inside the grid
        name_label.grid(row=0, column=0, rowspan=1, columnspan=2, padx=10, pady=5, sticky=tk.W)
        self.name.grid(row=1, column=0, rowspan=1, columnspan=2, padx=10, pady=5, sticky=tk.W)
        explanation.grid(row=2, column=0, rowspan=1, columnspan=2, padx=10, pady=5, sticky=tk.W)
        self.record_text.grid(row=3, column=0, rowspan=1, columnspan=2, padx=30, pady=5, sticky=tk.E)
        self.status.grid(row=4, column=0, rowspan=1, columnspan=2, padx=10, pady=5, sticky=tk.W)
        self.cancel_button.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W + tk.N + tk.E + tk.S)
        self.record_button.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W + tk.N + tk.E + tk.S)
        self.process_button.grid(row=6, column=0, rowspan=1, columnspan=2, padx=10, pady=5,
                                 sticky=tk.W + tk.N + tk.E + tk.S)

    def __set_sentence(self):
        self.record_text["text"] = self.sentences[self.current_index].sentence
        if self.status is not None:
            self.status["text"] = "Status: {}\{}".format(self.current_index, len(self.sentences))

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

    def record_clicked(self):
        if "התחל" in self.record_button["text"]:
            # Change button to its Stop version
            self.record_button["text"] = "סיים הקלטה"
            self.record_button["bg"] = Colors.STOP

            # Start recordings
            self.recorder.startRecording()

            # Enable the Cancel button
            self.cancel_button["state"] = tk.NORMAL
            self.cancel_button["bg"] = Colors.CANCEL
        elif "סיים" in self.record_button["text"]:
            # Change button to its Start version
            self.record_button["text"] = "התחל להקליט"
            self.record_button["bg"] = Colors.START

            # Stop recording
            if not os.path.isdir(os.path.join(self.dictPath, "recordings")):
                os.makedirs(os.path.join(self.dictPath, "recordings"))
            self.recorder.stopRecording(
                os.path.join(self.dictPath, "recordings",
                             self.name.get() + self.sentences[self.current_index].postfix + ".wav"))

            # Disable the Cancel button
            self.cancel_button["state"] = tk.DISABLED
            self.cancel_button["bg"] = Colors.CANCEL_DISABLED

            # Generate a new text for the user to record
            self.current_index += 1
            self.__set_sentence()

    def cancel_clicked(self):
        # Change button to its Start version
        self.record_button["text"] = "התחל להקליט"
        self.record_button["bg"] = Colors.START

        # Disable the Cancel button
        self.cancel_button["state"] = tk.DISABLED
        self.cancel_button["bg"] = Colors.CANCEL_DISABLED

        # Stop recording without saving
        self.recorder.stopRecording("", save=False)

    def process_clicked(self):
        # Clear the training folder
        train_dir = os.path.join(self.dictPath, os.path.pardir, os.path.pardir, os.path.pardir, "digits_audio", "train")
        shutil.rmtree(train_dir)
        os.makedirs(os.path.join(train_dir, self.name.get()))
        print(os.path.join(train_dir, self.name.get()))

        self.process_button["state"] = tk.DISABLED

        logging.info("Copying recordings to the training folder")
        # Move all recordings to the train folder
        for recording in os.listdir(os.path.join(self.dictPath, "recordings")):
            shutil.copy(os.path.join(self.dictPath, "recordings", recording),
                        os.path.join(self.dictPath, os.path.pardir, os.path.pardir, os.path.pardir, "digits_audio",
                                     "train", self.name.get(), recording))

        logging.info("Organizing data")
        subprocess.call(["python {}".format(os.path.join(self.dictPath, os.path.pardir, os.path.pardir, "pre", "organizer.py"))],
                        shell=True, start_new_session=True)
        logging.info("Finished organizing data")

        logging.info("Executing Kaldi")
        subprocess.call(["echo {} | sudo -S ./train.sh".format("q1w2e3r4")], shell=True, start_new_session=True)
        logging.info("Finished Kaldi")

        self.process_button["state"] = tk.NORMAL


def main():
    root = Tk()
    gui = Window(root)
    root.mainloop()


if __name__ == '__main__':
    main()
