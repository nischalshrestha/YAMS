# Declaring all constants
OCTAVE = 8
CHROMATIC = 12
# 1 stands for semitone, 2 for whole tone
SCALES = {
    'major': [2, 2, 1, 2, 2, 2, 1],
    'minor': [2, 1, 2, 2, 2, 1, 2],
    'natural_minor': [2, 1, 2, 2, 1, 2, 2],
}
# each mode value stands for the interval to start on for key
MODES = {
    'ionian': [2, 2, 1, 2, 2, 2, 1],
    'dorian': [2, 1, 2, 2, 2, 1, 2],
    'phrygian': [1, 2, 2, 2, 1, 2, 2],
    'lydian': [2, 2, 2, 1, 2, 2, 1],
    'mixolydian': [2, 2, 1, 2, 2, 1, 2],
    'aeolian': [2, 1, 2, 2, 1, 2, 2],
    'locrian': [1, 2, 2, 1, 2, 2, 2],
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
BASE = 440
A = 2**(1/12)
