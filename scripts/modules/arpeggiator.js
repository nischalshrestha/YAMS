
var synth = new Tone.Synth().toMaster();
var notes = [];
var count = 0;

function arpeggiate(root, scale) {
    if (isNote(root) ) {
        // console.log('valid note: '+root.toUpperCase()+' in '+scale);
        notes = chromatic(root, 2);
        playArpeggio("4n");
        console.log(root.toUpperCase()+' '+scale+' frequencies: '+notes);
    }
}

function triggerSynth(time) {
    count = count == notes.length ? count % CHROMATIC : count;
    synth.triggerAttackRelease(notes[count++], time);
}

function playArpeggio(interval) { 
    Tone.Transport.cancel();
    count = 0;
    var time = 0;
    notes.forEach(element => {
        Tone.Transport.schedule(triggerSynth, time);
        time += Tone.Time(interval);
    });
    Tone.Transport.loopEnd = '4n';
    Tone.Transport.bpm.value = 120;
    Tone.Transport.loop = true;
    Tone.Transport.start();
}

document.addEventListener('keypress', e => {
    arpeggiate(e.key, 'major');
});


