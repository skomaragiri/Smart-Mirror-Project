from intent_classification.intent_classification import IntentClassifier
intent_classifier = IntentClassifier()
from assistant_functions.hello import *
import pyttsx3
import speech_recognition as sr


class Assistant:

    mappings = {'greeting': hello()}

    def __init__(self, name):
        self.name = name #Create instance variable name
        
        self.speech_engine = pyttsx3.init()
        self.speech_engine.setProperty("rate", 150)

        self.r = sr.Recognizer() #Speech recognizer
        self.mic = sr.Microphone(device_index=0) #Change device_index 

    def listen(self):
        """Uses speech_recognition library to listen to get audio input and understand what the user is saying"""
    
        with self.mic as source:
            print("listening")
            audio = self.r.listen(source, timeout=7, phrase_time_limit=10) 

        return self.r.recognize_google(audio)


    def say(self, text):
        """Uses pyttsx3 engine text-to-speech to to say 'text' argument"""

        self.speech_engine.say(text)
        self.speech_engine.runAndWait()


    def reply(self, text):
        intent = intent_classifier.predict(text)

        replies = {
            'greeting' : hello,
            'leaving' : bye,
            'weather' : weather,
            'internet' : search,
            'reminder' : remind,
            'news' : news,
            'time' : timeCheck,
            'calendar' : date
            }

        reply_func = replies[intent]

        if callable(reply_func):
            self.say(reply_func()) #Line to change ... everything else is same

    
    def main(self):
        while True:
            said = self.listen()
            self.reply(said)


assistant = Assistant("Assistant")
assistant.main()