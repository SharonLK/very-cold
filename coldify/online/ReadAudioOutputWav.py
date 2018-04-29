import struct
import wave

import numpy as np
import pyaudio

from coldify.online import checks


def get_rms(block):
    # RMS amplitude is defined as the square root of the
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into
    # a string of 16-bit samples...

    # we will get one short out for each
    # two chars in the string.
    count = len(block) / 2
    format = "%dh" % count
    shorts = struct.unpack(format, block)

    return shorts


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
WAVE_OUTPUT_FILENAME = "output"


def start(callback):
    start_flag = 0
    end_flag = 0
    suffix = ".wav"
    file_number = 1
    SHORT_NORMALIZE = (1.0 / 32768.0)

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    i = 0

    counter = np.zeros(10000)

    while True:
        data_1 = stream.read(CHUNK)
        data = get_rms(data_1)
        data = np.asarray(list(data))
        print(data)
        if end_flag == 0:

            if start_flag == 0:
                # plt.plot(np.arange(i * CHUNK, (i + 1) * CHUNK), data, 'blue')
                start_flag = checks.checkSpeechStart(data, i)

            if start_flag == 1:
                # plt.plot(np.arange(i * CHUNK, (i + 1) * CHUNK), data, 'red')
                end_flag = checks.checkSpeechEnd(data, i, counter)

        if start_flag == 1:
            frames.append(data_1)
        if end_flag == 1:
            wf = wave.open(WAVE_OUTPUT_FILENAME + str(file_number) + suffix, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

            callback(WAVE_OUTPUT_FILENAME + str(file_number) + suffix)

            frames = []
            file_number += 1
            start_flag = 0
            end_flag = 0
            i = 0

        i += 1

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()
