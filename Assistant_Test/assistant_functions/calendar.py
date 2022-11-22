import time 
import datetime
from time import strftime

def date():
    dt = datetime.datetime.now()
    month_name = dt.strftime('%B')
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    day_name = dt.strftime('%A')
    last_digit = str(day)[-1] 
    #print(f"{last_digit}")
  

    
    return f"Today is {day_name}. The date is: {month_name} {day} of, {year}."
