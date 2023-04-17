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
from assistant_functions.Help import assist

from assistant_functions.ListenSpeak import listen_speak 

import pyttsx3
import speech_recognition as sr
import datetime
import time
from time import strftime
import winsound
freq = 2500
duration = 1000



class Assistant:

   

    def __init__(self, name): # default constructor for Assistant class, used to name Assistant
        self.name = name # Create instance variable name
        
#        self.speech_engine = pyttsx3.init()          # initialize text to speach engine for assistant replies
#        self.speech_engine.setProperty("rate", 150)  # speaking rate of assistant in words per minute (150wpm)

#        self.r = sr.Recognizer() # Speech recognizer
#        self.mic = sr.Microphone(device_index=0) # index 0 = default mic of device. Change device_index: pa = pyaudio.PyAudio(); pa.get_device_count() and change index accordingly  

#    def listen(self):
        """Uses speech_recognition library to listen to get audio input and understand what the user is saying"""
    

#        r = sr.Recognizer() #newline

#        with self.mic as source:
#            print("listening")
#            r.pause_threshold = 0.5 # wait 1sec of silence to determine end of phrase
#            audio = self.r.listen(source, phrase_time_limit=10) #(audio source, seconds of waiting for phrase to start before throwing exception, max seconds of speaking time after phrase start before processing)
            #source, timeout = 7,
#        try:
#            print("Recognizing...")   
#            query = r.recognize_google(audio)#, language ='en-in')
#            print(f"User said: {query}\n")
  
#        except Exception as e:
#            print(e)   
#            print("Unable to Recognize your voice.") 
#            return "qwertyifnfh"        # return nonsense if not understood to continue loop
     
#        return query

            
       # return self.r.recognize_google(audio) # return the recognized speech using google speech API


#    def say(self, text):
        """Uses pyttsx3 engine text-to-speech to to say 'text' argument"""
#        print(f"Assistant: {text}\n") # prints text argument said by assistant for user friendliness 
#        self.speech_engine.say(text)  # assistant will get text argument by user specification in assistant functions and convert it to speech. must be used with runandwait command for speech to be audible
        
#        self.speech_engine.runAndWait() # assistant will audibly say the tts argument from engine.say
        


    def reply(self, text):
        intent = intent_classifier.predict(text)  # takes user speech as text argument to predict intent using Naive Bayes model 

        # Dictionary of user mapped functions keyed on predicted intent of user speech
        replies = {                 
            'greeting' : hello,
            'leaving' : bye,
            'weather' : weather,
            'internet' : search,
            'reminder' : remind,
            'news' : news,
            'time' : timeCheck,
            'calendar' : date,
            'help' : assist
            }

        reply_func = replies[intent]                 # reply_func gets the function to execute based on the intent predicted from user speech

        if callable(reply_func):                     # if the function is callable execute function
             if (intent == 'internet'):              # Conditional statements used for executing dictionary functions that take parameters in the form of user speech input
                #self.say(reply_func(text))     
                listen_speak.say(reply_func(text))   # return string from function call spoken by say method
             elif (intent == 'reminder'):
                #self.say(reply_func(text))
                listen_speak.say(reply_func(text))
             elif (intent == 'weather'):
                #self.say(reply_func(text))
                listen_speak.say(reply_func(text))
             elif (intent == 'calendar'):
                #self.say(reply_func(text))
                listen_speak.say(reply_func(text))
             elif (intent == 'time'):
                #self.say(reply_func(text))
                listen_speak.say(reply_func(text))
             elif (intent == 'greeting'):
                #self.say(reply_func(text))
                listen_speak.say(reply_func(text))
             else:
                 #self.say(reply_func())
                 listen_speak.say(reply_func())

        #testing

        #if callable(reply_func):
         #   self.say(reply_func(text))


    def main(self):
        WAKE = "hey marvis"                             # Wake phrase that must be spoken before assistant will execute functions
        hour = int(datetime.datetime.now().hour)        # get current hour from system time and use it to greet user based on time of day
        if hour>= 0 and hour<12:
            #self.say("Good Morning!\n")
            listen_speak.say("Good Morning!\n")
  
        elif hour>= 12 and hour<18:
            #self.say("Good Afternoon!\n")
            listen_speak.say("Good Afternoon!\n")
  
        else:
            #self.say("Good Evening!\n")
            listen_speak.say("Good Evening!\n") 

        

        while True:                                     # infinite loop 
            print("Say 'Hey Marvis' to get started, then speak after the beep")        # Instruct user of what to say before they can ask for information
            #said = self.listen()        
            #print("Listening")
            said = listen_speak.listen()                # listen for user speech input

            if said.count(WAKE) > 0:                    # if number of non overlapping occurances of the wake phrase is greater than 0 listen for commands
                winsound.Beep(freq, duration)
                said = listen_speak.listen()   # Listen method of listen_speak object to pick up user speech input                                          # * In Use *
                #said = "Is it hot today"      # For debugging using text
                #print(f"\nYou: {said}")       # print user speech for user friendliness and debugging purposes (what did the AI hear)
                if(said == "qwertyifnfh"):     # if what was said was not understood. String of random characters returned from listen method exception handler as flag for conditional 
                    continue                   # restart while loop 
                self.reply(said)               # take user speech as said argument for the reply function
            
intentclassifier = IntentClassifier()          # create object of the intent classifier function to train AI model 
assistant = Assistant("Marvis")                # create onject of the assistant class and name assistant "Marvis"
assistant.main()                               # run main method