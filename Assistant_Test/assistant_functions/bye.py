from assistant_functions.ListenSpeak import listen_speak 
import random

def bye():
    goodbyes = ["Goodbye", "I'm glad I could be of service", "See you next time"]
    listen_speak.say(random.choice(goodbyes))
    quit()
    
    
