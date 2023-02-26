import pyttsx3
import speech_recognition as sr


class Listen_Speak:

    def __init__(self):
        
        self.speech_engine = pyttsx3.init()          # initialize text to speach engine for assistant replies
        self.speech_engine.setProperty("rate", 150)  # speaking rate of assistant in words per minute (150wpm)

        self.r = sr.Recognizer() # Speech recognizer
        self.mic = sr.Microphone(device_index=0) # index 0 = default mic of device. Change device_index: pa = pyaudio.PyAudio(); pa.get_device_count() and change index accordingly  

    def listen(self):
        """Uses speech_recognition library to listen to get audio input and understand what the user is saying"""
    

        r = sr.Recognizer() #newline

        with self.mic as source:
            print("listening")
            r.pause_threshold = 0.5 # wait 1sec of silence to determine end of phrase
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
     
        return query.lower() #added .lower()

            
       # return self.r.recognize_google(audio) # return the recognized speech using google speech API


    def say(self, text):
        """Uses pyttsx3 engine text-to-speech to to say 'text' argument"""
        print(f"Assistant: {text}\n") # prints text argument said by assistant for user friendliness 
        self.speech_engine.say(text)  # assistant will get text argument by user specification in assistant functions and convert it to speech. must be used with runandwait command for speech to be audible
        
        self.speech_engine.runAndWait() # assistant will audibly say the tts argument from engine.say

listen_speak = Listen_Speak()