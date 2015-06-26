import time

from mod_base import *
 
class Clock(Command):
    def get_status(self):
        s = time.strftime("%H:%M")
        if self.app.config["app"]["use_unicode_symbols"]:
            return "\u231A" + s
        return s

module = {
    "class": Clock,
    "name": "clock",
    "status": "top",
}
