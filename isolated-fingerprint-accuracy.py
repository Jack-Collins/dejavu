import warnings
import json
import os
import shutil
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer

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
	djv.fingerprint_directory("isolated_test_mp3", [".mp3"])
	
	files = 0
	correctMatches = 0;
	# Recognize all files from test suite
	# loop through length of folder and check for correct match and compute percentage retained
	for snippet in os.listdir('test_suite_overlays'):
		files = files + 1
		matchedSong = djv.recognize(FileRecognizer, 'test_suite_overlays/' + snippet)
		try:
			songMatched = matchedSong['song_name'] 	
			if(songMatched == snippet.split('__')[0]):	
				print('CORRECT')
				correctMatches = correctMatches + 1
			else:
				print('INCORRECT')
		except TypeError:
			print('INCORRECT')
	print "Accuracy percentage against test suite computed as %s" % str(correctMatches*100.0/files)
