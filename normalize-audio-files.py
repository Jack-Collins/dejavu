import warnings
import json
import random
import csv
warnings.filterwarnings("ignore")
from dejavu.testing import *
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer
from pydub import AudioSegment	

# load config from a JSON file (or anything outputting a python dictionary)
with open("dejavu.cnf.SAMPLE") as f:
    config = json.load(f)


if __name__ == '__main__':
	for subdir, dirs, files in os.walk("mp3"):
		for f in files:
			currentMp3 = AudioSegment.from_mp3(subdir + "/" + f)
			print(int(currentMp3.dBFS))	
			
