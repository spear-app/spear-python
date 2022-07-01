import threading

import speech_recognition as sr
from threading import Thread

audio_data = []

r = sr.Recognizer()
duration=5

def record_audio():
    while (True):
        # for i in range(5):
        with sr.Microphone() as source:
            # read the audio data from the default microphone
            audio_data.append(r.record(source, duration=5))


def recognize_text():
    global duration
    while (True):
        try:
            if (len(audio_data) == 0):
                continue
            text = r.recognize_google(audio_data.pop(0), language="en-US")
            print(duration," ",text)
            duration+=5
        except sr.UnknownValueError:
            print("error")


threading.Thread(target=record_audio).start()
threading.Thread(target=recognize_text).start()

'''
if __name__ == '__main__':
    Thread(target = func1).start()
    while (True):
        Thread(target = func2).start()
'''

'''

filename = "X2zqiX6yL3I.wav"
r = sr.Recognizer()

with sr.AudioFile(filename) as source:
    # listen for the data (load audio to memory)
    audio_data = r.record(source)
    # recognize (convert from speech to text)
    text = r.recognize_google(audio_data, language="ar-EG")
    print(text)
'''
'''
r = sr.Recognizer()

while (True):
    with sr.Microphone() as source:
        # read the audio data from the default microphone
        audio_data = r.record(source, duration=5)
        print("Recognizing...")
        # convert speech to text
        try:
            text = r.recognize_google(audio_data, language="ar-EG")
            print(text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
'''