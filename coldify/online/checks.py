from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt


start_thresh = 10000
end_thresh = 4000
counter_ones_sequence = 8


def checkSpeechStart(data, i):
    ind = np.argmax(data > start_thresh)
    if (ind > 0):
        #plt.plot(np.arange(ind + i * 1024, (i + 1) * 1024), data[ind:], 'red')
        return 1
    return 0


def checkSpeechEnd(data, i, counter):
    bool = (data > end_thresh)
    new = bool.astype(int)
    new_list = new.tolist()
    ones_count = new_list.count(1)
    sum = 0
    if ones_count == 0:
        counter[i] = 1
    if (i > counter_ones_sequence - 1):
        for j in range(0,counter_ones_sequence):
            if counter[i-j] == 1:
                sum += 1
        if counter_ones_sequence == sum:
            return 1
    return 0


if __name__ == "__main__":

    fs, data = wavfile.read('C:/Users/user/Documents/Python Scripts/Kaldi_Online/output1.wav')

    #one_ch_data = data[:, 0]

    one_ch_data = data

    start_flag = 0

    end_flag = 0

    counter = np.zeros((int(np.floor(len(one_ch_data) / 1024))))

    for i in range(0, int(np.floor(len(one_ch_data) / 1024))):

        this_data = one_ch_data[i * 1024:(i + 1) * 1024]

        if end_flag == 0:

            if start_flag == 0:
                plt.plot(np.arange(i * 1024, (i + 1) * 1024), this_data, 'blue')
                start_flag = checkSpeechStart(this_data, i)

            if start_flag == 1:
                plt.plot(np.arange(i * 1024, (i + 1) * 1024), this_data, 'red')
                end_flag = checkSpeechEnd(this_data, i, counter)

        if end_flag == 1:
            plt.plot(np.arange(i * 1024, (i + 1) * 1024), this_data, 'blue')

    print(counter)
    plt.show()
