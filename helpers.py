import sys
import time
import traceback

def curr_time():
    return time.strftime("%H:%M")
    
def curr_time_sec():
    return time.strftime("%H:%M:%S")

def starts(s, what):
    if type(what) == type(""):
        what = [what]
    for item in what:
        if s.find(item) == 0:
            return True
    return False

# return info about last error
def get_error_info():
    msg = str(traceback.format_exc()) + "\n" + str(sys.exc_info())
    return msg

# Get a substring of a string with two delimeters
def get_string_between(start, stop, s):
        i1 = s.find(start)
        if i1 == -1:
            return False
        s = s[i1 + len(start):]
        i2 = s.find(stop)
        if i2 == -1:
            return False
        s = s[:i2]
        return s