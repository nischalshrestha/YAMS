// Declaring all constants
const OCTAVE = 8;
const CHROMATIC = 12;

// 1 stands for semitone, 2 for whole tone
const SCALES = {
    'major': [2, 2, 1, 2, 2, 2, 1],
    'natural_minor': [2, 1, 2, 2, 1, 2, 2],
}
// each mode value stands for the interval to start on for key
const MODES = {
    'ionian': 1,
    'dorian': 2,
    'phrygian': 3,
    'lydian': 4,
    'mixolydian': 5,
    'aeolian': 6,
    'locrian': 7,
}
const MAJOR_FORMULA = {
    'maj': [1, 3, 5],
    'maj6': [1, 3, 5, 6],
    'maj7': [1, 3, 5, 7],
    'maj9': [1, 3, 5, 7, 9],
    'majadd9': [1, 3, 5, 9],
    'maj6/9': [1, 3, 5, 6, 9],
    'maj7/6': [1, 3, 5, 6, 7],
    'maj13': [1, 3, 5, 7, 9, 13],
}
// This is the basic formula but the 3rd and 7th will receive flat accidental
// by the minor method below
const MINOR_FORMULA = {
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
// Dominants which will receive accidentals by the dominant method below
const DOMINANT_FORMULA = {
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
const SHARPS = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#']
const FLATS = ['F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb']
const SHARP_NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
const FLAT_NOTES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
// these will be used to convert between the representations based
// on whether scale or chord adds accidentals (for e.g. min will use flat)
const EQUIVALENTS = {
    // to b
    'C#': 'Db', 
    'D#': 'Eb', 
    'F#': 'Gb', 
    'G#': 'Ab', 
    'A#': 'Bb',
    // b to #
    // 'Db': 'C#',
    // 'Eb': 'D#',
    // 'Gb': 'F#', 
    // 'Ab': 'G#',
    // 'Bb': 'A#',
}