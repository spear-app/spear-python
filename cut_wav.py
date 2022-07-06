import wave
from string import Template

# times between which to extract the wave from
start = 0 # seconds
end = 180 # seconds
# file to extract the snippet from
with wave.open('/home/rahma/Downloads/SS149_Kassywedding.wav', "rb") as infile:
    # get file data
    nchannels = infile.getnchannels()
    sampwidth = infile.getsampwidth()
    framerate = infile.getframerate()
    # set position in wave to start of segment
    infile.setpos(int(start * framerate))
    # extract data
    data = infile.readframes(int((end - start) * framerate))

# write the extracted data to a new file
with wave.open('/home/rahma/speech_files/voice.wav', 'w') as outfile:
    outfile.setnchannels(nchannels)
    outfile.setsampwidth(sampwidth)
    outfile.setframerate(framerate)
    outfile.setnframes(int(len(data) / sampwidth))
    outfile.writeframes(data)

