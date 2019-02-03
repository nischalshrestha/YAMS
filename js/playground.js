

var elem = document.getElementById('draw-shapes');

// BASICS
//create a synth and connect it to the master output (your speakers)
var synth = new Tone.Synth().toMaster();
//play a middle 'C' for the duration of an 8th note
synth.triggerAttackRelease(261.63, "8n");
// synth.triggerAttackRelease("C4", "8n");


// console.log(mode('C', 'ionian'));
// Note: since synth is an instrument you can't keep it playing indefinitely
// like you could with a audio Source
/*
// SCHEDULING
//schedule a series of notes, one per second
synth.triggerAttackRelease('C4', 0.5, 0)
synth.triggerAttackRelease('E4', 0.5, 1)
synth.triggerAttackRelease('G4', 0.5, 2)
synth.triggerAttackRelease('B4', 0.5, 3)

//schedule a series of notes to play as soon as the page loads
synth.triggerAttackRelease('C4', '4n', '8n')
synth.triggerAttackRelease('E4', '8n', Tone.Time('4n') + Tone.Time('8n'))
synth.triggerAttackRelease('G4', '16n', '2n')
synth.triggerAttackRelease('B4', '16n', Tone.Time('2n') + Tone.Time('8t'))
synth.triggerAttackRelease('G4', '16', Tone.Time('2n') + Tone.Time('8t')*2)
synth.triggerAttackRelease('E4', '2n', '0:3')

//this function is called right before the scheduled time
function triggerSynth(time){
	//the time is the sample-accurate time of the event
	synth.triggerAttackRelease('C2', '8n', time)
}

//schedule a few notes (this uses the bar:quarter:sixteenths encoding)
Tone.Transport.schedule(triggerSynth, 0)
//can do quote around time encoding as well
// Tone.Transport.schedule(triggerSynth, '0')
Tone.Transport.schedule(triggerSynth, '0:2')
Tone.Transport.schedule(triggerSynth, '0:2:2.5')

//set the transport to repeat
Tone.Transport.loopEnd = '1m'
// Tone.Transport.loop = true
Tone.Transport.toggle()
*/

/*
// BPM
var synth = new Tone.MetalSynth().toMaster();
function triggerSynth(time){
	synth.triggerAttackRelease('16n', time)
}

Tone.Transport.schedule(triggerSynth, 0)
Tone.Transport.schedule(triggerSynth, 2 * Tone.Time('8t'))
Tone.Transport.schedule(triggerSynth, Tone.Time('4n') + Tone.Time('8t'))
Tone.Transport.schedule(triggerSynth, Tone.Time('4n') + 2 * Tone.Time('8t'))
Tone.Transport.schedule(triggerSynth, Tone.Time('0:2') + Tone.Time('8t'))
Tone.Transport.schedule(triggerSynth, Tone.Time('0:3') + Tone.Time('8t'))

Tone.Transport.loopEnd = '1m'
Tone.Transport.loop = true
Tone.Transport.toggle()
Tone.Transport.bpm.value = 120
*/

/*
// LOOPS
var synth = new Tone.MembraneSynth().toMaster()
//create a loop
var loop = new Tone.Loop(function(time){
	synth.triggerAttackRelease("C1", "8n", time)
}, "4n")
//play the loop between 0-2m on the transport
loop.start(0).stop('2m')
Tone.Transport.toggle()
*/

/*
// PART (SCHEDULE ARRAY OF EVENTS)
var synth = new Tone.Synth().toMaster()
//pass in an array of events
var part = new Tone.Part(function(time, event){
	//the events will be given to the callback with the time they occur
	synth.triggerAttackRelease(event.note, event.dur, time)
}, [{ time : 0, note : 'C4', dur : '4n'},
	{ time : {'4n' : 1, '8n' : 1}, note : 'E4', dur : '8n'},
	{ time : '2n', note : 'G4', dur : '16n'},
	{ time : {'2n' : 1, '8t' : 1}, note : 'B4', dur : '4n'}])
//start the part at the beginning of the Transport's timeline
part.start(0)
//loop the part 3 times
part.loop = 3
part.loopEnd = '1m'
Tone.Transport.timeSignature = [6, 4]
Tone.Transport.bpm.value = 180
//start/stop the transport
Tone.Transport.toggle()
//can do phasing: https://github.com/Tonejs/Tone.js/blob/dev/examples/pianoPhase.html
*/

