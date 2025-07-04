from pydub import AudioSegment as AS
import os

folder = 'AudioClip'
res = AS.empty()
silence = AS.silent(duration=500)
for file in os.listdir(folder):
    res += AS.from_file(os.path.join(folder, file)) + silence
    print(file)

res.export("concatenated_audio.wav", format="wav")
