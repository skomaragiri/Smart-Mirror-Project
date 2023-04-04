import wikipedia
from assistant_functions.ListenSpeak import listen_speak 


def search(inquiry):
    In = inquiry                                                # A variable for user input used as input to wiki search
    try:
        result = wikipedia.summary(In, sentences = 1)           # Result is a summary of wikipedia page in 1 sentence
    except wikipedia.DisambiguationError as e:                  # Handle disambiguation error for unclear inquiry
        s = random.choice(e.options)                            # if multiple returns from unclear inquiry pick a random choice to summarize
        #p = wikipedia.page(s)
        listen_speak.say(f"I found a bunch of stuff related to {In}, here is something I found; if this is not what you are looking for could you try being a little more specific?") # inform user that result may not be exactly what is requested
        result = str(wikipedia.summary(s, sentences = 1))       # summarize random return in 1 sentence
    
    #print(result)
    #result = str(wikipedia.summary(In, sentences = 1))
    return f"{result}\n"                                        # return summary to be spoken to user by say method






