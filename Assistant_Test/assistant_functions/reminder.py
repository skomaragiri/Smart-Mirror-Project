import pyttsx3
import speech_recognition as sr
import random

def remind(request):
    voice = pyttsx3.init()
#    wlines = ("What should I remind you of?", "what did you not want to forget?", "what can I help you remember?", "what did you want to add to your reminders?")
#    rlines = ("Here is your reminders", "this is what you wanted to remember", "You told me to remind you about these things")
#    clrlines = (f"{} has been removed from your reminders", "okay, I have removed {} from your reminders", "{} has been removed")

    RdResponse = ("Here are your reminders", "This is your list of reminders", "Here's what you wanted to remember")    # tuple for assistant response strings for use with say method
    

    def wr(line):   # write method for adding to the reminders list txt document
        #write func
        wline = line                                    # assign user input to variable
        
        # conditional checks for isolating the reminder from the full user input string to be added to the reminders list
        if 'remind me to' in wline:
            # splits full input string after 'to' 1 time and puts result into a list where index 0 is up to and including the word of split and index 1 is the string after the split word so take only index 1 into result variable res
            res = (wline.split('to', 1))[1]             
        elif 'remind me that' in wline:
            res = (wline.split('that', 1))[1]
        elif 'remember' in wline:
            res = (wline.split('remember', 1))[1]
        elif 'remind me' in wline:                                   
            res = (wline.split('me', 1))[1]
        elif 'about' in wline:
            res = (wline.split('about', 1))[1]                      
        elif 'forget to' in wline:
            res = (wline.split('to', 1))[1]
        elif 'forget that' in wline:
            res = (wline.split('that', 1))[1]
        elif 'forget' in wline:
            res = (wline.split('forget', 1))[1]
        # isolate reminder in between 'add' and 'to'
        elif 'add' in wline:
            sub1 = 'add'
            sub2 = 'to'
            idx1 = wline.index(sub1)    # index of add
            idx2 = wline.rfind(sub2)    # index of to
            res = wline[idx1 + len(sub1) + 1 : idx2] # res is everything in the string after add but before to
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
        else:                                                   # could not understand what the user wanted to be added
            return "I am sorry I did not understand"

        with open('RemindersList.txt', 'a') as f:               # open the RemindersList text file as f (a character variable to be used when referring to the file) using the append ('a') method to add information without wiping current data
            # remove potential white space at beginning and end of data user wants added
            if res[0] == ' ':
                res = res[1:]
            if res[-1] == ' ':
                res = res[0:-1]
            f.write(f"{res}\n")     # write reminder to file
            f.close()               # close file

        return f"{res} was added to your reminders\n"   # notify user that reminder was added

    # method for reading the text file so user can see reminders on list
    def rd():
        with open('RemindersList.txt', 'r') as f:   # open file using read ('r') method
            fl = f.read()                           # fl gets contents of text file
            print(fl)                               # print contents
            f.close()                               # close file
        
        return random.choice(RdResponse)            # notify user with random response from tuple

    # method for removing items from text file
    def clr(line):
        rmvline = line                  # user input assigned to variable as the line to be removed
        clear_flag = False              # default state of variable flag for clearing all contents of file set to false
        delete_line_flag = False        # default state of variable flag for deleting lines of file set to false 

        # conditionals to isolate the line to be removed from the file from the larger user input string
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
        elif 'clear' in rmvline:                                # if user wants to clear the file
            clear_flag = True                                   # set the clear flag
            delete = open('RemindersList.txt', 'w')             # open the text file with the write method to clear its contents
            delete.close()                                      # close the file
        else:
            return "I am sorry, I did not understand"

        
        
        if (delete_line_flag == True):                          # if flag set to delete a line
            with open('RemindersList.txt', 'r') as f:           # open the text file with read method 
                inputLines = f.readlines()                      # read all contents of file into variable inputlines
                lineIndex = 1                                   # variable that acts as a pointer to the line in the file 
                with open('RemindersList.txt', 'w') as f:       # Open the file as write ('w') to clear contents of file
                    for textline in inputLines:                 # loop through each line read from the file into inputlines
                        if (textline[0] == ' '):                # remove potential extra space at beginning and end of each line to avoid conflict with lines to be remoed not matching
                            textline = textline[1:]
                        if (textline[-1] == ' '):
                            textline = textline[0:-1]
                        if res not in textline:                 # if the line that is desired to be removed is not the text line being looked at by the loop
                            f.write(textline)                   # rewrite that line back into the textfile otherwise the line is not written back to the textfile effectively deleting the line
                            lineIndex += 1                      # increase the pointer to the next line in the file 
            f.close()                                           # close the file

        if clear_flag:                                                      # if the clear flag was set inform user that file was cleared
            print("Reminders Cleared")
            return f"I have cleared your reminders"
        else:                                                               # otherwise inform user of line that was cleared
            print(f"{res} has been removed from your list of reminders")
            return f"{res} has been removed from your list of reminders"


    # Conditional checks to determine what the user wants to do: add, read, or delete based on a key word in input string
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

    
