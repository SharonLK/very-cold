import os
import re
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


def extract_name(name):
    """Extracts speaker name from a recording file name

    For examples, if file name is:

        dan897.wav:

    this function will extract the name "dan".

    :param name: recording file name
    :return: recording speaker name
    """
    return re.search(r"[a-zA-Z]*", name).group()


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


def remove_extension(name):
    """Removes an extension from a file name

    :param name: file name
    :return: file name without the extension
    """
    return name[:name.index(".")]


def gender_mapping():
    """Returns a mapping from name to gender

    The genders are fetched from the "genders" file that should be put in the data directory.

    A male gender is represented as "m" while a female as "f".

    :return: map from name to gender
    """
    mapping = {}

    curr_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(curr_dir, os.pardir, os.pardir, os.pardir, os.pardir, "data")

    with open(os.path.join(data_dir, "genders"), "r") as f:
        for line in f.readlines():
            name, gender = line.split(" ")
            mapping[name.strip()] = gender.strip()

    return mapping


if __name__ == "__main__":
    source_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

    types = ["train", "test"]

    corpus = []

    genders = gender_mapping()

    for dir_type in types:
        path = os.path.join(source_dir, "..", "..", "digits_audio", dir_type)

        text_lines = []
        utt2spk_lines = []
        wavscp_lines = []
        genders_lines = []

        for name_dir in os.listdir(path):
            genders_lines.append("{} {}".format(name_dir, genders[name_dir]))
            dir_path = os.path.join(path, name_dir)
            if os.path.isdir(dir_path):
                for recording in os.listdir(dir_path):
                    name = extract_name(recording)
                    utt2spk_lines.append("{} {}".format(remove_extension(recording), name))
                    corpus.append(" ".join(extract_words(recording)))
                    text_lines.append(convert_filename(recording))
                    wavscp_lines.append("{} {}".format(remove_extension(recording),
                                                       os.path.normpath(os.path.join(dir_path, recording))))

        text_lines.sort()
        utt2spk_lines.sort()
        wavscp_lines.sort()
        genders_lines.sort()

        with open(os.path.join(source_dir, "..", "..", "data", dir_type, "utt2spk"), "w") as f:
            for line in utt2spk_lines:
                f.write("{}{}".format(line, os.linesep))

        with open(os.path.join(source_dir, "..", "..", "data", dir_type, "wav.scp"), "w") as f:
            for line in wavscp_lines:
                f.write("{}{}".format(line, os.linesep))

        with open(os.path.join(source_dir, "..", "..", "data", dir_type, "text"), "w") as f:
            for line in text_lines:
                f.write("{}{}".format(line, os.linesep))

        with open(os.path.join(source_dir, "..", "..", "data", dir_type, "spk2gender"), "w") as f:
            for line in genders_lines:
                f.write("{}{}".format(line, os.linesep))

    corpus.sort()
    with open(os.path.join(source_dir, "..", "..", "data", "local", "corpus.txt"), "w") as f:
        for line in corpus:
            f.write("{}{}".format(line, os.linesep))
