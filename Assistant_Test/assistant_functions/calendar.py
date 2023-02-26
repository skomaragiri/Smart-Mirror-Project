import time 
import datetime
from time import strftime
#from pymongo import MongoClient
import pymongo
from assistant_functions.ListenSpeak import listen_speak 
import pandas

client = pymongo.MongoClient("mongodb+srv://phelpsian00:W25Zz49Xrv6P1xav@cluster0.h9d6t3f.mongodb.net/test")
dbname = client['Smart_Mirror']
evnt_collection = dbname["Calendar_Events"]
read_strs = ["any events", "anything to do", "am i busy", "do i have plans", "what do i have", "do i have any plans"]


def date(text):
    #dbname = get_database()
    #evnt_collection = dbname["Events"]

    dt = datetime.datetime.now()
    month_name = dt.strftime('%B')
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)    #maybe move to time
    day = int(datetime.datetime.now().day)
    day_name = dt.strftime('%A')
    last_digit = str(day)[-1] 
    #print(f"{last_digit}")

    
      ########################
    rd_check = [phrase for phrase in read_strs if(phrase in text.lower())]
    if (len(rd_check) > 0):
        rd_check = rd_check.pop()
    if rd_check:
       idx = read_strs.index(rd_check)
       retVal = read_event(text.lower(), idx)

    elif "add " in text:
        add_event(text.lower())
        retVal = "Okay, I have added that to your calendar"
    elif "put " in text:
        add_event(text.lower())
        retVal = "Okay, I have add that to your calendar"
    elif "remove" in text:
        retVal = delete_1event(text.lower())
    elif "take" and "off" in text:
        retVal = delete_1event(text.lower())
    elif "delete" in text:
        retVal = delete_1event(text.lower())
    elif "clear my calendar" or "remove all" or "cancel my plans" in text:  # add seperate func for clearing all events on a date
        pass

        
        


    #################################################

    #return f"Today is {day_name}. The date is: {month_name} {day} of, {year}."
    return retVal





def add_event(text):
    if "add an event" in text:
        listen_speak.say("What event would you like to add to your calendar?")
        evnt = listen_speak.listen()
    elif "add another event" in text:
        listen_speak.say("What event would you like to add to your calendar?")
        evnt = listen_speak.listen()
    elif "put an event" in text:
        listen_speak.say("What event would you like to add to your calendar?")
        evnt = listen_speak.listen()
    elif "put another event" in text:
        listen_speak.say("What event would you like to add to your calendar?")
        evnt = listen_speak.listen()

    elif 'add' in text:
         sub1 = 'add'
         sub2 = 'to'
         idx1 = text.index(sub1)
         idx2 = text.rfind(sub2)
         evnt = text[idx1 + len(sub1) + 1 : idx2]
         if evnt[0] == ' ':
             evnt = evnt[1:]
         if evnt[-1] == ' ':
             evnt = evnt[0:-1]

    elif 'put' in text:
         sub1 = 'put'
         if "on " in text:
             sub2 = 'on'
         elif "in " in text:
             sub2 = 'in'
         idx1 = text.index(sub1)
         idx2 = text.rfind(sub2)
         evnt = text[idx1 + len(sub1) + 1 : idx2]
         if evnt[0] == ' ':
             evnt = evnt[1:]
         if evnt[-1] == ' ':
             evnt = evnt[0:-1]
    
    listen_speak.say("what is the starting date of that event?")
    start_date = get_date(listen_speak.listen())          #return in form year(000)-month(00)-day(00)
    start_date = datetime.datetime.combine(start_date, datetime.datetime.min.time()) #returns form year-month-day 00:00:00
    #code to format date

    listen_speak.say("what is the ending date of that event?")
    end_date = get_date(listen_speak.listen())
    end_date = datetime.datetime.combine(end_date, datetime.datetime.min.time()) #returns form year-month-day 00:00:00
    if (start_date == end_date):
        end_date = datetime.datetime.combine(end_date, datetime.datetime.max.time()) #returns form year-month-day 23:59:59
 
    #code to format date
    
    #Event_data = [start_date, end_date, evnt]
    event = {
              "event_start" : start_date,
              "event_end" : end_date,
              "event_name" : f"{evnt}"
            }
    evnt_collection.insert_one(event)
    #print("Event Added")
    return 

#read event: "Do I have any events today/coming up"

