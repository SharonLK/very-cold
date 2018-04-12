import os
import sys
from coldify.utils import numeric


def extract_words(name):
    """Extracts the words from the file name

    For example, if the file name is

        dan_897.wav

    this function will extract the numbers and return ["eight", "nine", "seven"].

    :param name: file name
    :return: list of the words spoken in that .wav file
    """
    nums = [numeric.to_number(char) for char in name if numeric.is_number(char)]
    return [numeric.to_string_repr(num) for num in nums]


def convert_filename(name):
    """Converts a file name to the wanted format in the train/test text file

    For example, if the file name is

        chen432.wav

    this function will return the following string:

        chen432 four three two

    :param name: file name
    :return: representation of this file as needed by the text file
    """
    prefix = name[:name.index(".")]
    return "{} {}".format(prefix, " ".join(extract_words(name)))


if __name__ == "__main__":
    source_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

    types = ["train", "test"]

    for dir_type in types:
        path = os.path.join(source_dir, "..", "..", "digits_audio", dir_type)

        lines = []

        for name_dir in os.listdir(path):
            dir_path = os.path.join(path, name_dir)
            if os.path.isdir(dir_path):
                for recording in os.listdir(dir_path):
                    lines.append(convert_filename(recording))

        lines.sort()

        with open(os.path.join(source_dir, "..", "..", "data", dir_type, "text"), "w") as f:
            for line in lines:
                f.write("{}{}".format(line, os.linesep))
