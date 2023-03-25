import wikipedia
from assistant_functions.ListenSpeak import listen_speak 


def search(inquiry):
    In = inquiry
    try:
        result = str(wikipedia.summary(In, sentences = 1))
    except wikipedia.DisambiguationError as e:
        s = random.choice(e.options)
        #p = wikipedia.page(s)
        listen_speak.say(f"I found a bunch of stuff related to {In}, here is something I found; if this is not what you are looking for could you try being a little more specific?")
        result = str(wikipedia.summary(s, sentences = 1))
    
    #print(result)
    #result = str(wikipedia.summary(In, sentences = 1))
    return f"{result}\n"






