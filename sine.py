import pyaudio
import numpy as np
import time

# TODO add encapsulation with use of classes once different wave shapes
# can be generated

p = pyaudio.PyAudio()
fr = 44100

def generate_wave(freq=440, duration=1.0, start=0, offset=0, amp=1.0):
    # makes sure that amp is within range [0.0, 1.0]
    amp = max(0, min(1.0, amp))
    # framerate is the # samples per second so we divide each second by fr
    ts = start + np.arange(fr * duration) / fr
    # This is the evaluation of the wave given the ts
    phases = 2 * np.pi * freq * ts  + offset
    # generate samples, note conversion to float32 array
    # the tobytes() is required due to pyaudio conversion of numpy
    # https://stackoverflow.com/a/48454913/9193847
    ys = amp * np.sin(phases).astype(np.float32)
    return ys

sine_wave = generate_wave(freq=440, amp=0.9)

def callback(in_data, frame_count, time_info, status):
    end = callback.start_offset + frame_count
    data = sine_wave[callback.start_offset:end]
    callback.start_offset += frame_count
    # let pyaudio continue calling this function until there's no more data
    # to be read from wave
    return data, pyaudio.paContinue

callback.start_offset = 0

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fr,
                output=True,
                stream_callback=callback)

# blocking version uses this and removes the stream_callback parameter in open()
# stream.write(sine_wave)

# non-blocking
# start the stream
stream.start_stream()
# wait for stream to finish because the audio playing is non-blocking
while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()

p.terminate()