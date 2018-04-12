from coldify.utils import numeric


def extract_words(name):
    """Extracts the words from the file name

    For example, if the file name is

        dan_897.wav

    this function will extract the numbers and return list("eight", "nine", "seven").

    :param name: file name
    :return: list of the words spoken in that .wav file
    """
    nums = [numeric.to_number(char) for char in name if numeric.is_number(char)]
    return [numeric.to_string_repr(num) for num in nums]


if __name__ == "__main__":
    print(extract_words("chen178.wav"))
