from pydub import AudioSegment
import random
#average mp3 bd level approx 85
# range to generate data for could be considered 50 - 100 db for now? ie + 15 or - 35

#def main():
   # for i in range(1000): # generate 1000 data points
     #   timeSnippet = Math.ceil(rand(10)) # typical time of use case of app like shazam
      #  originalSongVolumeShift = rand(-35, 15) #randomly increase/decrease the file
       # overlayedNoiseVolumeShifts = rand(-35,15) # similarly decrease/increase the noise files at random 
       # composeTestCase(pathToSong, timeSnippet, originalSongVolumeShift, overlayedNoiseVolumeShifts)

def test():
	output = composeTestCase("mp3/Alt-J - Fitzpleasure (Live on KEXP)", 5000, 15, {"mp3/Relaxing Fan White Noise For Sleeping, Studying, Soothing Crying Baby, Insomnia.mp3" : 10})
	output.export("overlays/overlayed-track.mp3", format="mp3")

def composeTestCase(pathToOriginalSong, timeSnippet, originalSongVolumeShift, overlayedNoiseVolumeShifts):
	originalAudio = AudioSegment.from_mp3(pathToOriginalSong)
	audioSnippet = trimAudio(originalAudio, timeSnippet, 10000)

	for noise in overlayedNoiseVolumeShifts.keys():
		overlay = AudioSegment.from_mp3(noise)
		overlaySnippet = trimAudio(overlay, timeSnippet, 10000)
    	audioSnippet = audioSnippet.overlay(overlaySnippet, position = 0)
	return audioSnippet
	


def trimAudio(audio, time, padding):
	randomPosition = random.randint(padding, len(audio) - padding - time)
	audio = audio[randomPosition:randomPosition + time]
	return audio
test()
