import speech_recognition as sr
import sys
filename = sys.argv[1] 
r = sr.Recognizer()
with sr.AudioFile(filename) as source:
    # listen for the data (load audio to memory)
    audio_data = r.record(source)
    # recognize (convert from speech to text)
    try:
        text = r.recognize_google(audio_data)
        print(text)
    except: 
        print("Error:", str(sr.UnknownValueError ))