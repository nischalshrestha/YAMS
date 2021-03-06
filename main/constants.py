"""
This contains all things related to music as constants (maybe more in future)
"""
import random as rand
import time

# Declaring all constants
OCTAVE = 8
CHROMATIC = 12
# each value is # halfsteps
SCALES = {
    'major': [0, 2, 4, 5, 7, 9, 11, 12],
    'minor': [0, 2, 3, 5, 7, 9, 10, 12],
    'natural_minor': [0, 2, 3, 5, 7, 8, 10, 12],
    'harmonic_minor': [0, 2, 3, 5, 7, 8, 11, 12]
}
# each value is # halfsteps
MODES = {
    'ionian': [0, 2, 4, 5, 7, 9, 11, 12],
    'dorian': [0, 2, 3, 5, 7, 9, 10, 12],
    'phrygian': [0, 1, 3, 5, 7, 8, 10, 12],
    'lydian': [0, 2, 4, 6, 7, 9, 11, 12],
    'mixolydian': [0, 2, 4, 5, 7, 9, 10, 12],
    'aeolian': [0, 2, 3, 5, 7, 8, 11, 12],
    'locrian': [0, 1, 3, 5, 6, 8, 10, 12],
}

ESOTERIC = {
    'super_locrian': [0, 1, 3, 4, 6, 8, 10],
    'arabic': [0, 1, 4, 5, 7, 8, 11],
    'hungarian_minor': [0, 2, 3, 6, 7, 8, 11],
    'minor_gypsy': [0, 1, 4, 5, 7, 8, 10],
    'hirojoshi': [0, 2, 3, 7, 8],
    'in_sen': [0, 1, 5, 7, 10],
    'iwato': [0, 1, 5, 6, 10],
    'kumoi': [0, 2, 3, 7, 9],
    'pelog': [0, 1, 3, 4, 7, 8],
    'spanish': [0, 1, 3, 4, 5, 6, 8, 10],
    'tritone': [0, 1, 4, 6, 7, 10],
    'enigmatic': [0, 1, 4, 6, 8, 10, 11]
}

# these are based on how many half tones needed for 3rd 5th etc.
# trick: 1, 3, 5 => 1-1 (0 meaning no interval), 3-1 (first 2 of ionian), 5-1 (first 4 of ionian) 
MAJOR_FORMULA = {
    'maj': [0, 4, 7],
    'maj6': [0, 4, 7, 9],
    'maj7': [0, 4, 7, 11],
    'maj9': [0, 4, 7, 11, 14],
    'majadd9': [0, 4, 7, 14],
    'maj6/9': [0, 4, 7, 9, 14],
    'maj7/6': [0, 4, 7, 9, 11],
    'maj13': [0, 4, 7, 11, 14, 21],
}

MINOR_FORMULA = {
    'min': [0, 3, 7],
    'min6': [0, 3, 7, 9],
    'min7': [0, 3, 7, 10],
    'min9': [0, 3, 7, 10, 14],
    'min11': [0, 3, 7, 10, 14, 17],
    'min7/11': [0, 3, 7, 10, 17],
    'minadd9': [0, 3, 7, 14],
    'min9/9': [0, 3, 7, 9, 14],
    'minmaj7': [0, 3, 7, 11],
    'minmaj9': [0, 2, 3, 7, 11],
}

DOMINANT_FORMULA = {
    '7': [0, 4, 7, 10],
    '7/6': [0, 4, 7, 10, 9],
    '7/11': [0, 4, 7, 10, 17],
    '7sus4': [0, 5, 7, 10],
    '7/6sus4': [0, 5, 7, 10, 9], # love this chord!
    '9': [0, 4, 7, 10, 14],
    '11': [0, 4, 5, 7, 10],
    '13': [0, 4, 7, 10, 21],
    '7/6/11': [0, 4, 10, 9, 17],
    '11/13': [0, 4, 5, 7, 9, 10],
    'dim': [0, 3, 6], 
    'dim7': [0, 3, 6, 9],
    '+': [0, 4, 8],
    '+7': [0, 4, 8, 10],
}

