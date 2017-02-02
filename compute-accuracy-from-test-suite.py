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

correctCount = 0
num = 0
totalMatchTime = 0
if __name__ == '__main__':
		for root, dirs, filenames in os.walk("test_suite_originals/mp3/classical"):
			for f in filenames:
				num = num + 1
				originalSnippet = AudioSegment.from_mp3(root + "/" + f)
				overlayedSnippet = AudioSegment.from_mp3("test_suite_overlays" + root.split("originals")[1] + "/" + f)
				#compose test case
				snippets = [originalSnippet, overlayedSnippet]
	
				snippets[0].export("overlays/original-snippet.mp3", format="mp3")
				snippets[1].export("overlays/overlayed-track.mp3", format="mp3")
				print(snippets[0] /(snippets[0].dBFS))
				#save resulting audio:
	
				# create a Dejavu instance
				djv = Dejavu(config)

				# Recognize audio from its original file
				originalAudio = djv.recognize(FileRecognizer, "overlays/original-snippet.mp3")
				#print "From file we recognized: %s\n" % originalAudio
	
				# Recognize audio from a file with various noises overlayed on top of it
				overlayedAudio = djv.recognize(FileRecognizer, "overlays/overlayed-track.mp3")
				totalMatchTime = totalMatchTime + overlayedAudio["match_time"]
				#print "From file we recognized: %s\n" % overlayedAudio
				try:
					if(originalAudio["song_id"] == overlayedAudio["song_id"]):
						print "correct match"
						correctCount = correctCount + 1
					else:
						print "Incorrect match"
				except TypeError:
					print "Incorrect match"
		print "accuracy computed as %s" % str(correctCount*100.0 / num)
		print "average match time computed as %s" % str(totalMatchTime*1.0 / num)

