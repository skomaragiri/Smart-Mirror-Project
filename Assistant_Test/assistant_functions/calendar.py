import time 
import datetime
from time import strftime
#from pymongo import MongoClient
import pymongo
from assistant_functions.ListenSpeak import listen_speak 
import pandas

client = pymongo.MongoClient("mongodb+srv://phelpsian00:W25Zz49Xrv6P1xav@cluster0.h9d6t3f.mongodb.net/test")        # connection url string to link code to mongoDB Compass 
dbname = client['Smart_Mirror']                                                                                     # name of the database client
evnt_collection = dbname["Calendar_Events"]                                                                         # collection name within database

read_strs = ["any events", "anything to do", "am i busy", "do i have plans", "what do i have", "do i have any plans", "do i have events", "what events do i have", "what plans do i have"] # list of strings to check user speech against to determine if user wants to read database documents
clearALL_strs = ["clear my calendar", "remove all", "cancel my plans", "delete all", "clear all", "free up my schedule", "clear my schedule"]                                              # list of strings for checking user speech if they want to delete all events on a date

def date(text):
    
      ########################
    rd_check = [phrase for phrase in read_strs if(phrase in text.lower())]              # check if user input is in read_strs if true read_check is a list of matching phrase
    if (len(rd_check) > 0):                                                             # check length of read_check list to determing if read request made
        rd_check = rd_check.pop()                                                       # remove matched phrase from list
    #if rd_check:
        idx = read_strs.index(rd_check)                                                 # get index of matched phrase
        retVal = read_event(text.lower(), idx)                                          # execute read database method and get string 
        return retVal                                                                   # return string to inform user using say method

    delALL_check = [phrase for phrase in clearALL_strs if(phrase in text.lower())]      # check if user input is in clearALL_strs if true delALL_check is a list of matching phrase
    if (len(delALL_check) > 0):                                                         # check length of delALL_check list to determing if clear all request made
        delALL_check = delALL_check.pop()                                               # remove matching phrase from list
    #if rd_check:
        idx = clearALL_strs.index(delALL_check)                                         # get index of matching phrase
        retVal = delete_ALLevents(text.lower(), idx)                                    # execute delete all database method and get string
        return retVal                                                                   # return string to inform user using say method

    elif "add " in text:                                                                # check if word add was in user input 
        add_event(text.lower())                                                         # call add event method
        retVal = "Okay, I have added that to your calendar"                             # return string to inform user event was added
    elif "put " in text:                                                                # check if 'put' was in user input signifying add event
        add_event(text.lower())                                                         # call add event method
        retVal = "Okay, I have add that to your calendar"                               # return string to inform user event was added
    elif "remove" in text:                                                              # check if user wants to remove an event 
        retVal = delete_1event(text.lower())                                            # return string from delete1event method to inform user event was removed
    elif "take" and "off" in text:                                                      # check if 'take...off' in user input
        retVal = delete_1event(text.lower())                                            # return string from delete1event method to inform user event was removed
    elif "delete" in text:                                                              # check if user wants to delete an event based on input speech string
        retVal = delete_1event(text.lower())                                            # return string from delete1event method to inform user event was removed
    else:
        retVal = "I'm sorry I did not understand"                                       # if unsure of what user wants inform them of such

        
        


    #################################################

    #return f"Today is {day_name}. The date is: {month_name} {day} of, {year}."
    return retVal                                                                       # return retVal string to be spoken back to user using say method





