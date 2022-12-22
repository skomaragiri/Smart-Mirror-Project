import pyttsx3

def bye():
    voice = pyttsx3.init()
    print("Goodbye")
    voice.say("Goodbye")
    voice.runAndWait()
    quit()
    
    
