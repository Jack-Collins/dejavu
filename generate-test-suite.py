import warnings
import json
import random
import csv
import shutil
import os
warnings.filterwarnings("ignore")
from dejavu.testing import *
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer
from pydub import AudioSegment

def composeTestCase(pathToOriginalSong, timeSnippet, originalSongVolumeShift, overlayedNoiseVolumeShifts):
	print("File: %s" % pathToOriginalSong, "Attributes: %s" % str(originalSongVolumeShift) + "," + str(overlayedNoiseVolumeShifts.values()))
	originalAudio = AudioSegment.from_mp3(pathToOriginalSong)
	audioSnippet = trimAudio(originalAudio, timeSnippet, 10000)
	originalSnippet = audioSnippet
	print(audioSnippet.dBFS)
	audioSnippet = audioSnippet  + originalSongVolumeShift
	for noise in overlayedNoiseVolumeShifts.keys():
		overlay = AudioSegment.from_mp3(noise)
		overlaySnippet = trimAudio(overlay, timeSnippet, 10000)
		overlaySnippet = overlaySnippet + overlayedNoiseVolumeShifts[noise]
    		audioSnippet = audioSnippet.overlay(overlaySnippet, position = 0)
	return [originalSnippet, audioSnippet]
	


def trimAudio(audio, time, padding):
	randomPosition = random.randint(padding, len(audio) - padding - time)
	audio = audio[randomPosition:randomPosition + time]
	return audio
	
	

# load config from a JSON file (or anything outputting a python dictionary)
with open("dejavu.cnf.SAMPLE") as f:
    config = json.load(f)

correctCount = 0;

if __name__ == '__main__':
		# remove old test suite
		shutil.rmtree('test_suite_originals')	
		shutil.rmtree('test_suite_overlays')			
		os.mkdir('test_suite_originals')
		os.mkdir('test_suite_overlays')
		for i in range(50):
			randomTrack = random.choice(os.listdir("isolated_test_mp3"))
			randomTimeSnippet = random.randint(1000, 10000)
			randomOriginalSoundLevel = random.randint(-60, 50)
			randomWhiteNoiseLevel = random.randint(-60, 50)

			#compose test case
			trackName = randomTrack.split(".mp3")[0]
			snippets = composeTestCase("isolated_test_mp3/" + trackName + ".mp3", randomTimeSnippet, randomOriginalSoundLevel, {"overlays/whitenoise.mp3" : randomWhiteNoiseLevel})
	
			#Save test case to the test suite for later use
			snippets[0].export("test_suite_originals/" + trackName + "__" + str(i) + ".mp3", format="mp3")
			snippets[1].export("test_suite_overlays/" + trackName + "__" + str(i) + ".mp3", format="mp3")
	


