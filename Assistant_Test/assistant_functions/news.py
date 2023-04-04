#from gnewsclient import gnewsclient
#import random

from pygooglenews import GoogleNews
import random

def news():

    response = ("Here are today's top stories", "These are todays current events", "This is what is going on today") # tuple of assistant response strings
#    newsList = client.get_news()
#    for item in newsList:
#        ttl = item['title']
#        print(f"{ttl}\n")
#    return random.choice(response)


    gn = GoogleNews()                       # create object of GoogleNews Class
    top = gn.top_news()                     # variable for storing top stories from google news
    headlines = []                          # list for storing top news headlines
    for item in top['entries']:             # loop through all top stories returned to top
        headlines.append(item['title'])     # append headlines to list

    for item in range(5):                   # loop to select 5 random headlines to be displayed to user
        print(random.choice(headlines))
        print("")

    return random.choice(response)          # return 5 random headlines

