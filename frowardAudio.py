import os

# convert audio from .opus extension to .wav extension
def opus2wav(audio_file):
    new_audio_file = "newFile.wav"
    command = "ffmpeg -i %s -vn %s" %(audio_file, new_audio_file)
    os.system(command)

def trimAudio(audio_file, start, end):
    dummy_file_name = "trimmed.wav"
    if dummy_file_name in os.listdir('./'):
        command = 'del %s' % (dummy_file_name)
        os.system(command)
        
    # trim from start time to stop time
    command = "ffmpeg -i %s -ss %f -to %f -c copy %s" % (audio_file, start, end, dummy_file_name)
    os.system(command)
