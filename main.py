from vosk import Model, KaldiRecognizer
from playsound import playsound
from vosk import SetLogLevel
import os
import pyaudio
import json
import aiml
import pyttsx3
import sys

SetLogLevel(-1)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

BRAIN_FILE = "brain.dump"

k = aiml.Kernel()

# To increase the startup speed of the bot it is
# possible to save the parsed aiml files as a
# dump. This code checks if a dump exists and
# otherwise loads the aiml from the xml files
# and saves the brain dump.

if os.path.exists(BRAIN_FILE):
    print("Loading from brain file: " + BRAIN_FILE)
    k.loadBrain(BRAIN_FILE)
else:
    print("Parsing aiml files")
    k.bootstrap(learnFiles="std-startup.aiml", commands="load aiml b")
    print("Saving brain file: " + BRAIN_FILE)
    k.saveBrain(BRAIN_FILE)
   

model = Model("vosk_speech_engine/model") #loading model
rec = KaldiRecognizer(model, 16000)

# Opens microphone for listening.
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()
speak("Welcome to ECE Department, How can I help you ?")
playsound('sound.mp3')
print("Listening")

WAKE = "ece assistant"

while True:
    # speak("you can talk now")
    
    data = stream.read(10000)

    if len(data) == 0:
        
        break
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())

        query = result['text']
        a = query.lower()

        print(a)

        if a == "quit" or a == "exit" or a == "close" or a == "goodbye":
            speak("Thank You . Have a nice day !")
            print("Bye Sir. Have a nice day !")
            sys.exit()
        if a == "who are you" or a == "what is your name" or a == "what can you do" or a == "hello":
            speak("I am ECE assistant. you can ask me anything related to this college")
            
        
           

        else:
            response = k.respond(a)
            speak(response)
            print(response)
           
            