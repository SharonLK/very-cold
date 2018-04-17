import re

"""
A mapping from integers to their string representation 
"""
NUM_TO_REPR = {
    0: "efes",
    1: "ahat",
    2: "shtaim",
    3: "shalosh",
    4: "arba",
    5: "hamesh",
    6: "shesh",
    7: "sheva",
    8: "shmone",
    9: "tesha",
    10: "eser",
    11: "ahat esre",
    12: "shteim esre",
    13: "shlosh esre",
    14: "arba esre",
    15: "hamesh esre",
    16: "shesh esre",
    17: "shva esre",
    18: "shmona esre",
    19: "tsha esre",
    20: "esrim",
    21: "esrim ve ahat",
    22: "esrim ve shtaim",
    23: "esrim ve shalosh",
    24: "esrim ve arba",
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
    return NUM_TO_REPR[to_number(num)]
