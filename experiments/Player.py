"""
This module represents an audio player using a callback (non-blocking).

A class is handy since it can encapsulate properties of the Stream and handle
state regarding the buffer used to store audio data.

"""
# import threading
import pyaudio
import numpy as np
import time

class Player():

    def __init__(self, paFormat=pyaudio.paFloat32, fr=44100, sample_size=1024, \
                channels=1, continuous=True):
        # threading.Thread.__init__(self)
        self.p = pyaudio.PyAudio()
        self.paFormat = paFormat
        self.fr = fr
        self.sample_size = sample_size
        self.stream = self.get_stream(
            callback=self.audio_callback,
            paformat=paFormat, 
            framerate=fr, 
            num_channels=channels)
        self.wave = np.zeros(sample_size)
        self.release = False
        self.offset = 0
        self.continuous = continuous
    
    def set_wave(self, wave):
        self.wave = wave
    
    # def fill_buffer(self, wave):
    #     self.wave[]
    
    def audio_callback(self, in_data, frame_count, time_info, status):
        """
        pyaudio will continue calling this function to play from a buffer

        continuous -- By default we assume that we'll keep checking buffer indefinitely
        """
        print('ready to write audio!')
        if not self.release: return None, pyaudio.paComplete
        end = self.offset + frame_count
        data = self.wave[self.offset:end]
        self.offset += frame_count
        if self.continuous and self.offset > len(self.wave):
            self.wave = np.zeros(len(self.wave))
            self.offset = 0
            return self.wave, pyaudio.paContinue
        return data, pyaudio.paContinue

    def run(self):
        self.release = True
        self.stream.start_stream()
        while self.stream.is_active():
            time.sleep(0.01)
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def get_stream(self, callback=None, paformat=pyaudio.paFloat32, num_channels=1, \
                    framerate=44100, sample_size=1024):
        return self.p.open(format=paformat,
                        channels=num_channels,
                        rate=framerate,
                        # input=True,
                        frames_per_buffer=sample_size,
                        output=True,
                        stream_callback=callback)
    
    def stop(self):
        self.release = True
