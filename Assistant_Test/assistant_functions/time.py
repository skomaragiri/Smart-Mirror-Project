import time 
import datetime
from time import strftime


def timeCheck(text):
    dt = datetime.datetime.now()                                                            # get current time from system
    if("date" in text):                                                                     # if the word date was in user speech input give the date
        
        month_name = dt.strftime('%B')                                                      # get the full month name as a string
        year = int(datetime.datetime.now().year)                                            # get the year
        month = int(datetime.datetime.now().month)                                          # get the month number 
        day = int(datetime.datetime.now().day)                                              # get the day
        day_name = dt.strftime('%A')                                                        # get the full day name
        #last_digit = str(day)[-1] 
        
        return f"Today is {day_name}. The date is: {month_name} {day} of, {year}."          # return string to speak date to user

    else:                                                                                   # if date was not asked for give the user the current time
        hour = dt.strftime('%#H')                                                           # get time hour
        minute = dt.strftime('%M')                                                          # get time minutes
        return f"It is currently {hour} : {minute}"                                         # return string to speak time to user 
    
