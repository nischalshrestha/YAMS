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
    # TODO refactor the rest to be 2 for W and 1 for h
    'dorian': [1, 0.5, 1, 1, 1, 0.5, 1],
    'phrygian': [0.5, 1, 1, 1, 0.5, 1, 1],
    'lydian': [1, 1, 1, 0.5, 1, 1, 0.5],
    'mixolydian': [1, 1, 0.5, 1, 1, 0.5, 1],
    'aeolian': [1, 0.5, 1, 1, 0.5, 1, 1],
    'locrian': [0.5, 1, 1, 0.5, 1, 1, 1],
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

# TODO update these for number of half tone steps like MAJOR_FORMULA
# This is the basic formula but the 3rd and 7th will receive flat accidental
# by the minor method below
MINOR_FORMULA = {
    'min': [1, 3, 5],
    'min6': [1, 3, 5, 6],
    'min7': [1, 3, 5, 7],
    'min9': [1, 3, 5, 7, 9],
    'min11': [1, 3, 5, 7, 9, 11],
    'min7/11': [1, 3, 5, 7, 11],
    'minadd9': [1, 3, 5, 9],
    'min6/9': [1, 3, 5, 6, 9],
    'minmaj7': [1, 3, 5, 7],
    'minmaj9': [1, 3, 5, 7, 9],
}

# TODO update these for number of half tone steps like MAJOR_FORMULA
# Dominants which will receive accidentals by the dominant method below
DOMINANT_FORMULA = {
    '7': [1, 3, 5, 7],
    '7/6': [1, 3, 5, 7, 6],
    '7/11': [1, 3, 5, 7, 11],
    '7sus4': [1, 4, 5, 7],
    '7/6sus4': [1, 4, 5, 7, 6],
    '9': [1, 3, 5, 7, 9],
    '11': [1, 3, 5, 7, 9, 11],
    '13': [1, 3, 5, 7, 9, 13],
    '7/6/11': [1, 3, 5, 7, 11, 13],
    '11/13': [1, 3, 5, 7, 9, 11, 13],
    'dim': [1, 3, 5, 6], 
    '+': [1, 3, 5],
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
