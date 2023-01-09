import random

def hello():
    greetings = ("Hello, how can I help you?", "Hi", "Hey", "Hello", "What can I do for you?", "What did you need?", "How is it going?")
    #wellness = ("I am well, how are you?", )
    respone = random.choice(greetings)
    return respone
