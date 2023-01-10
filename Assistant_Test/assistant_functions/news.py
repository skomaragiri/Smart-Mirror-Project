#from gnewsclient import gnewsclient
#import random

from pygooglenews import GoogleNews
import random

def news():
#    client = gnewsclient.NewsClient(language = 'english', location ='United States', topic = 'Top Stories', max_results = 3)
#    client = gnewsclient.NewsClient(language = 'english', location ='United States', topic = 'Top Stories', max_results = 3)
#    loc = client.location

    response = ("Here are today's top stories", "These are todays current events", "This is what is going on today")
#    newsList = client.get_news()
#    for item in newsList:
#        ttl = item['title']
#        print(f"{ttl}\n")
#    return random.choice(response)


    gn = GoogleNews()
    top = gn.top_news()
    headlines = []
    for item in top['entries']:
        headlines.append(item['title'])

    for item in range(5):
        print(random.choice(headlines))
        print("")

    return random.choice(response)

