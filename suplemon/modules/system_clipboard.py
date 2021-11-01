# -*- encoding: utf-8

import os
import subprocess
from platform import system

from suplemon.suplemon_module import Module


class SystemClipboard(Module):
    """Integrates the system clipboard with suplemon."""

    def init(self):
        self.init_logging(__name__)
        if (
        system() == 'Windows' and
        self.which("powershell")
        ):
            self.clipboard_type = "powershell"
        elif (
        system() == 'Linux' and
        self.which("powershell") and
        os.path.isfile('/proc/version')
        ):
            if "microsoft" in open('/proc/version', 'r').read().lower():
                self.clipboard_type = "powershell"
        elif (
        os.environ.get("WAYLAND_DISPLAY") and
        self.which("wl-copy")
        ):
            self.clipboard_type = "wl"
        elif self.which("xsel"):
            self.clipboard_type = "xsel"
        elif self.which("pbcopy"):
            self.clipboard_type = "pb"
        elif self.which("xclip"):
            self.clipboard_type = "xclip"
        elif self.which("termux-clipboard-get"):
            self.clipboard_type = "termux"
        else:
            self.logger.warning(
                "Can't use system clipboard. Install 'xsel' or 'pbcopy' or 'xclip' for system clipboard support.\nOn Termux, install 'termux-api' for system clipboard support.")
            return False
        self.bind_event_before("insert", self.insert)
        self.bind_event_after("copy", self.copy)
        self.bind_event_after("cut", self.copy)

    def copy(self, event):
        lines = self.app.get_editor().get_buffer()
        data = "\n".join([str(line) for line in lines])
        self.set_clipboard(data)

    def insert(self, event):
        data = self.get_clipboard()
        lines = data.split("\n")
        self.app.get_editor().set_buffer(lines)

    def get_clipboard(self):
        try:
            if self.clipboard_type == "powershell":
                command = ["powershell.exe", "-noprofile", "-command", "Get-Clipboard"]
            elif self.clipboard_type == "wl":
                command = ["wl-paste", "-n"]
            elif self.clipboard_type == "xsel":
                command = ["xsel", "-b"]
            elif self.clipboard_type == "pb":
                command = ["pbpaste", "-Prefer", "txt"]
            elif self.clipboard_type == "xclip":
                command = ["xclip", "-selection", "clipboard", "-out"]
            elif self.clipboard_type == "termux":
                command = ["termux-clipboard-get"]
            else:
                return False
            data = subprocess.check_output(command, universal_newlines=True)
            return data
        except:
            return False

    def set_clipboard(self, data):
        try:
            if self.clipboard_type == "powershell":
                command = ["powershell.exe", "-noprofile", "-command", "Set-Clipboard"]
            elif self.clipboard_type == "wl":
                command = ["wl-copy"]
            elif self.clipboard_type == "xsel":
                command = ["xsel", "-i", "-b"]
            elif self.clipboard_type == "pb":
                command = ["pbcopy"]
            elif self.clipboard_type == "xclip":
                command = ["xclip", "-selection", "clipboard", "-in"]
            elif self.clipboard_type == "termux":
                command = ["termux-clipboard-set"]
            else:
                return False
            p = subprocess.Popen(command, stdin=subprocess.PIPE)
            out, err = p.communicate(input=bytes(data, "utf-8"))
            return out
        except:
            return False

    def which(self, program): # https://stackoverflow.com/a/379535
        def is_exe(fpath):
            return os.path.exists(fpath) and os.access(fpath, os.X_OK) and os.path.isfile(fpath)

        def ext_candidates(fpath):
            yield fpath
            for ext in os.environ.get("PATHEXT", "").split(os.pathsep):
                yield fpath + ext

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                exe_file = os.path.join(path, program)
                for candidate in ext_candidates(exe_file):
                    if is_exe(candidate):
                        return candidate
        return False


module = {
    "class": SystemClipboard,
    "name": "system_clipboard",
}
