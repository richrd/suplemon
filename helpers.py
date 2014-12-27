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