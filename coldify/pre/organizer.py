import os
import re
import sys

from coldify.utils import numeric


def parse_for_text_file(name):
    """Converts a file name to the wanted format in the train/test text file

    For example, if the file name is

        chen432.wav

    this function will return the following string:

        chen432 four three two

    :param name: file name
    :return: representation of this file as needed by the text file
    """
    return "{} {}".format(remove_extension(name), parse_name(name))


def extract_name(name):
    """Extracts speaker name from a recording file name

    For examples, if file name is:

        dan897.wav:

    this function will extract the name "dan".

    :param name: recording file name
    :return: recording speaker name
    """
    return re.search(r"[a-zA-Z]*", name).group()


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


def parse_name(name):
    """Extracts the words from the file name

    Extracts the words from the filename according to its type. To see the format of each type and how the output will
    look like, refer to the documentation of __parse_x() functions.

    :param name: file name
    :return: string representing the words spoken in the file
    """
    if re.search(r"^[a-zA-Z0-9]+-1", name):
        return __parse_name_1(name)
    if re.search(r"^[a-zA-Z0-9]+-2", name):
        return __parse_name_2(name)
    if re.search(r"^[a-zA-Z0-9]+-3", name):
        return __parse_name_3(name)
    if re.search(r"^[a-zA-Z0-9]+-4", name):
        return __parse_name_4(name)
    if re.search(r"^[a-zA-Z0-9]+-5", name):
        return __parse_name_5(name)
    if re.search(r"^[a-zA-Z0-9]+-6", name):
        return __parse_name_6(name)


def __parse_name_1(name):
    """Parses files of type 1

    Files of type 1 have the following structure as their name:

        <name>-1-<num>

    The <name> parameter is the name of the speaker.
    The <num> parameter is the number spoken in the file.

    The output format is:

        aaver modul <num> le shidur

    :param name: file name
    :return: string representing the data in this file
    """
    parts = remove_extension(name).split("-")[2:]

    return "aaver modul {} le shidur".format(numeric.to_string_repr(parts[0]))


def __parse_name_2(name):
    """Parses files of type 2

    Files of type 2 have the following structure as their name:

        <name>-2-<num>

    The <name> parameter is the name of the speaker.
    The <num> parameter is the number spoken in the file.

    The output format is:

        aaver modul <num> le aazana

    :param name: file name
    :return: string representing the data in this file
    """
    parts = remove_extension(name).split("-")[2:]

    return "aaver modul {} le aazana".format(numeric.to_string_repr(parts[0]))


def __parse_name_3(name):
    """Parses files of type 3

    Files of type 3 have the following structure as their name:

        <name>-3-<num#1>-<num#2>-<num#3>-<num#4>-<num#5>

    The <name> parameter is the name of the speaker.
    The <num#1> parameter is the number spoken in the file.
    The <num#2> parameter is the first digit of second number.
    The <num#3> parameter is the second digit of second number
    The <num#4> parameter is the third digit of second number
    The <num#5> parameter is the fifth digit of second number

    The output format is:

        batsea aktsaa be modul <num#1> le aruts <num#2> <num#2> <num#4> <num#5>

    :param name: file name
    :return: string representing the data in this file
    """
    parts = remove_extension(name).split("-")[2:]
    module = parts[0]
    numbers = " ".join([numeric.to_string_repr(part) for part in parts[1:]])

    return "batsea aktsaa be modul {} le aruts {}".format(module, numbers)


def __parse_name_4(name):
    """Parses files of type 4

    Files of type 4 have the following structure as their name:

        <name>-4-<num>

    The <name> parameter is the name of the speaker.
    The <num> parameter is the number spoken in the file.

    The output format is:

        avor le gibui <num>

    :param name: file name
    :return: string representing the data in this file
    """
    parts = remove_extension(name).split("-")[2:]

    return "avor le gibui {}".format(numeric.to_string_repr(parts[0]))


def __parse_name_5(name):
    """Parses files of type 5

    Files of type 5 have the following structure as their name:

        <name>-4-<num#1>-<num#2>-...-<num#n>

    The <name> parameter is the name of the speaker.
    The <num#1> parameter is the first number spoken in the file.
    The <num#2> parameter is the second number spoken in the file.
    ...
    The <num#n> parameter is the n'th number spoken in the file.

    The output format is:

        <num#1> <num#2> ... <num#n>

    :param name: file name
    :return: string representing the data in this file
    """
    parts = remove_extension(name).split("-")[2:]

    return " ".join([numeric.to_string_repr(part) for part in parts])


def __parse_name_6(name):
    """Parses files of type 6

    The input and output format are exactly the same as in type 5.

    :param name: file name
    :return: string representing the data in this file
    """
    return __parse_name_5(name)


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
                    corpus.append(parse_name(recording))
                    text_lines.append(parse_for_text_file(recording))
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
