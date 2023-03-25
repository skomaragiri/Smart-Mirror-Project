import time 
import datetime
from time import strftime


def timeCheck(text):
    dt = datetime.datetime.now()
    if("date" in text):
        
        month_name = dt.strftime('%B')
        year = int(datetime.datetime.now().year)
        month = int(datetime.datetime.now().month)    #maybe move to time
        day = int(datetime.datetime.now().day)
        day_name = dt.strftime('%A')
        last_digit = str(day)[-1] 
        #print(f"{last_digit}")
        return f"Today is {day_name}. The date is: {month_name} {day} of, {year}."    

    else:
        hour = dt.strftime('%#H')
        minute = dt.strftime('%M')
        return f"It is currently {hour} : {minute}"
    
