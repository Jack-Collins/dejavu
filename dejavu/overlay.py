from pydub import AudioSegment

#read in audio files
sound1 = AudioSegment.from_mp3("U:\Cadet - Letter To Krept.mp3")
sound2 = AudioSegment.from_mp3("U:\white noise.mp3")

sound1_10_db_quieter = sound1 - 10
sound2_very_loud = sound2 + 36

#overlay the loud white noise on the quiet song:
output = sound1_10_db_quieter.overlay(sound2_very_loud, position = 0)

#save resulting audio:

output.export("mixed_sound.mp3", format="mp3")
