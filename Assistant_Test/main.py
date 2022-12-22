from intent_classification.intent_classification import IntentClassifier
intent_classifier = IntentClassifier()
from assistant_functions.hello import hello
from assistant_functions.bye import bye
from assistant_functions.calendar import date
from assistant_functions.IntSearch import search
from assistant_functions.time import timeCheck
from assistant_functions.news import news
from assistant_functions.reminder import remind
from assistant_functions.weather import weather
import pyttsx3
import speech_recognition as sr


class Assistant:

   

    def __init__(self, name):
        self.name = name # Create instance variable name
        
        self.speech_engine = pyttsx3.init()          # initialize text to speach engine for assistant replies
        self.speech_engine.setProperty("rate", 150)  # speaking rate of assistant in words per minute (150wpm)

        self.r = sr.Recognizer() # Speech recognizer
        self.mic = sr.Microphone(device_index=0) # index 0 = default mic of device. Change device_index: pa = pyaudio.PyAudio(); pa.get_device_count() and change index accordingly  

    def listen(self):
        """Uses speech_recognition library to listen to get audio input and understand what the user is saying"""
    

        r = sr.Recognizer() #newline

        with self.mic as source:
            print("listening")
            r.pause_threshold = 1 # wait 1sec of silence to determine end of phrase
            audio = self.r.listen(source, phrase_time_limit=10) #(audio source, seconds of waiting for phrase to start before throwing exception, max seconds of speaking time after phrase start before processing)
            #source, timeout = 7,
        try:
            print("Recognizing...")   
            query = r.recognize_google(audio)#, language ='en-in')
            print(f"User said: {query}\n")
  
        except Exception as e:
            print(e)   
            print("Unable to Recognize your voice.") 
            return "qwertyifnfh"        # return nonsense if not understood to continue loop
     
        return query

            
       # return self.r.recognize_google(audio) # return the recognized speech using google speech API


    def say(self, text):
        """Uses pyttsx3 engine text-to-speech to to say 'text' argument"""
        print(f"Assistant: {text}\n") # prints text argument said by assistant for user friendliness 
        self.speech_engine.say(text)  # assistant will get text argument by user specification in assistant functions and convert it to speech. must be used with runandwait command for speech to be audible
        
        self.speech_engine.runAndWait() # assistant will audibly say the tts argument from engine.say
        


    def reply(self, text):
        intent = intent_classifier.predict(text)  # takes user speech as text argument to predict intent using Naive Bayes model 

        # Dictionary of user mapped functions based on predicted intent of user speech
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

        reply_func = replies[intent]    # reply_func gets the function to execute based on the intent predicted from user speech

        if callable(reply_func):        # if the function is callable execute function
             if(intent == 'internet'):
                self.say(reply_func(text))      # generates speech from returned text string in user function
             else:
                 self.say(reply_func())

        #testing

        #if callable(reply_func):
         #   self.say(reply_func(text))


    def main(self):
        while True:
            said = self.listen()        # listen for user speech input
            #print(f"\nYou: {said}")     # print user speech for user friendliness and debugging purposes (what did the AI hear)
            if(said == "qwertyifnfh"):  # if what was said was not understood
                continue
            self.reply(said)            # take user speech as said argument for the reply function
            
intentclassifier = IntentClassifier()
assistant = Assistant("Assistant")      # name of assistant
assistant.main()                        # run main method