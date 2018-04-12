import re

"""
A mapping from integers to their string representation 
"""
NUM_TO_REPR = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine"
}


def is_number(string):
    """Checks whether the given string is a number

    :param string: string
    :return: True if the string is a number, False otherwise
    """
    return re.search(r"[\d]+", string) is not None


def to_number(string):
    """converts the given string to a number

    :param string: string
    :return: integer if the string represents a number, None otherwise
    """
    try:
        return int(string)
    except ValueError:
        return None


def to_string_repr(num):
    """Converts the integer to its string representation

    For example, converts the integer 0 to the string "zero"
    For example, converts the integer 2 to the string "two"

    etc...

    :param num: a number
    :return: string representation of the number
    """
    return NUM_TO_REPR[num]
