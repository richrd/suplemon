import time
from mod_base import *
 
class Clock(Command):
    def __init__(self):
        pass

    def get_status(self):
        return time.strftime("%H:%M")
 
module = {
    "class": Clock,
    "name": "clock",
    "status": "top",
}
