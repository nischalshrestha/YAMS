
var synth = new Tone.Synth().toMaster();
var notes = [];
var octave = "3";
var count = 0;

function arpeggiate(root, scale) {
    if (isNote(root) ) {
        console.log('valid note: '+root.toUpperCase()+' in '+scale);
        notes = chromatic(root);
        playArpeggio("4n");
        console.log('notes: '+notes);
    }
}

function triggerSynth(time) {
    count = count == notes.length ? count % notes.length : count;
    // TODO fix this so that octave also updates as necessary
    synth.triggerAttackRelease(notes[count++] + octave, time);
}

function playArpeggio(interval) { 
    Tone.Transport.cancel('2');
    count = 0;
    var time = 0;
    notes.forEach(element => {
        Tone.Transport.schedule(triggerSynth, time+0.01);
        time += Tone.Time(interval);
    });
    Tone.Transport.loopEnd = '1m';
    Tone.Transport.bpm.value = 120;
    // Tone.Transport.loop = true;
    Tone.Transport.toggle();
}

document.addEventListener('keypress', e => {
    arpeggiate(e.key, 'major');
});


