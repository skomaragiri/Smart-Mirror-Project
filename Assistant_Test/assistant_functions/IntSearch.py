import wikipedia

def search(inquiry):
    In = inquiry
    result = str(wikipedia.summary(In, sentences = 1))
    #print(result)

    return f"{result}\n"






