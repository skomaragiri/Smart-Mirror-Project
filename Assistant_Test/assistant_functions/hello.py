import random
import pyjokes

Ugreetings = ("what's up", "hi", "hey", "hello")                        # tuple with greeting strings that user might say checked so assistant can respond properly
apprecation = ("thanks", "thank you", "appreciate it")                  # tuple with appreciation strings that user might say checked so assistant can respond properly
wellness = ("how are you", "how is it going", "how's it going")         # tuple with wellness strings that user might say checked so assistant can respond properly
joke = ("joke", "funny", "laugh", "giggle", "chuckle", "hilarious")     # tuple with joke request strings that user might say checked so assistant can respond properly

def hello(text):
    grtResponse = ("Hello, how can I help you?", "Hi, what can I do for you?", "Hello, is there something I can help you with?")                    # tuple for assistant responses to greeting strings
    wlnsResponse = ("I am well, thanks for asking. Is there something I can help you with?", "Good, thank you for asking. How can I assist you?")   # tuple for assistant responses to wellness strings
    aprResponse = ("You are very welcome", "Your welcome", "Glad I could be of service", "Always happy to help", "Of course")                       # tuple for assistant responses to appreciation strings

    greet_check = [phrase for phrase in Ugreetings if(phrase in text.lower())]      # check if user said greeting string
    apr_check = [phrase for phrase in apprecation if(phrase in text.lower())]       # check if user said appreciation string
    wlns_check = [phrase for phrase in wellness if(phrase in text.lower())]         # check if user said wellness string
    fun_check = [phrase for phrase in joke if(phrase in text.lower())]              # check if user asked for a joke

    if (len(greet_check) > 0):
        response = random.choice(grtResponse)                               # if user said greeting assistant returns with random response from greeting responses tuple
    elif (len(apr_check) > 0):
        response = random.choice(aprResponse)                               # if user expressed appreciation assistant returns with random response from appreciation responses tuple
    elif (len(wlns_check) > 0):
        response = random.choice(wlnsResponse)                              # if user said wellnes string assistant returns with random response from wellness responses tuple
    elif (len(fun_check) > 0):
        response = pyjokes.get_joke()                                       # if user asked for joke assistant returns with random response from pyjokes library
    else:
        response = "I'm sorry, I didn't understand what you said"           # default if not understood or user said something not checked for
    
    return response                                                         # return response string for say method of listen_speak
