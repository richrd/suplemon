import time
from mod_base import *
 
class Battery(Command):
    def __init__(self):
        self.last_value = None
        self.checked = time.time()
        self.interval = 10

    def value(self):
        if not self.last_value:
            state = self.battery_status()
        elif time.time()-self.checked > self.interval:
            state = self.battery_status()
        else:
            return self.last_value
        self.last_value = state
        return state

    def value_str(self):
        val = self.value()
        if val:
            return "BAT " + str(val) + "%"
        return ""

    def get_status(self):
        return self.value_str()

    def battery_status(self):
        try:
            path_info = self.readf("/proc/acpi/battery/BAT0/info")
            path_state = self.readf("/proc/acpi/battery/BAT0/state")
        except:
            return False
        try:
            max_cap = float( get_string_between("last full capacity:", "mWh", path_info) )
            cur_cap = float( get_string_between("remaining capacity:", "mWh", path_state) )
            return int(cur_cap / max_cap * 100)
        except:
            return False

    def readf(self, path):
        f = open(path)
        data = f.read()
        f.close()
        return data
 
module = {
    "class": Battery,
    "name": "battery",
    "status": "top",
}
