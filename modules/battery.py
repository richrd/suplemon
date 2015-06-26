import os
import time
import subprocess

from mod_base import *
 
class Battery(Command):
    def init(self):
        self.last_value = -1
        self.checked = time.time()
        self.interval = 10

    def value(self):
        """Get the battery charge percent and cache it."""
        if self.last_value == -1:
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
        value = None
        methods = [
            self.battery_status_read,
            self.battery_status_acpi,
            self.battery_status_upower
        ]
        for m in methods:
            value = m()
            if value != None:
                break
        return value
        
    def battery_status_read(self):
        """Get the battery status via proc/acpi."""
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
        """Get the battery status via acpi."""
        try:
            raw_str = subprocess.check_output(["acpi"])
        except:
            return None
        raw_str = raw_str.decode("utf-8")
        part = get_string_between(",", "%", raw_str)
        if part:
            try:
                return int(part)
            except:
                return None
        return None

    def battery_status_upower(self):
        """Get the battery status via upower."""
        try:
            raw_str = subprocess.check_output(["upower", "-i", "/org/freedesktop/UPower/devices/battery_BAT0"])
        except:
            return None
        raw_str = raw_str.decode("utf-8")
        part = get_string_between("percentage:", "%", raw_str)
        if part:
            try:
                return int(part)
            except:
                return None
        return None

    def readf(self, path):
        """Read and return file contents at path."""
        f = open(path)
        data = f.read()
        f.close()
        return data
 
module = {
    "class": Battery,
    "name": "battery",
    "status": "top",
}
