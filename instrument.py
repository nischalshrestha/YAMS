#!/usr/bin/env python3

# ^ this is required for capturing key events
# you need to also give script executable right and run with sudo

# TODO envelope filter - ADSR (attack, decay, sustain, release)
# TODO Polypony -- playing multiple notes at once

# playing with keyboard events; for now it makes it easy to debug sounds
import numpy as np
import scipy as sc
from pynput import keyboard
from audio import get_stream, triangle, clean_up
from constants import *
from play import Play
import threading

class Instrument(keyboard.Listener):

    def __init__(self):
        keyboard.Listener.__init__(self, on_press=self.on_press, on_release=self.on_release)
        self.current = ''
        self.p = None

    def on_press(self, key):    
        try:
            print('alphanumeric key {0} pressed'.format(key.char))
            possible_note = (key.char.upper()+'0')
            if key.char == 'q':
                clean_up()
                sys.exit(0)
            elif possible_note in TABLE and possible_note[:-1] != self.current:
                note = key.char.upper()+'3'
                self.current = key.char.upper()
                w = triangle(TABLE[note], duration=1.0, taper=False)
                self.p = Play(w)
                self.p.start()
        except AttributeError:
            pass
    
    def on_release(self, key):
        self.p.stop()
        self.current = ''
        print('Key {} released.'.format(key))
 
listener = Instrument()
listener.start()
listener.join()

# with keyboard.Listener(
#     on_press = on_press,
#     on_release = on_release) as listener:
#     listener.join()