/*
// INSTRUMENTS
var synthA = new Tone.Synth({
	oscillator: {
		type: 'fmsquare',
		modulationType: 'sawtooth',
		modulationIndex: 3,
		harmonicity: 3.4
	},
	envelope: {
		// these could be dials
		attack: 0.001,
		decay: 0.1,
		sustain: 0.1,
		release: 0.1
	}
}).toMaster()

var synthB = new Tone.Synth({
	oscillator: {
	  type: 'triangle8'
	},
	envelope: {
	  attack: 2,
	  decay: 1,
	  sustain: 0.4,
	  release: 4
	}
}).toMaster()

synthA.triggerAttackRelease('C4', '4n')
synthB.triggerAttackRelease('C4', '4n')
*/

// EFFECTS




/*
// POLYSYNTH (CHORDS!!!)
var polySynth = new Tone.PolySynth(4, Tone.Synth).toMaster()
//an array of notes can be passed into PolySynth
// polySynth.triggerAttackRelease(['C4', 'E4', 'G4', 'B4'])
elem.addEventListener('mousedown', e => {
    polySynth.triggerAttack(['C4', 'E4', 'G4', 'B4']);
})
elem.addEventListener('mouseup', e => {
	// unlike other synths you need to still pass in array for release
    polySynth.triggerRelease(['C4', 'E4', 'G4', 'B4']);
})
*/

/*
// EFFECTS 
var distortion = new Tone.Distortion(0.6)
// note: Tremelo is actually an LFO so needs to be started
var tremolo = new Tone.Tremolo().start()
// the order of chaining doesn't seem to matter here
var polySynth = new Tone.PolySynth(4, Tone.Synth).chain(distortion, tremolo, Tone.Master)
elem.addEventListener('mousedown', e => {
	// scheduling even a bit later improves perf
	// more: https://github.com/Tonejs/Tone.js/wiki/Performance
	Tone.Transport.schedule(polySynth, 0.1)
    polySynth.triggerAttack(['C4', 'E4', 'G4', 'B4']);
})
elem.addEventListener('mouseup', e => {
	// unlike other synths you need to still pass in array for release
    polySynth.triggerRelease(['C4', 'E4', 'G4', 'B4']);
})
*/

/*
// SOURCES
// a pwm oscillator
var pwm = new Tone.PWMOscillator("Bb3").toMaster()
pwm.volume.value = -10
elem.addEventListener('mousedown', () => {
	pwm.start()
})
elem.addEventListener('mouseup', () => {
	pwm.stop()
})
*/

/*
// SIGNALS
var filter = new Tone.Filter({
	// https://developer.mozilla.org/en-US/docs/Web/API/BiquadFilterNode/type
	type: 'bandpass',
	Q: 12
}).toMaster()
//schedule a series of frequency changes
filter.frequency.setValueAtTime('C5', 0)
filter.frequency.setValueAtTime('E5', 0.5)
filter.frequency.setValueAtTime('G5', 1)
filter.frequency.setValueAtTime('B5', 1.5)
filter.frequency.setValueAtTime('C6', 2)
filter.frequency.linearRampToValueAtTime('C1', 3)
//create brown noise and connect to filter
var noise = new Tone.Noise("brown").connect(filter).start(0).stop(3)
//schedule an amplitude curve
noise.volume.setValueAtTime(-20, 0)
noise.volume.linearRampToValueAtTime(20, 2)
noise.volume.linearRampToValueAtTime(-Infinity, 3)
*/

// SHAPES 

// Make an instance of two and place it on the page.
// var elem = document.getElementById('draw-shapes');
var params = { width: 285, height: 200 };
// var two = new Two(params).appendTo(document.body);
var two = new Two(params).appendTo(elem);   
// two has convenience methods to create shapes.
var circle = two.makeCircle(72, 100, 50);
var rect = two.makeRectangle(213, 100, 100, 100);
// The object returned has many stylable properties:
circle.fill = '#FF8000';
circle.stroke = 'orangered'; // Accepts all valid css color
circle.linewidth = 5;
rect.fill = 'rgb(0, 200, 255)';
rect.opacity = 0.75;
rect.stroke = '#1C75BC';
// rect.noStroke();
// Don't forget to tell two to render everything
// to the screen
two.update();

//attach a listener to the keyboard events
// elem.addEventListener('mousedown', e => {
//     console.log('hello');
//     synth.triggerAttack(261.63);
// })

// elem.addEventListener('mouseup', e => {
//     console.log('untrigger');
//     synth.triggerRelease();
// })

// var synth = new Tone.FMSynth().toMaster()
