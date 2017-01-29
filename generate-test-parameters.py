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
	#print("File: %s" % pathToOriginalSong, "Attributes: %s" % str(originalSongVolumeShift) + "," + str(overlayedNoiseVolumeShifts.values()))
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
	with open("test_parameters.csv", "wb") as csvfile:
		for i in range(100):
			randomTimeSnippet = random.randint(1000, 10000)
			randomOriginalSoundLevel = random.randint(-30, 50)
			randomWhiteNoiseLevel = random.randint(-30, 50)

			#write to csv file:
			writer = csv.writer(csvfile, delimiter=',')
			writer.writerow([randomTimeSnippet, randomOriginalSoundLevel, randomWhiteNoiseLevel])
	genres = []
	for subdir, dirs, files in os.walk("mp3"):	
		if(subdir != "mp3"):
			genres.append(subdir)
	for genreDir in genres:
		with open("test_parameters.csv", "rb") as csvfile:
			reader = csv.reader(csvfile, delimiter=' ')

			# remove old test suites
			shutil.rmtree('test_suite_originals/' + genreDir)
			shutil.rmtree('test_suite_overlays/' + genreDir)			
			os.mkdir('test_suite_originals/' + genreDir)
			os.mkdir('test_suite_overlays/' + genreDir)
			correctCount = 0
			totalMatchTime = 0
			rowNum = 0
			for row in reader:
				rowNum = rowNum + 1
				randomTrack = random.choice(os.listdir(genreDir))
				randomTimeSnippet = int(row[0].split(",")[0])
				randomOriginalSoundLevel = float(row[0].split(",")[1])
				randomWhiteNoiseLevel = float(row[0].split(",")[2])

				#compose test case
				trackName = randomTrack.split(".mp3")[0]
				snippets = composeTestCase(genreDir + "/" + trackName + ".mp3", randomTimeSnippet, randomOriginalSoundLevel, {"overlays/whitenoise.mp3" : randomWhiteNoiseLevel})
	
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
				totalMatchTime = totalMatchTime + overlayedAudio["match_time"]
				try:
					if(originalAudio["song_id"] == overlayedAudio["song_id"]):
						#print "correct match"
						correctCount = correctCount + 1
					#else:
						#print "Incorrect match"
				except TypeError:
					pass

				

				#Save test case to the test suite for later use
				snippets[0].export("test_suite_originals/" + genreDir + "/" + trackName + "__" + str(rowNum) + ".mp3", format="mp3")
				snippets[1].export("test_suite_overlays/" + genreDir + "/" + trackName + "__" + str(rowNum) + ".mp3", format="mp3")
			print "accuracy computed as %s" % str(correctCount*100.0 / rowNum)
			print "average match time computed as %s" % str(totalMatchTime / rowNum)

	
			

	
