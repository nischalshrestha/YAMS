
// Declaring all constants
const OCTAVE = 8;
const CHROMATIC = 12;
// 1 stands for whole step, 0.5 for half 
const SCALES = {
    'major': [1, 1, 0.5, 1, 1, 1, 0.5],
    'natural_minor': [1, 0.5, 1, 1, 0.5, 1, 1],
}
// note how dorian onwards, the mode is just n left rotates on ionian
const MODES = {
    'ionian': [1, 1, 0.5, 1, 1, 1, 0.5],
    'dorian': [1, 0.5, 1, 1, 1, 0.5, 1],
    'phrygian': [0.5, 1, 1, 1, 0.5, 1, 1],
    'lydian': [1, 1, 1, 0.5, 1, 1, 0.5],
    'mixolydian': [1, 1, 0.5, 1, 1, 0.5, 1],
    'aeolian': [1, 0.5, 1, 1, 0.5, 1, 1],
    'locrian': [0.5, 1, 1, 0.5, 1, 1, 1],
}
// Note: 
// Chord formula differs from the whole/half step interval shown above 
// for scales/modes.
// TODO ported from Python version, change to suit tonejs 
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
// TODO ported from Python version, change to suit tonejs 
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
// TODO ported from Python version, change to suit tonejs 
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
const NOTES = SHARPS.concat(FLATS)
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
/**
 * Returns number of half-steps from note a to note b
 * A negative number is returned if note b has lower pitch than a
 * @param {Array} noteList 
 * @param {String} a 
 * @param {String} b 
 */
var halfStepsFromTo = function(noteList, a, b) {
    var aIdx = noteList.indexOf(a);
    var bIdx = noteList.indexOf(b);
    // console.log(a+": "+aIdx+" "+b+": "+bIdx+" dist: "+(bIdx - aIdx));
    return (bIdx - aIdx);
}

var keySet; // used to find index of the note + octave representation
var frequencyTable; // holds the frequency table for equal-tempered scale
/**
 * Initializes the frequencyTable for future reference
 */
var initFrequencyTable = function () {
    frequencyTable = new Object();
    var noteList = [];
    for (var i = 0; i <= 8; i++) {
        // for semi tones like C# or Db we'll go with the sharp representation
        // tone can play either format
        for (var n in SHARP_NOTES) {
            noteList.push(SHARP_NOTES[n]+i);
        }
    }
    keySet = [];
    frequencyTable = [];
    const f_0 = 440; // we'll chose A4 as f0
    const a = Math.pow(2, 1/12); // 12th root of 2
    for (var i = 0; i < noteList.length; i++) {
        // formula for equal tempered scale
        let f = f_0 * Math.pow(a, halfStepsFromTo(noteList, "A4", noteList[i]));
        keySet.push(noteList[i]);
        frequencyTable.push(f);
    }
}
initFrequencyTable();
// console.log(frequencyTable);

var isNote = function (name) {
    return NOTES.includes(name.toUpperCase());
}

var isMode = function (name) {
    return MODES[name.toUpperCase()] != undefined;
}

var mode = function (root, name) {
    if (isNote(root) == false) return "not a valid root note!"
    if (isMode(name) == false) return "not a valid mode!"
}

var getChromaticFrequenciesFrom = function(root, octave) {
    let rootIdx = keySet.indexOf(root+octave);
    let notes = []
    for (var i = rootIdx; i < rootIdx+CHROMATIC; i++) {
        notes.push(frequencyTable[i]);
    }
    return notes;
}

var chromatic = function(root, octave) {
    let oct = octave || 4;
    // Returns the chromatic notes given the root note
    root = root.toUpperCase();
    if (SHARP_NOTES.includes(root) == false) return []
    let notes = getChromaticFrequenciesFrom(root, oct);
    return notes
}
