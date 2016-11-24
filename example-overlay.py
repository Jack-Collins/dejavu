import warnings
import json
warnings.filterwarnings("ignore")
from dejavu.testing import *
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer
from pydub import AudioSegment

# load config from a JSON file (or anything outputting a python dictionary)
with open("dejavu.cnf.SAMPLE") as f:
    config = json.load(f)

if __name__ == '__main__':
	#generate_test_files("mp3", "overlays", 5, fmts=[".mp3", ".wav"], padding=10)
	#read in audio files
	sound1 = AudioSegment.from_mp3("overlays/Over - Kings of Leon_88_5sec.mp3")
	sound2 = AudioSegment.from_mp3("overlays/Relaxing Fan White Noise For Sleeping, Studying, Soothing Crying Baby, Insomnia_22_5sec.mp3")

	sound1_10_db_quieter = sound1 - 36
	sound2_very_loud = sound2 #+ 36

	#overlay the loud white noise on the quiet song:
	output = sound1_10_db_quieter.overlay(sound2_very_loud, position = 0)

	#save resulting audio:

	output.export("overlays/overlayed-track.mp3", format="mp3")
	
	# create a Dejavu instance
	djv = Dejavu(config)

	# Recognize audio from its original file
	song = djv.recognize(FileRecognizer, "overlays/Over - Kings of Leon_88_5sec.mp3")
	print "From file we recognized: %s\n" % song
	
	# Recognize audio from a file with white noise overlayed on top of it
	song = djv.recognize(FileRecognizer, "overlays/overlayed-track.mp3")
	print "From file we recognized: %s\n" % song
	
	