def read_event(text, indx):
    #find() all items in collect 
    #break up string 
    #do i have plans tomorrow
    if "coming up" in text:
        found_event = evnt_collection.find().sort('event_start', pymongo.ASCENDING).limit(3) #if works also tell user about other events
        Nextevnts = []
        NextevntsDates = []
        print("Events coming up:\n")
        for i in found_event:
            Nextevnts.append(i['event_name'])
            NextevntsDates.append(i['event_start'])
            print(i['event_name'], i['event_start'])
        nextEvent = Nextevnts[0]
        nextEvntDate = datetime.datetime.strptime(str(NextevntsDates[0]), "%Y-%m-%d %H:%M:%S")
        nextEvntDate = nextEvntDate.date()
        retVal = f"You have {nextEvent} coming up on {nextEvntDate}"
        #nextEvent = found_event[0]
        #print(nextEvent['event_name'], nextEvent['event_start'])
        #retVal = f"You have {nextEvent['event_name']} coming up on {strftime(nextEvent['event_start'])}"
        return retVal

    elif "soon" in text:
        found_event = evnt_collection.find().sort('event_start', pymongo.ASCENDING).limit(3) #if works also tell user about other events
        Nextevnts = []
        NextevntsDates = []
        print("Events coming up:\n")
        for i in found_event:
            Nextevnts.append(i['event_name'])
            NextevntsDates.append(i['event_start'])
            print(i['event_name'], i['event_start'])
        nextEvent = Nextevnts[0]
        nextEvntDate = datetime.datetime.strptime(str(NextevntsDates[0]), "%Y-%m-%d %H:%M:%S")
        nextEvntDate = nextEvntDate.date()
        retVal = f"You have {nextEvent} coming up on {nextEvntDate}"
        #nextEvent = found_event[0]
        #print(nextEvent['event_name'], nextEvent['event_start'])
        #retVal = f"You have {nextEvent['event_name']} coming up on {strftime(nextEvent['event_start'])}"
        return retVal

        #found_event = evnt_collection.find().sort('event_start', pymongo.DESCENDING).limit(3) #if works also tell user about other events
        #nextEvent = found_event[0]
        #print(nextEvent['event_name'], nextEvent['event_start'])
        #retVal = f"You have {nextEvent['event_name']} coming up on {strftime(nextEvent['event_start'])}"

    elif "on" in text:
        Querydate = text.split("on ", 1)[1]
    else:
        Querydate = text.split(f"{read_strs[indx]} ",1)[1]

    QuerydateDT = get_date(Querydate)
    QuerydateDT = datetime.datetime.combine(QuerydateDT, datetime.datetime.min.time()) #returns form year-month-day 00:00:00
    found_event = evnt_collection.find({'event_start': QuerydateDT})
    for i in found_event:
        #evntsDF = pandas.DataFrame(found_evnt)
        print(i['event_name'])
    
    retVal = f"Here is what you have on {Querydate}"
    return retVal

def delete_1event(text):
    
    if "delete an event" in text:
        listen_speak.say("What event would you like to remove from your calendar?")
        ans = listen_speak.listen()
        if "on " in ans:
            Querydate = ans.split("on ", 1)[1]
            QuerydateDT = get_date(Querydate)
            QuerydateDT = datetime.datetime.combine(QuerydateDT, datetime.datetime.min.time())
            evnt_collection.delete_one({'event_start' : QuerydateDT})
            retVal = f"The event on {QuerydateDT} has been removed"
#        elif "next " in ans:
#            Querydate = ans.split("next ", 1)[1]
#            QuerydateDT = get_date(Querydate)
#            QuerydateDT = datetime.datetime.combine(QuerydateDT, datetime.datetime.min.time())
#            evnt_collection.delete_one({'event_start' : QuerydateDT})
#           retVal = f"The event on {QuerydateDT} has been removed"
        elif "one " in ans:
            Querydate = ans.split("one ", 1)[1]
            QuerydateDT = get_date(Querydate)
            QuerydateDT = datetime.datetime.combine(QuerydateDT, datetime.datetime.min.time())
            evnt_collection.delete_one({'event_start' : QuerydateDT})
            retVal = f"The event on {QuerydateDT} has been removed"
        else:
            evnt = ans
            evnt_collection.delete_one({'event_name' : f"{evnt}"})
            retVal = f"{evnt} has been removed from your calendar"

    elif "remove an event" in text:
        listen_speak.say("What event would you like to remove from your calendar?")
        ans = listen_speak.listen()
        if "on " in ans:
            Querydate = ans.split("on ", 1)[1]
            QuerydateDT = get_date(Querydate)
            QuerydateDT = datetime.datetime.combine(QuerydateDT, datetime.datetime.min.time())
            evnt_collection.delete_one({'event_start' : QuerydateDT})
            retVal = f"The event on {QuerydateDT} has been removed"