SHARPS = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#']
FLATS = ['F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb']
SHARP_NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
FLAT_NOTES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
# these will be used to convert between the representations based
# on whether scale or chord adds accidentals (for e.g. min will use flat)
EQUIVALENTS = {
    # # to b
    'C#': 'Db', 
    'D#': 'Eb', 
    'F#': 'Gb', 
    'G#': 'Ab', 
    'A#': 'Bb',
    # b to #
    # 'Db': 'C#',
    # 'Eb': 'D#',
    # 'Gb': 'F#', 
    # 'Ab': 'G#',
    # 'Bb': 'A#',
}

# Note relative lengths and time constants
SIXTY_FOURTH = 0.0625
THIRTY_SECOND = 0.125
SIXTEENTH = 0.25
EIGHTH = 0.5
QUARTER = 1
HALF = 2
WHOLE = 4
MINUTE = 60.0

def key_note_list(key, scale):
    """Gives back a note list for a given key and scale"""
    # get the scale and cutoff the octave (12) interval
    major_columns = [MODES[scale][i] for i in range(8)][:-1]
    # get the notelist for the particular key
    key_idx = SHARP_NOTES.index(key)
    note_list = np.array(SHARP_NOTES[key_idx:] + SHARP_NOTES[:key_idx])
    return note_list[major_columns]

# Frequency table stuff
BASE = 440
A = 2**(1/12)

def construct_note_list():
    """Gives back a notelist for all octaves (for e.g. C0-C8)"""
    note_list = []
    for i in range(9):
        # for semi tones like C # or Db we'll go with the sharp representation
        # tone can play either format
        for n in SHARP_NOTES:
            note_list.append(n+str(i))
    return note_list
NOTELIST = construct_note_list()

def halfsteps_from_to(notelist, a, b):
    """Returns distance in number of half steps from note a to b"""
    a_idx = notelist.index(a)
    b_idx = notelist.index(b)
    return (b_idx - a_idx)

def init_frequency_table():
    """Initializes a frequency table for all notes for 8 octaves"""
    frequency_table = {}
    f_0 = BASE; # we'll chose A4 as f0
    for i in range(len(NOTELIST)):
        f = f_0 * A ** halfsteps_from_to(NOTELIST, "A4", NOTELIST[i])
        frequency_table[NOTELIST[i]] = round(f, 2)
    return frequency_table
TABLE = init_frequency_table()

def major(root, formula):
    return MAJOR_FORMULA[formula]

def minor(root, formula):
    return MINOR_FORMULA[formula]

def dominant(root, formula):
    return DOMINANT_FORMULA[formula]

def get_note_list(root, halfsteps):
    """
    Given the root and the halfsteps, returns a list of strings representing
    notes of some sequence such as chords or scales. 

    Parameters
    ----------
    root : a string
        in the letter and octave form (C#)
    halfsteps : a list of ints
        represents the halfsteps in the sequence
    """
    note_list = []
    start_idx = SHARP_NOTES.index(root)
    note_list.append(SHARP_NOTES[start_idx])
    for h in halfsteps[1:]:
        target_idx = (start_idx + h) 
        note_list.append(SHARP_NOTES[target_idx % len(SHARP_NOTES)])
    return note_list

def get_random_chord(key):
    """
    Returns a random chord as a list of notes, given a key.
    
    Parameters
    ----------
    key : a string
        in the letter and octave form (e.g. C#2)
    """
    possible_families = ['maj', 'min', 'dom']
    family = rand.choices(possible_families, [0.33, 0.33, 0.33], k = 1)[0]
    if family == 'maj':
        formulas = list(MAJOR_FORMULA.keys())
        formula = formulas[rand.randint(0, len(formulas) - 1)]
        chord = major(key, formula)
    elif family == 'min':
        formulas = list(MINOR_FORMULA.keys())
        formula = formulas[rand.randint(0, len(formulas) - 1)]
        chord = minor(key, formula)
    elif family == 'dom':
        formulas = list(DOMINANT_FORMULA.keys())
        formula = formulas[rand.randint(0, len(formulas) - 1)]
        chord = dominant(key, formula)
    return get_note_list(key, chord)
