import pyaudio
import wave


class Recorder:
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "file.wav"

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = []
        self.frames = []

    def startRecording(self):
        print("A")
        self.frames = []
        # start Recording
        self.stream = self.audio.open(format=self.FORMAT,
                                      channels=self.CHANNELS,
                                      rate=self.RATE,
                                      input=True,
                                      frames_per_buffer=self.CHUNK,
                                      stream_callback=self.__callback)

    def stopRecording(self):
        print("C")
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        waveFile = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(self.frames))
        waveFile.close()

    def __callback(self, in_data, frame_count, time_info, status):
        print("B")
        print(type(in_data))
        print(frame_count)
        print(time_info)
        self.frames.append(in_data)

        return None, pyaudio.paContinue
