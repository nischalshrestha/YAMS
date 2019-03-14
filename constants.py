# Declaring all constants
OCTAVE = 8
CHROMATIC = 12
# 1 stands for semitone, 2 for whole tone
SCALES = {
    'major': [1, 1, 0.5, 1, 1, 1, 0.5],
    'natural_minor': [1, 0.5, 1, 1, 0.5, 1, 1],
}
# each mode value stands for the interval to start on for key
MODES = {
    'ionian': [1, 1, 0.5, 1, 1, 1, 0.5],
    'dorian': [1, 0.5, 1, 1, 1, 0.5, 1],
    'phrygian': [0.5, 1, 1, 1, 0.5, 1, 1],
    'lydian': [1, 1, 1, 0.5, 1, 1, 0.5],
    'mixolydian': [1, 1, 0.5, 1, 1, 0.5, 1],
    'aeolian': [1, 0.5, 1, 1, 0.5, 1, 1],
    'locrian': [0.5, 1, 1, 0.5, 1, 1, 1],
}
MAJOR_FORMULA = {
    'maj': [1, 3, 5],
    'maj6': [1, 3, 5, 6],
    'maj7': [1, 3, 5, 7],
    'maj9': [1, 3, 5, 7, 9],
    'majadd9': [1, 3, 5, 9],
    'maj6/9': [1, 3, 5, 6, 9],
    'maj7/6': [1, 3, 5, 6, 7],
    'maj13': [1, 3, 5, 7, 9, 13],
}
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
