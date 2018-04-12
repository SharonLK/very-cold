import itertools
import shutil
import argparse
import os
import random

# Name of the data directory containing all audio files
DATA_DIR_NAME = "data"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k",
                        default=10,
                        type=int,
                        help="folds amount")
    args = parser.parse_args()

    # Retrieve the audio directories (found directly under the data directory)
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(curr_dir, os.pardir, os.pardir, os.pardir, os.pardir, DATA_DIR_NAME)
    names = [name for name in os.listdir(data_dir)]

    # Shuffle and divide the audio directories into K groups
    random.shuffle(names)
    dirs_len = len(names)
    groups = [names[int(dirs_len / args.k * i):int(dirs_len / args.k * (i + 1))] for i in range(0, args.k)]

    # Iterate over all folds, each time assigning a different group as the test data
    for i in range(0, args.k):
        # Declare the directories that will act as test data and those that will act as train data
        test_data_dirs = groups[i]
        train_data_dirs = list(itertools.chain.from_iterable(groups[:i] + groups[i + 1:]))

        # Remove current test data
        test_dir = os.path.join(curr_dir, os.pardir, os.pardir, "digits_audio", "test")
        shutil.rmtree(test_dir)
        os.makedirs(test_dir)

        # Remove current train data
        train_dir = os.path.join(curr_dir, os.pardir, os.pardir, "digits_audio", "train")
        shutil.rmtree(train_dir)
        os.makedirs(train_dir)

        # Copy new test data to its position
        for name in test_data_dirs:
            shutil.copytree(os.path.join(data_dir, name), os.path.join(test_dir, name))

        # Copy new train data to its position
        for name in train_data_dirs:
            shutil.copytree(os.path.join(data_dir, name), os.path.join(train_dir, name))
