from pydub import AudioSegment
#average mp3 bd level approx 85
# range to generate data for could be considered 50 - 100 db for now? ie + 15 or - 35

#def main():
   # for i in range(1000): # generate 1000 data points
     #   timeSnippet = Math.ceil(rand(10)) # typical time of use case of app like shazam
      #  originalSongVolumeShift = rand(-35, 15) #randomly increase/decrease the file
       # overlayedNoiseVolumeShifts = rand(-35,15) # similarly decrease/increase the noise files at random 
       # composeTestCase(pathToSong, timeSnippet, originalSongVolumeShift, overlayedNoiseVolumeShifts)

def test():
    composeTestCase("C:\Users\collijac\Desktop\Over - Kings of Leon.mp3", 5, 15, {"C:\Users\collijac\Desktop\Coffee Shop Sound Effect.mp3" : 10})
def composeTestCase(pathToOriginalSong, timeSnippet, originalSongVolumeShift, overlayedNoiseVolumeShifts):
    originalAudio = AudioSegment.from__mp3(pathToOriginalSong)
    print(len(originalAudio))
    originalAudio = originalAudio[:10]
    print(len(originalAudio))

    #for noise in overlayedNoiseVolumeShifts:
    #originalAudio = originalAudio.overlay(noise.pathToNoise + noise.volumeShift)
