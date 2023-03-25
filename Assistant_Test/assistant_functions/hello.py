import random
import pyjokes

Ugreetings = ("what's up", "hi", "hey", "hello")
apprecation = ("thanks", "thank you", "appreciate it")
wellness = ("how are you", "how is it going", "how's it going")
joke = ("joke", "funny", "laugh", "giggle", "chuckle", "hilarious")

def hello(text):
    grtResponse = ("Hello, how can I help you?", "Hi, what can I do for you?", "Hello, is there something I can help you with?")
    wlnsResponse = ("I am well, thanks for asking. Is there something I can help you with?", "Good, thank you for asking. How can I assist you?")
    aprResponse = ("You are very welcome", "Your welcome", "Glad I could be of service", "Always happy to help", "Of course")

    greet_check = [phrase for phrase in Ugreetings if(phrase in text.lower())]
    apr_check = [phrase for phrase in apprecation if(phrase in text.lower())]
    wlns_check = [phrase for phrase in wellness if(phrase in text.lower())]
    fun_check = [phrase for phrase in joke if(phrase in text.lower())]

    if (len(greet_check) > 0):
        response = random.choice(grtResponse)
    elif (len(apr_check) > 0):
        response = random.choice(aprResponse)
    elif (len(wlns_check) > 0):
        response = random.choice(wlnsResponse)
    elif (len(fun_check) > 0):
        response = pyjokes.get_joke()
    else:
        response = "I'm sorry, I didn't understand what you said"
    
    return response