#        elif "next " in ans:
#            Querydate = ans.split("next ", 1)[1]
#            QuerydateDT = get_date(Querydate)
#            QuerydateDT = datetime.datetime.combine(QuerydateDT, datetime.datetime.min.time())
#            evnt_collection.delete_one({'event_start' : QuerydateDT})
#            retVal = f"The event on {QuerydateDT} has been removed"
        elif "one " in ans:
            Querydate = ans.split("one ", 1)[1]
            QuerydateDT = get_date(Querydate)
            QuerydateDT = datetime.datetime.combine(QuerydateDT, datetime.datetime.min.time())
            evnt_collection.delete_one({'event_start' : QuerydateDT})
            retVal = f"The event on {QuerydateDT} has been removed"
        else:
            evnt = ans
            evnt_collection.delete_one({'event_name' : f"{evnt}"})
            retVal = f"{evnt} has been removed from your calendar"

    

    elif "remove" in text:
         if "on" in text:
            Querydate = text.split("on ", 1)[1]
            QuerydateDT = get_date(Querydate)
            QuerydateDT = datetime.datetime.combine(QuerydateDT, datetime.datetime.min.time())
            evnt_collection.delete_one({'event_start' : QuerydateDT})
            retVal = f"The event on {QuerydateDT} has been removed"
         else:
             sub1 = "remove"
             sub2 = "from"
             idx1 = text.index(sub1)
             idx2 = text.rfind(sub2)
             evnt = text[idx1 + len(sub1) + 1 : idx2]
             if evnt[0] == ' ':
                 evnt = evnt[1:]
             if evnt[-1] == ' ':
                 evnt = evnt[0:-1]
             evnt_collection.delete_one({'event_name': f"{evnt}"})
             retVal = f"{evnt} has been removed from your calendar"
         
    elif "take" in text:
         if "on" in text:
            Querydate = text.split("on ", 1)[1]
            QuerydateDT = get_date(Querydate)
            QuerydateDT = datetime.datetime.combine(QuerydateDT, datetime.datetime.min.time())
            evnt_collection.delete_one({'event_start' : QuerydateDT})
            retVal = f"The event on {QuerydateDT} has been removed"
         else:
             sub1 = "take"
             if "off" in text:
                sub2 = "off"
             elif "out" in text:
                sub2 = "out"
             idx1 = text.index(sub1)
             idx2 = text.rfind(sub2)
             evnt = text[idx1 + len(sub1) + 1 : idx2]
             if evnt[0] == ' ':
                 evnt = evnt[1:]
             if evnt[-1] == ' ':
                 evnt = evnt[0:-1]
             evnt_collection.delete_one({'event_name': f"{evnt}"})
             retVal = f"{evnt} has been removed from your calendar"

    elif "delete" in text:
         if "on" in text:
            Querydate = text.split("on ", 1)[1]
            QuerydateDT = get_date(Querydate)
            QuerydateDT = datetime.datetime.combine(QuerydateDT, datetime.datetime.min.time())
            evnt_collection.delete_one({'event_start' : QuerydateDT})
            retVal = f"The event on {QuerydateDT} has been removed"
         else:
             sub1 = "delete"
             if "from" in text:
                sub2 = "from"
             elif "in" in text:
                sub2 = "in"
             idx1 = text.index(sub1)
             idx2 = text.rfind(sub2)
             evnt = text[idx1 + len(sub1) + 1 : idx2]
             if evnt[0] == ' ':
                 evnt = evnt[1:]
             if evnt[-1] == ' ':
                 evnt = evnt[0:-1]
             evnt_collection.delete_one({'event_name': f"{evnt}"})
             retVal = f"{evnt} has been removed from your calendar"


        
    
        
    return retVal
    

def get_date(text):
    MONTHS = ["january", "february", "march", "april", "may", "june","july", "august", "september","october", "november", "december"]
    DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    DAY_EXTENTIONS = ["rd", "th", "st", "nd"]

    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today
    elif text.count("tomorrow") > 0:
        tomorrow = today + datetime.timedelta(1)
        return tomorrow

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    # THE NEW PART STARTS HERE
    if month != -1 and day == -1:
        listen_speak.say("I'm sorry, I did not catch the day of that event could you please repeat?")
        ans = listen_speak.listen()
        for word in ans.split():
            if word in DAYS:
                day_of_week = DAYS.index(word)
            elif word.isdigit():
                day = int(word)
            else:
                for ext in DAY_EXTENTIONS:
                    found = word.find(ext)
                    if found > 0:
                        try:
                            day = int(word[:found])
                        except:
                            pass

    if month < today.month and month != -1:  # if the month mentioned is before the current month set the year to the next
        year = year+1

    # This is slighlty different from the video but the correct version
    if month == -1 and day != -1:  # if we didn't find a month, but we have a day
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month

    # if we only found a dta of the week
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)

    if day != -1:  # FIXED FROM VIDEO
        return datetime.date(month=month, day=day, year=year)

#def get_database():

#    CONNECTION_STRING = "mongodb+srv://phelpsian00:W25Zz49Xrv6P1xav@cluster0.h9d6t3f.mongodb.net/test"

#    client = MongoClient(CONNECTION_STRING)

#    return client['Calendar_Events']