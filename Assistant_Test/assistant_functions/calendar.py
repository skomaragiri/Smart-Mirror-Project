from datetime import date

def date():
    date_now = datetime.now
    current_year = strftime("%Y")
    current_month = strftime("%B")
    current_day = strftime("%A")
    day_date = strftime("%d")
    return f"Today is {current_day} the {day_date} of {current_month}, {current_year}."