def add_event(text):                                                                    # method for adding events to database

    # condtional statements used to check for various ways user may request to add an event
    # assistant asks user to state the title of the event they would like to add which is stored in variable evnt 
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
    
    # Conditional statements for isolating event title in middle of string for add request 'add...{event}...to..."
    elif 'add' in text:
         sub1 = 'add'
         sub2 = 'to'
         idx1 = text.index(sub1)
         idx2 = text.rfind(sub2)
         evnt = text[idx1 + len(sub1) + 1 : idx2]
         # Remove spaces that may appear at front and/or back of user input string so that the event title does not have extra white space characters that may interfer when referenced by user in future
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
    
    listen_speak.say("what is the starting date of that event?")                        # prompt user for starting date of event 
    start_date = get_date(listen_speak.listen())                                        # user spoken date gets converted to date datetime format using get_date method. return in form year(000)-month(00)-day(00)
    start_date = datetime.datetime.combine(start_date, datetime.datetime.min.time())    # completes full date time format by combing date datetime object with time datetime object returns form year-month-day 00:00:00
    #code to format date

    listen_speak.say("what is the ending date of that event?")                          # user prompted for end date of event
    end_date = get_date(listen_speak.listen())
    end_date = datetime.datetime.combine(end_date, datetime.datetime.min.time())        # returns form year-month-day 00:00:00
    if (start_date == end_date):                                                        # if event ends on same date as start the end time will be the max time/ end of day (11:59pm)
        end_date = datetime.datetime.combine(end_date, datetime.datetime.max.time())    # returns form year-month-day 23:59:59
 
    # MongoDB event schema in form of python dictionary

    event = {
              "event_start" : start_date,
              "event_end" : end_date,
              "event_name" : f"{evnt}"
            }
    evnt_collection.insert_one(event)                                                   # call mongoDB insert_one method to put one event in data base
    #print("Event Added")
    return 

#read event: "Do I have any events today/coming up"

def read_event(text, indx):

    # cases handling if user is asking for events in the near future rather than on a specific date
    if "coming up" in text:                                                                     # check if 'coming up' in request
        found_event = evnt_collection.find().sort('event_start', pymongo.ASCENDING).limit(3)    # search database for all events and sort by start date in ascending/chronological order limit to 3 events returned to variable
        Nextevnts = []                                                                          # list for storing titles of events coming up
        NextevntsDates = []                                                                     # list for storing starting dates of events coming up  
        print("Events coming up:\n")
        for i in found_event:                                                                       # loop to fill lists with titles and start dates of events coming up 
            Nextevnts.append(i['event_name'])
            NextevntsDates.append(i['event_start'])
            print(i['event_name'], i['event_start'])                                                # print event title and start date for the next three events in chronological order for user 
        nextEvent = Nextevnts[0]                                                                    # the next event is the first index in the list 
        nextEvntDate = datetime.datetime.strptime(str(NextevntsDates[0]), "%Y-%m-%d %H:%M:%S")      # format the datetime date object of start time 
        nextEvntDate = nextEvntDate.date()                                                          # convert start time to date
        retVal = f"You have {nextEvent} coming up on {nextEvntDate}"                                # inform user of next event coming up
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

    elif "on" in text:                                            # if want to read an event on a specific date look for word 'on' in request
        Querydate = text.split("on ", 1)[1]                       # isolate date by splitting string after 'on'
    else:
        Querydate = text.split(f"{read_strs[indx]} ",1)[1]        # if 'on' not in request but still want specific date split after read string (ex. do I have plans Thursday)

    QuerydateDT = get_date(Querydate)                                                   # convert user requested date to datetime date object using get_date function
    QuerydateDT = datetime.datetime.combine(QuerydateDT, datetime.datetime.min.time())  # combine datetime date object with datetime time so date is in format of mongoDB schema 

    if evnt_collection.count_documents({'event_start': QuerydateDT}) == 0:              # check if event being search for exists
        retVal = f"I'm sorry, I could not find any event on {QuerydateDT}"
        return retVal

    found_event = evnt_collection.find({'event_start': QuerydateDT})                    # find mmethod searches database for event matching filter of start date
    for i in found_event:                                                               # loop to print every event found on start date
        #evntsDF = pandas.DataFrame(found_evnt)
        print(i['event_name'])
    
    retVal = f"Here is what you have on {Querydate}"
    return retVal

