import time
from mod_base import *
 
class Clock(Command):
    def get_status(self):
        s = time.strftime("%H:%M")
        return s

module = {
    "class": Clock,
    "name": "clock",
    "status": "top",
}
