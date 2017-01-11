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

if __name__ == '__main__':
	with open("results.csv", "wb") as csvfile:
		for i in range(1000):
			randomTimeSnippet = random.randint(1000, 10000)
			randomOriginalSoundLevel = random.randint(-60, 50)
			randomWhiteNoiseLevel = random.randint(-60, 50)
			randomCoffeeShopNoiseLevel = random.randint(-60, 50)

			#compose test case
			snippets = composeTestCase("mp3/Sean-Fournier--Falling-For-You.mp3", randomTimeSnippet, randomOriginalSoundLevel, {"overlays/Relaxing Fan White Noise For Sleeping, Studying, Soothing Crying Baby, Insomnia.mp3" : randomWhiteNoiseLevel, "overlays/Coffee Shop Sound Effect.mp3" : randomCoffeeShopNoiseLevel})
			
			#save resulting audio:
			snippets[0].export("overlays/original-snippet.mp3", format="mp3")
			snippets[1].export("overlays/overlayed-track.mp3", format="mp3")
			
			#Note original dBFS value of snippet along with dBFS change applied:
			originalSnippet = AudioSegment.from_mp3("overlays/original-snippet.mp3")
			audioSnippet = AudioSegment.from_mp3("overlays/overlayed-track.mp3")
			dBFSOriginal = 	originalSnippet.dBFS	
			dBFSChange = audioSnippet.dBFS - dBFSOriginal
	
			# create a Dejavu instance
			djv = Dejavu(config)

			# Recognize audio from its original file
			originalAudio = djv.recognize(FileRecognizer, "overlays/original-snippet.mp3")
			#print "From file we recognized: %s\n" % originalAudio
	
			# Recognize audio from a file with various noises overlayed on top of it
			overlayedAudio = djv.recognize(FileRecognizer, "overlays/overlayed-track.mp3")
			#print "From file we recognized: %s\n" % overlayedAudio
			writer = csv.writer(csvfile, delimiter=',')
			try:
				if(originalAudio["song_id"] == overlayedAudio["song_id"]):
					print "Percentage of fingerprints retained %s" % (overlayedAudio["confidence"]*100.0/originalAudio["confidence"] )
					writer.writerow([dBFSOriginal, dBFSChange, randomTimeSnippet, randomWhiteNoiseLevel, randomCoffeeShopNoiseLevel, (overlayedAudio["confidence"]*100.0/originalAudio["confidence"] ), 'CORRECT'])
				else:
					print "Incorrect match"
					writer.writerow([dBFSOriginal, dBFSChange, randomTimeSnippet, randomWhiteNoiseLevel, randomCoffeeShopNoiseLevel, 0, 'INCORRECT'])
			except TypeError:
				print "Incorrect match"
				writer.writerow([dBFSOriginal, dBFSChange, randomTimeSnippet, randomWhiteNoiseLevel, randomCoffeeShopNoiseLevel, 0, 'INCORRECT'])
		i
