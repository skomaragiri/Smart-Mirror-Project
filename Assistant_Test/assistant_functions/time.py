from datetime import datetime

def timeCheck():
    time_now = datetime.now
    current_hour = time_now.strftime("%H")
    current_min = time_now.strftime("%M")
    return f"It is currently {current_hour} {current_min}"