def delete_1event(text): # method for deleting 1 event
    
    # method for deleting an event 
    if "delete an event" in text:
        listen_speak.say("What event would you like to remove from your calendar?")                             # ask user to specify the event to be deleted
        ans = listen_speak.listen()                                                                             # take user answer
        if "on " in ans:                                                                                        # delete an event 'on' a date
            Querydate = ans.split("on ", 1)[1]                                                                  # isolate date in input string
            QuerydateDT = get_date(Querydate)                                                                   # convert string date to datetime date object
            QuerydateDT = datetime.datetime.combine(QuerydateDT, datetime.datetime.min.time())                  # combine date object with datetime time for mongoDB schema format

            if evnt_collection.count_documents({'event_start': QuerydateDT}) == 0:                              # check if event to delete exists
                retVal = f"I'm sorry, I could not find any event on {QuerydateDT}"
                return retVal

            if evnt_collection.count_documents({'event_start': QuerydateDT}) > 1:                               # check if more than 1 event is on the date that the user wants to delete an event
                listen_speak.say("I found multiple events on that date, which one did you want to remove?")     # inform user that multiple events found
                found_event = evnt_collection.find({'event_start': QuerydateDT})                                # find method to get all events on start date
                evnt_names = []                                                                                 # list for storing event titles
                for i in found_event:                                                                           # loop for printing and populating list with event titles
                    #evntsDF = pandas.DataFrame(found_evnt)
                    print(i['event_name'])
                    evnt_names.append(i['event_name'])
                ans = listen_speak.listen()                                                                     # user specifies title of event they want to delete
                evntName_check = [name for name in evnt_names if(name in ans.lower())]                          # loop through user answer to find event title match in list if match found store in list
                if (len(evntName_check) > 0):
                    evntName_check = evntName_check.pop()                                                       # if match found pop from list
                #if evntName_check:
                    idx = evnt_names.index(evntName_check)                                                      # get index of match
                else:
                    retVal = "I'm sorry, I couldn't find that event"                                            # if no match found inform user
                    return retVal
                    
                evnt_collection.delete_one({'event_name' : f"{evnt_names[idx]}"})                               # delete event from database using delete_one method and the title of the event found in list of event names at the retrieved index
                retVal = f"{evnt_names[idx]} on {QuerydateDT} has been removed"
                return retVal

            evnt_collection.delete_one({'event_start' : QuerydateDT})                                           # if only one event found on date delete that event by the date
            retVal = f"The event on {QuerydateDT} has been removed"

        # another method for deleting an event by date (ex '...the one next thursday')
        elif "one " in ans:
            Querydate = ans.split("one ", 1)[1]
            QuerydateDT = get_date(Querydate)
            QuerydateDT = datetime.datetime.combine(QuerydateDT, datetime.datetime.min.time())
            if evnt_collection.count_documents({'event_start': QuerydateDT}) == 0:
                retVal = f"I'm sorry, I could not find any event on {QuerydateDT}"
                return retVal
            if evnt_collection.count_documents({'event_start': QuerydateDT}) > 1:
                listen_speak.say("I found multiple events on that date, which one did you want to remove?")
                found_event = evnt_collection.find({'event_start': QuerydateDT})
                evnt_names = []
                for i in found_event:
                    #evntsDF = pandas.DataFrame(found_evnt)
                    print(i['event_name'])
                    evnt_names.append(i['event_name'])
                ans = listen_speak.listen()
                evntName_check = [name for name in evnt_names if(name in ans.lower())]
                if (len(evntName_check) > 0):
                    evntName_check = evntName_check.pop()
                #if evntName_check:
                    idx = evnt_names.index(evntName_check)
                else:
                    retVal = "I'm sorry, I couldn't find that event"
                    return retVal
                    
                evnt_collection.delete_one({'event_name' : f"{evnt_names[idx]}"})
                retVal = f"{evnt_names[idx]} on {QuerydateDT} has been removed"
                return retVal

            evnt_collection.delete_one({'event_start' : QuerydateDT})
            retVal = f"The even on {QuerydateDT} has been removed"
        else:
            evnt = ans
            if evnt_collection.count_documents({'event_start': f"{evnt}"}) == 0:
                retVal = f"I'm sorry, I could not find {evnt}"
                return retVal
            evnt_collection.delete_one({'event_name' : f"{evnt}"})
            retVal = f"{evnt} has been removed from your calendar"

    # another method for deleting an event based on another way a user may ask to delete an event
    elif "remove an event" in text:
        listen_speak.say("What event would you like to remove from your calendar?")
        ans = listen_speak.listen()
        if "on " in ans:
            Querydate = ans.split("on ", 1)[1]
            QuerydateDT = get_date(Querydate)
            QuerydateDT = datetime.datetime.combine(QuerydateDT, datetime.datetime.min.time())
            if evnt_collection.count_documents({'event_start': QuerydateDT}) == 0:
                retVal = f"I'm sorry, I could not find any event on {QuerydateDT}"
                return retVal
            if evnt_collection.count_documents({'event_start': QuerydateDT}) > 1:
                listen_speak.say("I found multiple events on that date, which one did you want to remove?")
                found_event = evnt_collection.find({'event_start': QuerydateDT})
                evnt_names = []
                for i in found_event:
                    #evntsDF = pandas.DataFrame(found_evnt)
                    print(i['event_name'])
                    evnt_names.append(i['event_name'])
                ans = listen_speak.listen()
                evntName_check = [name for name in evnt_names if(name in ans.lower())]
                if (len(evntName_check) > 0):
                    evntName_check = evntName_check.pop()
                #if evntName_check:
                    idx = evnt_names.index(evntName_check)
                else:
                    retVal = "I'm sorry, I couldn't find that event"
                    return retVal
                    
                evnt_collection.delete_one({'event_name' : f"{evnt_names[idx]}"})
                retVal = f"{evnt_names[idx]} on {QuerydateDT} has been removed"
                return retVal

            evnt_collection.delete_one({'event_start' : QuerydateDT})
            retVal = f"The even on {QuerydateDT} has been removed"
            

        elif "one " in ans:
            Querydate = ans.split("one ", 1)[1]
            QuerydateDT = get_date(Querydate)
            QuerydateDT = datetime.datetime.combine(QuerydateDT, datetime.datetime.min.time())
            if evnt_collection.count_documents({'event_start': QuerydateDT}) == 0:
                retVal = f"I'm sorry, I could not find any event on {QuerydateDT}"
                return retVal
            if evnt_collection.count_documents({'event_start': QuerydateDT}) > 1:
                listen_speak.say("I found multiple events on that date, which one did you want to remove?")
                found_event = evnt_collection.find({'event_start': QuerydateDT})
                evnt_names = []
                for i in found_event:
                    #evntsDF = pandas.DataFrame(found_evnt)
                    print(i['event_name'])
                    evnt_names.append(i['event_name'])
                ans = listen_speak.listen()
                evntName_check = [name for name in evnt_names if(name in ans.lower())]
                if (len(evntName_check) > 0):
                    evntName_check = evntName_check.pop()
                #if evntName_check:
                    idx = evnt_names.index(evntName_check)
                else:
                    retVal = "I'm sorry, I couldn't find that event"
                    return retVal
                    
                evnt_collection.delete_one({'event_name' : f"{evnt_names[idx]}"})
                retVal = f"{evnt_names[idx]} on {QuerydateDT} has been removed"
                return retVal

            evnt_collection.delete_one({'event_start' : QuerydateDT})
            retVal = f"The even on {QuerydateDT} has been removed"
            
        else:
            evnt = ans
            if evnt_collection.count_documents({'event_start': f"{evnt}"}) == 0:
                retVal = f"I'm sorry, I could not find {evnt}"
                return retVal
            evnt_collection.delete_one({'event_name' : f"{evnt}"})
            retVal = f"{evnt} has been removed from your calendar"

    
    # another method for deleting an event based on another way a user may ask to delete an event
    elif "remove" in text:
         if "on" in text:
            Querydate = text.split("on ", 1)[1]
            QuerydateDT = get_date(Querydate)
            QuerydateDT = datetime.datetime.combine(QuerydateDT, datetime.datetime.min.time())
            if evnt_collection.count_documents({'event_start': QuerydateDT}) == 0:
                retVal = f"I'm sorry, I could not find any event on {QuerydateDT}"
                return retVal
            if evnt_collection.count_documents({'event_start': QuerydateDT}) > 1:
                listen_speak.say("I found multiple events on that date, which one did you want to remove?")
                found_event = evnt_collection.find({'event_start': QuerydateDT})
                evnt_names = []
                for i in found_event:
                    #evntsDF = pandas.DataFrame(found_evnt)
                    print(i['event_name'])
                    evnt_names.append(i['event_name'])
                ans = listen_speak.listen()
                evntName_check = [name for name in evnt_names if(name in ans.lower())]
                if (len(evntName_check) > 0):
                    evntName_check = evntName_check.pop()
                #if evntName_check:
                    idx = evnt_names.index(evntName_check)
                else:
                    retVal = "I'm sorry, I couldn't find that event"
                    return retVal
                    
                evnt_collection.delete_one({'event_name' : f"{evnt_names[idx]}"})
                retVal = f"{evnt_names[idx]} on {QuerydateDT} has been removed"
                return retVal

            evnt_collection.delete_one({'event_start' : QuerydateDT})
            retVal = f"The even on {QuerydateDT} has been removed"
            
         else:                                                                      # another method for deleting an event based on another way a user may ask to delete an event (ex 'remove...{event}... from...')
             sub1 = "remove"
             sub2 = "from"
             idx1 = text.index(sub1)
             idx2 = text.rfind(sub2)
             evnt = text[idx1 + len(sub1) + 1 : idx2]
             # remove potential extra space at front and back of user response
             if evnt[0] == ' ':
                 evnt = evnt[1:]
             if evnt[-1] == ' ':
                 evnt = evnt[0:-1]

             if evnt_collection.count_documents({'event_start': f"{evnt}"}) == 0:
                retVal = f"I'm sorry, I could not find {evnt}"
                return retVal
             evnt_collection.delete_one({'event_name': f"{evnt}"})
             retVal = f"{evnt} has been removed from your calendar"

    # another method for deleting an event based on another way a user may ask to delete an event
    elif "take" in text:
         if "on" in text:
            Querydate = text.split("on ", 1)[1]
            QuerydateDT = get_date(Querydate)
            QuerydateDT = datetime.datetime.combine(QuerydateDT, datetime.datetime.min.time())
            if evnt_collection.count_documents({'event_start': QuerydateDT}) == 0:
                retVal = f"I'm sorry, I could not find any event on {QuerydateDT}"
                return retVal
            if evnt_collection.count_documents({'event_start': QuerydateDT}) > 1:
                listen_speak.say("I found multiple events on that date, which one did you want to remove?")
                found_event = evnt_collection.find({'event_start': QuerydateDT})
                evnt_names = []
                for i in found_event:
                    #evntsDF = pandas.DataFrame(found_evnt)
                    print(i['event_name'])
                    evnt_names.append(i['event_name'])
                ans = listen_speak.listen()
                evntName_check = [name for name in evnt_names if(name in ans.lower())]
                if (len(evntName_check) > 0):
                    evntName_check = evntName_check.pop()
                #if evntName_check:
                    idx = evnt_names.index(evntName_check)
                else:
                    retVal = "I'm sorry, I couldn't find that event"
                    return retVal
                    
                evnt_collection.delete_one({'event_name' : f"{evnt_names[idx]}"})
                retVal = f"{evnt_names[idx]} on {QuerydateDT} has been removed"
                return retVal

            evnt_collection.delete_one({'event_start' : QuerydateDT})
            retVal = f"The even on {QuerydateDT} has been removed"
            
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
             
             if evnt_collection.count_documents({'event_start': f"{evnt}"}) == 0:
                retVal = f"I'm sorry, I could not find {evnt}"
                return retVal
             evnt_collection.delete_one({'event_name': f"{evnt}"})
             retVal = f"{evnt} has been removed from your calendar"

    # another method for deleting an event based on another way a user may ask to delete an event
    elif "delete" in text:
         if "on" in text:
            Querydate = text.split("on ", 1)[1]
            QuerydateDT = get_date(Querydate)
            QuerydateDT = datetime.datetime.combine(QuerydateDT, datetime.datetime.min.time())
            if evnt_collection.count_documents({'event_start': QuerydateDT}) == 0:
                retVal = f"I'm sorry, I could not find any event on {QuerydateDT}"
                return retVal
            if evnt_collection.count_documents({'event_start': QuerydateDT}) > 1:
                listen_speak.say("I found multiple events on that date, which one did you want to remove?")
                found_event = evnt_collection.find({'event_start': QuerydateDT})
                evnt_names = []
                for i in found_event:
                    #evntsDF = pandas.DataFrame(found_evnt)
                    print(i['event_name'])
                    evnt_names.append(i['event_name'])
                ans = listen_speak.listen()
                evntName_check = [name for name in evnt_names if(name in ans.lower())]
                if (len(evntName_check) > 0):
                    evntName_check = evntName_check.pop()
                #if evntName_check:
                    idx = evnt_names.index(evntName_check)
                else:
                    retVal = "I'm sorry, I couldn't find that event"
                    return retVal
                    
                evnt_collection.delete_one({'event_name' : f"{evnt_names[idx]}"})
                retVal = f"{evnt_names[idx]} on {QuerydateDT} has been removed"
                return retVal

            evnt_collection.delete_one({'event_start' : QuerydateDT})
            retVal = f"The even on {QuerydateDT} has been removed"
            
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
             
             if evnt_collection.count_documents({'event_start': f"{evnt}"}) == 0:
                retVal = f"I'm sorry, I could not find {evnt}"
                return retVal
             evnt_collection.delete_one({'event_name': f"{evnt}"})
             retVal = f"{evnt} has been removed from your calendar"


        
    
     
    return retVal

