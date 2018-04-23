from random import shuffle


def generate():
    """Generates and print the numbers between 0 and 24 shuffled

    The numbers printed are divided into two lines.
    """
    l = list(range(0, 25))
    shuffle(l)

    print(l[:12])
    print(l[12:])


if __name__ == "__main__":
    for _ in range(10):
        generate()
        print()
