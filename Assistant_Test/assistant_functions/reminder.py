import pyttsx3
import speech_recognition as sr
import random

def remind(request):
    voice = pyttsx3.init()
#    wlines = ("What should I remind you of?", "what did you not want to forget?", "what can I help you remember?", "what did you want to add to your reminders?")
#    rlines = ("Here is your reminders", "this is what you wanted to remember", "You told me to remind you about these things")
#    clrlines = (f"{} has been removed from your reminders", "okay, I have removed {} from your reminders", "{} has been removed")

    RdResponse = ("Here are your reminders", "This is your list of reminders", "Here's what you wanted to remember")
    

    def wr(line):
        #write func
        wline = line
        
        if 'remind me to' in wline:
            res = (wline.split('to', 1))[1]
        elif 'remind me that' in wline:
            res = (wline.split('that', 1))[1]
        elif 'remember' in wline:
            res = (wline.split('remember', 1))[1]
        elif 'remind me' in wline:                                  # small bugs with this one where saying "I have hw due" = calander  
            res = (wline.split('me', 1))[1]
        elif 'about' in wline:
            res = (wline.split('about', 1))[1]                      # bug = interpreted as internet intent
        elif 'forget to' in wline:
            res = (wline.split('to', 1))[1]
        elif 'forget that' in wline:
            res = (wline.split('that', 1))[1]
        elif 'forget' in wline:
            res = (wline.split('forget', 1))[1]
        elif 'add' in wline:
            sub1 = 'add'
            sub2 = 'to'
            idx1 = wline.index(sub1)
            idx2 = wline.rfind(sub2)
            res = wline[idx1 + len(sub1) + 1 : idx2]
        elif 'put' in wline:
            sub1 = 'put'
            if "on " in wline:
                sub2 = 'on'
            elif "in " in wline:
                sub2 = 'in'
            
            idx1 = wline.index(sub1)
            idx2 = wline.rfind(sub2)
            res = wline[idx1 + len(sub1) + 1 : idx2]
#            for idx in range(idx1 + len(sub1) + 1, idx2):
#                res = res + wline[idx]
        else:
            return "I am sorry I did not understand"

        with open('RemindersList.txt', 'a') as f:
            if res[0] == ' ':
                res = res[1:]
            if res[-1] == ' ':
                res = res[0:-1]
            f.write(f"{res}\n")
            f.close()

        return f"{res} was added to your reminders\n"

    def rd():
        with open('RemindersList.txt', 'r') as f:
            fl = f.read()
            print(fl)
            f.close()
        
        return random.choice(RdResponse)

    def clr(line):
        rmvline = line
        clear_flag = False
        delete_line_flag = False


        if 'remove' in rmvline:
            sub1 = 'remove'
            sub2 = 'from'
            idx1 = rmvline.index(sub1)
            idx2 = rmvline.rfind(sub2)
            res = rmvline[idx1 + len(sub1) + 1 : idx2]
            if res[0] == ' ':
                res = res[1:]
            if res[-1] == ' ':
                res = res[0:-1]
            delete_line_flag = True
        elif 'take' in rmvline:
            sub1 = 'take'
            sub2 = 'off'
            idx1 = rmvline.index(sub1)
            idx2 = rmvline.rfind(sub2)
            res = rmvline[idx1 + len(sub1) + 1 : idx2]
            if res[0] == ' ':
                res = res[1:]
            if res[-1] == ' ':
                res = res[0:-1]
            delete_line_flag = True
        elif 'clear' in rmvline:
            clear_flag = True
            delete = open('RemindersList.txt', 'w')
            delete.close()
        else:
            return "I am sorry, I did not understand"

        

        if (delete_line_flag == True):
            with open('RemindersList.txt', 'r') as f:
                inputLines = f.readlines()
                lineIndex = 1
                with open('RemindersList.txt', 'w') as f:
                    for textline in inputLines:
                        if (textline[0] == ' '):
                            textline = textline[1:]
                        if (textline[-1] == ' '):
                            textline = textline[0:-1]
                        if res not in textline:
                            f.write(textline)
                            lineIndex += 1
            f.close()
        if clear_flag:
            print("Reminders Cleared")
            return f"I have cleared your reminders"
        else:
            print(f"{res} has been removed from your list of reminders")
            return f"{res} has been removed from your list of reminders"


    #or "remind me" or "forget" or "put"
    if "add" in request:
        rmndr = wr(request)
        return rmndr

    elif "forget" in request:
        rmndr = wr(request)
        return rmndr

    elif "remember" in request:
        rmndr = wr(request)
        return rmndr

    elif "remind me" in request:
        rmndr = wr(request)
        return rmndr

    elif "put" in request:
        rmndr = wr(request)
        return rmndr

    elif "what" in request:
        rmndr = rd()
        return rmndr

    elif "tell me" in request:
        rmndr = rd()
        return rmndr

    elif "display" in request:
        rmndr = rd()
        return rmndr

    elif "show" in request:
        rmndr = rd()
        return rmndr

    elif "remove" in request:
        rmndr = clr(request)
        return rmndr

    elif "off" in request:
        rmndr = clr(request)
        return rmndr

    elif "clear" in request:
        rmndr = clr(request)
        return rmndr

    else:
        return f"could not understand"

    
