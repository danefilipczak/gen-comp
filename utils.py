
from midi2audio import FluidSynth
from music21 import midi
import os


def render(stream, path):
	'''
		convert a music21 stream into a wav file using midi2audio, 
		then optionally display it in the ipython notebook
	'''
	mf = midi.translate.streamToMidiFile(stream)
	mf.open('temp.mid', 'wb')
	mf.write()
	mf.close()
	fs = FluidSynth()
	fs.midi_to_audio('temp.mid', path)
	os.remove('temp.mid')
