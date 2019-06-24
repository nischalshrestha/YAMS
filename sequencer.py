import time
import threading
from threading import Thread
import schedular
from schedular import TimeKeeper
from constants import *
import audio
import numpy as np

# TODO play with a sequencer

# TODO play with interleaving for multiple channels
# https://stackoverflow.com/questions/22636499/convert-multi-channel-pyaudio-into-numpy-array/22644499#22644499
# https://stackoverflow.com/questions/24974032/reading-realtime-audio-data-into-numpy-array/24985016#24985016

fr = 44100
buffer = np.zeros(len(np.arange(1*fr)))
stream = audio.get_stream()
time_keeper = TimeKeeper(stream)

def metronome(note, beats):
    global buffer
    """
    Basic metronome given type of note length (quarter note etc.) the beats
    in bpm and wave type
    """
    base_dur = beats
    note_dur = note*base_dur
    print(note_dur)
    last = time_keeper.sample()
    while True:
        curr = time_keeper.sample()
        # instead of using exact time of play, calculate next time for more accuracy
        if curr >= last + note_dur:
            # since the write blocks for only the time it needs to, it will be
            # fairly accurate compared to time.sleep() which might drift
            print('beep', curr)
            if np.any(buffer):
                stream.write(buffer.tobytes())
                buffer = np.zeros(len(np.arange(1*fr)))
            last = curr

def myfunc(i):
    print("sleeping 5 sec from thread %d" % i)
    print("thread id ", threading.get_ident())
    metronome(EIGHTH, schedular.bpm(120))
    print("finished sleeping from thread %d" % i)

# for i in range(10):
audio_thread = Thread(target=myfunc, args=(0,))
audio_thread.start()

print("yello")
time.sleep(2)
buffer = audio.generate_triangle(220, duration=0.05) + audio.generate_square(110, duration=0.05, amp=0.15)
print("yello again")