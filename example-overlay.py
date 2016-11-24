import warnings
import json
warnings.filterwarnings("ignore")

from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer

# load config from a JSON file (or anything outputting a python dictionary)
with open("dejavu.cnf.SAMPLE") as f:
    config = json.load(f)

if __name__ == '__main__':

	# create a Dejavu instance
	djv = Dejavu(config)

	# Fingerprint all the mp3's in the directory we give it
	djv.fingerprint_directory("mp3", [".mp3"])

	# Recognize audio from its original file
	song = djv.recognize(FileRecognizer, "mp3/Over - Kings of Leon.mp3", 10)
	print "From file we recognized: %s\n" % song
	
	# Recognize audio from a file with white noise overlayed on top of it
	song = djv.recognize(FileRecognizer, "overlays/overlayed-track.mp3", 10)
	print "From file we recognized: %s\n" % song
	