# method for deleting all events on a specified date
def delete_ALLevents(text, indx):
    
    # conditional check for if user specified date
    if "on" in text:
        Querydate = text.split("on ", 1)[1]
    else:
        Querydate = text.split(f"{read_strs[indx]} ",1)[1]

    QuerydateDT = get_date(Querydate)
    QuerydateDT = datetime.datetime.combine(QuerydateDT, datetime.datetime.min.time()) #returns form year-month-day 00:00:00

    if evnt_collection.count_documents({'event_start': QuerydateDT}) == 0:
        retVal = f"There are no events on {QuerydateDT}"
        return retVal

    evnt_collection.delete_many({'event_start' : QuerydateDT})  # delete many method used for deleting multiple documents from database collection at once
    
    retVal = f"Okay, I have removed all events on {Querydate}" 
    return retVal
    
# method for converting a date into a datetime date object
def get_date(text):
    MONTHS = ["january", "february", "march", "april", "may", "june","july", "august", "september","october", "november", "december"] # list of month names
    DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]                                             # list of day names
    DAY_EXTENTIONS = ["rd", "th", "st", "nd"]                                                                                         # list of date number suffix

    text = text.lower()                 # make input lowercase to reduce case conflicts
    today = datetime.date.today()       # get today date from system time
    #today = datetime.datetime.today()

    if text.count("today") > 0:                     # if the user said today
        return today                                # return todays date as datetime date object
    elif text.count("tomorrow") > 0:                # if user said tomorrow
        tomorrow = today + datetime.timedelta(1)    # use timedelta which represents the difference betweeen 2 datetime objects to add 1 day to today
        return tomorrow                             # return tomorrow as a datetime object



    day = -1                 # default value for day
    day_of_week = -1         # default value for day of the week
    month = -1               # default value for month
    year = today.year        # default year is the current year

    for word in text.split():                   # loop through every word in user speech string
        if word in MONTHS:                      # if user said a month name set the value of month variable
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)      # if user said the name of a day of the week set day of the week variable
        elif word.isdigit():                    # check if the user said a number for the date
            day = int(word)                     # the day variable is set to the date number 
        else:                                   # if the number said has a suffix and is therefore not a digit
            for ext in DAY_EXTENTIONS:              # loop through each suffix in list
                found = word.find(ext)              # found gets the suffix from the user input that is matched in list
                if found > 0:                       # if suffix is found 
                    try:
                        day = int(word[:found])     # the day varible is assigned just the number the user said without the suffix by taking the user word up to but not including the found suffix
                    except:                         # if suffix not found / matched 
                        pass                        # pass is no code used to continue loop

    # check for error where no month and no day found
    if month != -1 and day == -1:
        listen_speak.say("I'm sorry, I did not catch the day of that event could you please repeat?")   # ask user to respecify day
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

    
    if month == -1 and day != -1:       # if we didn't find a month, but we have a day
        if day < today.day:             # if the date day number is before the current date day number assume next month otherwise current month
            month = today.month + 1
        else:
            month = today.month

    # if we only found a day of the week
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()               # set the current day of the week to today's weekday
        dif = day_of_week - current_day_of_week             # difference of the day of the week requested and today's weekday

        if dif < 0:                                         # if dif is less than 0 day of the week is for the next week
            dif += 7                
            if text.count("next") >= 1:                     # if user said next day of the week is on the next week
                dif += 7

        return today + datetime.timedelta(dif)              # add days to today using timedelta of the dif

    if day != -1:                                               # if have only a day the month and year is set as the current month and year
        return datetime.date(month=month, day=day, year=year)

