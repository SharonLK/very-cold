import random

if __name__ == "__main__":
    """Generates a randomly shuffled sequence from 0 to 24
    
    The sequences are split into 2 sentences, first one containing 12 numbers and the later 13 numbers.
    """
    nums = list(range(0, 25))
    random.shuffle(nums)
    print(nums[:12])
    print(nums[12:])
