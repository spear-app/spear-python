'''import rx
import rx.operators as ops
import diart.operators as myops
from diart.sources import MicrophoneAudioSource
import diart.functional as fn

sample_rate = 16000
mic = MicrophoneAudioSource(sample_rate)

# Initialize independent modules
segmentation = fn.FrameWiseModel("pyannote/segmentation")
embedding = fn.ChunkWiseModel("pyannote/embedding")
osp = fn.OverlappedSpeechPenalty(gamma=3, beta=10)
normalization = fn.EmbeddingNormalization(norm=1)

# Reformat microphone stream. Defaults to 5s duration and 500ms shift
regular_stream = mic.stream.pipe(myops.regularize_stream(sample_rate))
# Branch the microphone stream to calculate segmentation
segmentation_stream = regular_stream.pipe(ops.map(segmentation))
# Join audio and segmentation stream to calculate speaker embeddings
embedding_stream = rx.zip(regular_stream, segmentation_stream).pipe(
    ops.starmap(lambda wave, seg: (wave, osp(seg))),
    ops.starmap(embedding),
    ops.map(normalization)
)

embedding_stream.subscribe(on_next=lambda emb: print(emb.shape))

mic.read()'''
import argparse
import os
import time
from pathlib import Path

import diart.operators as dops
import threading
import diart.sources as src
import rx.operators as ops
from diart.pipelines import OnlineSpeakerDiarization
from diart.sinks import RealTimePlot, RTTMWriter
import speech_recognition as sr

# Define script arguments
'''
parser = argparse.ArgumentParser()
parser.add_argument("source",default='microphone', type=str, help="'microphone'")
parser.add_argument("--step", default=0.5, type=float, help="Source sliding window step")
parser.add_argument("--latency", default=0.5, type=float, help="System latency")
parser.add_argument("--sample-rate", default=16000, type=int, help="Source sample rate")
parser.add_argument("--tau", default=0.5, type=float, help="Activity threshold tau active")
parser.add_argument("--rho", default=0.3, type=float, help="Speech duration threshold rho update")
parser.add_argument("--delta", default=1, type=float, help="Maximum distance threshold delta new")
parser.add_argument("--gamma", default=3, type=float, help="Parameter gamma for overlapped speech penalty")
parser.add_argument("--beta", default=10, type=float, help="Parameter beta for overlapped speech penalty")
parser.add_argument("--max-speakers", default=20, type=int, help="Maximum number of identifiable speakers")
parser.add_argument(
    "--output", type=str,
    help="Output directory to store the RTTM. Defaults to home directory "
         "if source is microphone or parent directory if source is a file"
)
args = parser.parse_args()
#args.source = "microphone"
'''
r = sr.Recognizer()
audio_data = []
text_data = []
start = True
def record_audio():
    while (True):
        # for i in range(5):
        with sr.Microphone() as source:
            # read the audio data from the default microphone
            print("listening")
            audio_data.append(r.record(source, duration=5))


def recognize_text():
    while (True):
        try:
            if (len(audio_data) == 0):
                continue
            audio = audio_data.pop(0)
            text = r.recognize_google(audio, language="ar-EG")
            text_data.append(text)
            #print(text_data[len(text_data)-1],'.......................')
            #print(text)
        except sr.UnknownValueError:
            text_data.append(" ")
            #print(" ")
            #print(text_data[len(text_data) - 1],".................................")


# Define online speaker diarization pipeline

def diarization():
    global start
    pipeline = OnlineSpeakerDiarization(
        step=0.5,
        latency=0.5,
        tau_active=0.5,
        rho_update=0.3,
        delta_new=1,
        gamma=3,
        beta=10,
        max_speakers=20,
        # source=args.source
    )

    # Manage audio source

    output_dir = Path("D:\\python test\\").expanduser()
    audio_source = src.MicrophoneAudioSource(16000)

    # Build pipeline from audio source and stream predictions to a real-time plot
    pipeline.from_source(audio_source).pipe(
        ops.do(RTTMWriter(path=output_dir / "output.txt")),
        dops.buffer_output(
            duration=pipeline.duration,
            step=pipeline.step,
            latency=pipeline.latency,
            sample_rate=audio_source.sample_rate
        ),
    ).subscribe()

    # print(pipeline.latency)

    # Read audio source as a stream

    print("Recording...")
    start = False
    audio_source.read()



def readfile():
    global text_data
    global start
    duration = 5
    while start:
        continue
    time.sleep(10.5)

    '''while os.path.exists("output.txt"):
        continue'''
    print("start......................................")
    i = 0
    while True:
        if not text_data:
            #print("wating")
            continue
        t = text_data.pop(0)
        #print(t,"hhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
        if(t == " "):
            duration = duration + 5
            continue

        file = open("output.txt", "r")
        while True:
            '''if len(file.readlines())<(i-1):
                break'''
            line = file.readline()
            list = line.split(" ")
            #i+=1
            if (len(list) <= 1):
                continue


            if float(list[3]) > duration:
                print(list[7],t)
                duration = duration + 5
                break
        file.close()


try:
    threading.Thread(target=record_audio).start()
    threading.Thread(target=recognize_text).start()
    threading.Thread(target=diarization).start()
    threading.Thread(target=readfile).start()
except:
   print ("Error: unable to start thread")
