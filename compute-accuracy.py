import warnings
import json
import random
import csv
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
		for i in range(50):
			randomTimeSnippet = random.randint(1000, 10000)
			randomOriginalSoundLevel = random.randint(-60, 50)
			randomWhiteNoiseLevel = random.randint(-60, 50)

			#compose test case
			snippets = composeTestCase("mp3/Sean-Fournier--Falling-For-You.mp3", randomTimeSnippet, randomOriginalSoundLevel, {"mp3/Relaxing Fan White Noise For Sleeping, Studying, Soothing Crying Baby, Insomnia.mp3" : randomWhiteNoiseLevel})
	
			snippets[0].export("overlays/original-snippet.mp3", format="mp3")
			snippets[1].export("overlays/overlayed-track.mp3", format="mp3")
	
			#save resulting audio:
	
			# create a Dejavu instance
			djv = Dejavu(config)

			# Recognize audio from its original file
			originalAudio = djv.recognize(FileRecognizer, "overlays/original-snippet.mp3")
			#print "From file we recognized: %s\n" % originalAudio
	
			# Recognize audio from a file with various noises overlayed on top of it
			overlayedAudio = djv.recognize(FileRecognizer, "overlays/overlayed-track.mp3")
			#print "From file we recognized: %s\n" % overlayedAudio
			try:
				if(originalAudio["song_id"] == overlayedAudio["song_id"]):
					print "correct match"
					correctCount = correctCount + 1
				else:
					print "Incorrect match"
			except TypeError:
				print "Incorrect match"
		print "accuracy computed as %s" % str(correctCount*100.0 / i)
		

def fingerprintAndComputeAccuracy(fingerprintReduction, peakSort, defaultOverlapRatio, defaultFanValue, defaultAmpMin, peakNeighbourhoodSize):
	# create a Dejavu instance
	djv = Dejavu(config)

	# Fingerprint all the mp3's in the directory we give it
	djv.fingerprint_directory("mp3", [".mp3"])
