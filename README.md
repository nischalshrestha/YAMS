# YAMS (Yet Another Modular Synthesizer)

A **WORK IN PROGRESS** Modular Synthesis in Python using pyaudio. I draw inspiration from different audio programming systems/tools/languages I've seen like [extempore](https://extemporelang.github.io), [Sonic Pi](https://sonic-pi.net), [ChucK](https://chuck.cs.princeton.edu), [Pure Data](https://puredata.info), and [VCV Rack](https://vcvrack.com). These systems vary in the level of detail required for audio programming. For e.g. extempore, ChucK and Sonic Pi all require coding and having to know the underlying "api" well. On the other hand, Pure Data and VCV Rack are more "simple" in that the api is lifted to a GUI and it's a lot faster to start building components visually.

My **goal** is to build a purely Python system that allows the flexibility of using either *text-based* or *visual-based* audio programming.

I've come up with an initial folder schema, but here's what you should know in terms of what works:

- The more stable modules are in [main](https://github.com/nischalshrestha/YAMS/tree/master/main), which contain basic audio generation, synthesis, a schedular (for accurate audio timing using audio device time) and some music theory facilities. 

- The modules in [modules](https://github.com/nischalshrestha/YAMS/tree/master/modules) are less stable as I'm experimenting with the best way to implement modular synths in Python.

- I would stay clear of [experiments](https://github.com/nischalshrestha/YAMS/tree/master/experiments) which is really just a playground for me to figure what's possible with Python and audio synthesis.

# Dependencies 

Python 3.6 is used. You'll need portaudio v. 19.6.0 before installing the Python dependencies:

Mac: `brew install portaudio`

Linux: 

- `sudo apt-get install libasound-dev` (binds portaudio and pyaudio)
- `tar xvfz [portaudiofile.tgz]` in the directory where `libasound-dev` lives (`/usr/lib`)
- `./configure` inside the portaudio folder (the ALSA should say yes now in output)
- `make`, `make install` and `ldconfig` (makes the so file available)
- `export LD_LIBRARY_PATH=/lib:/usr/lib:/usr/local/lib` 

More [here](https://medium.com/@niveditha.itengineer/learn-how-to-setup-portaudio-and-pyaudio-in-ubuntu-to-play-with-speech-recognition-8d2fff660e94)

Then, `pip install -r requirements.txt`

# Future work

- Coming up with a solid timing engine for musical timings, beats etc.
- A DSL for audio synthesis / composition
- An interpreter mode which is a precursor to a GUI mode
- A GUI mode that abstracts the underlying API
