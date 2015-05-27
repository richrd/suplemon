import os
import time

from mod_base import *
 
class Battery(Command):
    def init(self):
        self.last_value = None
        self.checked = time.time()
        self.interval = 30

    def value(self):
        """Get the battery charge percent and cache it."""
        if self.last_value == None:
            state = self.battery_status()
        elif time.time()-self.checked > self.interval:
            state = self.battery_status()
        else:
            return self.last_value
        self.last_value = state
        return state

    def value_str(self):
        """Return formatted value string to show in the UI."""
        val = self.value()
        if val:
            if self.app.config["app"]["use_unicode_symbols"]:
                return "\u26A1" + str(val) + "%"
            else:
                return "BAT " + str(val) + "%"
        return ""

    def get_status(self):
        """Called by app when showing status bar contents."""
        return self.value_str()

    def battery_status(self):
        """Attempts to get the battery charge percent."""
        val = self.battery_status_read()
        if val != None:
            return val
        else:
            val = self.battery_status_acpi()
        return val
        
    def battery_status_read(self):
        try:
            path_info = self.readf("/proc/acpi/battery/BAT0/info")
            path_state = self.readf("/proc/acpi/battery/BAT0/state")
        except:
            return None
        try:
            max_cap = float( get_string_between("last full capacity:", "mWh", path_info) )
            cur_cap = float( get_string_between("remaining capacity:", "mWh", path_state) )
            return int(cur_cap / max_cap * 100)
        except:
            return None

    def battery_status_acpi(self):
        try:
            raw_str = os.popen("acpi").read()
        except:
            return None
        part = get_string_between(",", "%", raw_str)
        return int(part)

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
