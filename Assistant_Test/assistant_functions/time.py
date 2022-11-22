import time 
import datetime
from time import strftime


def timeCheck():
    tm = datetime.datetime.now()
    hour = tm.strftime('%#H')
    #if(hour[0] == 0):
        
    minute = tm.strftime('%M')
    #hour = int(datetime.datetime.now().second)
    print(f"It is currently {hour} {minute}")
    return f"It is currently {hour} {minute}"
