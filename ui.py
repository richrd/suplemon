"""
Curses user interface.
"""

import os
from helpers import *

# Force enabling colors
os.environ["TERM"] = "xterm-256color"
# Reduce ESC detection time to 50ms
os.environ["ESCDELAY"] = "50"
# Now import curses
import curses
import curses.textpad

class UI:
    def __init__(self):
        self.screen = curses.initscr()
        self.setup_colors()

        curses.cbreak()
        curses.noecho()
        curses.curs_set(0)
        self.screen.keypad(1)

        self.current_yx = self.screen.getmaxyx() # For checking resize
        self.setup_windows()

    def setup_colors(self):
        """Initialize color support and define colors."""
        curses.start_color()
        curses.use_default_colors()

        if curses.can_change_color(): # Can't get these to work :(
            #curses.init_color(11, 254, 0, 1000)
            pass

        # This only works with: TERM=xterm-256color
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLUE)
        curses.init_pair(4, curses.COLOR_WHITE, -1)

        # Higlight colors:
        black = curses.COLOR_BLACK
        curses.init_pair(10, -1, -1) # Default (white on black)

        curses.init_pair(11, curses.COLOR_BLUE, black)
        curses.init_pair(12, curses.COLOR_CYAN, black)
        curses.init_pair(13, curses.COLOR_GREEN, black)
        curses.init_pair(14, curses.COLOR_MAGENTA, black)
        curses.init_pair(15, curses.COLOR_RED, black)
        curses.init_pair(17, curses.COLOR_YELLOW, black)
        curses.init_pair(16, curses.COLOR_WHITE, black)

        # Better colors
        try:
            # TODO: Define RGB forthese to avoid getting different results
            curses.init_pair(11, 69, black) # blue
            curses.init_pair(12, 81, black) # cyan
            curses.init_pair(13, 119, black) # green
            curses.init_pair(14, 171, black) # magenta
            curses.init_pair(15, 197, black) # red
            curses.init_pair(17, 221, black) # yellow
        except:
            self.logger.log("Enhanced colors failed to load.")

    def setup_windows(self, resize=False):
        """Initialize windows."""
        yx = self.screen.getmaxyx()
        self.text_input = None
        self.header_win = curses.newwin(1, yx[1], 0, 0)
        self.status_win = curses.newwin(1, yx[1], yx[0]-1, 0)
        y_sub = 0
        y_start = 0
        if self.config["display"]["show_top_bar"]:
            y_sub += 1
            y_start = 1
        if self.config["display"]["show_bottom_bar"]:
            y_sub += 1
        if self.config["display"]["show_legend"]:
            y_sub += 2
        self.editor_win = curses.newwin(yx[0]-y_sub, yx[1], y_start, 0)
        self.legend_win = curses.newwin(2, yx[1], yx[0]-y_sub+1, 0)

        if resize:
            self.editor().resize( (yx[0]-y_sub, yx[1]) )
            self.editor().move_win( (y_start, 0) )

    def resize(self, yx=None):
        """Resize UI to yx."""
        if yx == None:
            yx = self.screen.getmaxyx()
        self.screen.clear()
        curses.resizeterm(yx[0], yx[1])
        self.setup_windows(resize = True)
        self.screen.refresh()
        
    def max_editor_height(self):
        """Get maximum height of editor window."""
        d = self.config["display"]
        subtract = int(d["show_top_bar"]) + int(d["show_bottom_bar"]) + [0,2][d["show_legend"]]
        return self.size()[1] - subtract

    def check_resize(self):
        """Check if terminal has resized."""
        yx = self.screen.getmaxyx()
        if self.current_yx != yx:
            self.current_yx = yx
            self.resize(yx)

    def size(self):
        """Get terminal size."""
        y, x = self.screen.getmaxyx()
        return (x, y)

    def _query(self, text, initial=""):
        """Ask for text input via the status bar."""
        self.show_capture_status(text, initial)
        self.text_input = curses.textpad.Textbox(self.status_win)
        try:
            out = self.text_input.edit()
        except:
            return False

        # If input begins with prompt, remove the prompt text
        if len(out) >= len(text):
           if out[:len(text)] == text:
                out = out[len(text):]
        if len(out) > 0 and out[-1] == " ": out = out[:-1]
        out = out.rstrip("\r\n")
        return out

    def query(self, text, initial=""):
        result = self._query(text, initial)
        return result

    def query_bool(self, text, default = False):
        indicator = "[y/N]"
        initial = ""
        if default:
            indicator = "[Y/n]"
            initial = "y"
        
        result = self._query(text + " " + indicator, initial)
        if result in ["Y", "y"]:
            return True
        if result == "":
            return default
        return False

    def show_top_status(self):
        """Show top status row."""
        self.header_win.clear()
        size = self.size()
        display = self.config["display"]
        head_parts = []
        if display["show_app_name"]:
            head_parts.append("Suplemon Editor v"+self.version)
        if display["show_clock"]:
            head_parts.append(curr_time())
        if display["show_file_list"]:
            head_parts.append(self.file_list_str())

        head = " - ".join(head_parts)
        head = head + ( " " * (self.screen.getmaxyx()[1]-len(head)-1) )
        if len(head) >= size[0]:
            head = head[:size[0]-1]
        self.header_win.addstr(0,0, head, curses.color_pair(0) | curses.A_REVERSE)
        self.header_win.refresh()
        
    def file_list_str(self):
        """Return rotated file that begins at current file."""
        file_list = self.files[self.current_file:] + self.files[:self.current_file]
        str_list = []
        for f in file_list:
            fname = f.name + (["", "*"][f.is_changed()])
            if not str_list:
                str_list.append("[" + fname + "]")
            else:
                str_list.append(fname)
        return " ".join(str_list)

    def show_bottom_status(self):
        """Show bottom status row."""
        # FIXME: Seems to write to max_y+1 line and crash
        editor = self.editor()
        size = self.size()
        cur = editor.cursor()
        data = "@ "+str(cur[0])+","+str(cur[1])+" "+\
            "cur:"+str(len(editor.cursors))+" "+\
            "buf:"+str(len(editor.buffer))
        if self.config["display"]["show_last_key"]:
            data += " key:"+str(self.last_key)
        if self.config["display"]["show_term_size"]:
            data += " ["+str(size[0])+"x"+str(size[1])+"]"
        if self.config["app"]["debug"]:
            data += " cs:"+str(editor.current_state)+" hist:"+str(len(editor.history))  # Undo / Redo debug
        if editor.last_find:
            find = editor.last_find
            if len(find) > 10:find = find[:10]+"..."
            data = "find:'"+find+"' " + data
        self.status_win.clear()
        status = self.status_msg
        extra = size[0] - len(status+data) - 1
        line = status+(" "*extra)+data

        if len(line) >= size[0]:
            line = line[:size[0]-1]

        self.status_win.addstr(0,0, line, curses.color_pair(0) | curses.A_REVERSE)
        self.status_win.refresh()
        
    def show_legend(self):
        """Show keyboard legend."""
        self.legend_win.clear()
        keys = [
            ("F1", "Save"),
            ("F2", "Reload"),
            ("^O", "Open"),
            ("^X", "Cut"),
            ("^V", "Paste"),
            ("^F", "Find"),
            ("^D", "Find next"),
            ("^A", "Find all"),
            ("^W", "Duplicate line"),
            ("ESC", "Single cursor"),
            ("^G", "Go to"),
            ("^C", "Exit"),
        ]
        x = 0
        y = 0
        max_y = 1
        for key in keys:
            if x+len(" ".join(key)) >= self.size()[0]:
                x = 0
                y += 1
                if y > max_y:
                    break
            self.legend_win.addstr(y, x, key[0], curses.A_REVERSE)
            x += len(key[0])
            self.legend_win.addstr(y, x, " "+key[1])
            x += len(key[1])+2
        self.legend_win.refresh()

    def show_capture_status(self, s="", value=""):
        """Show status when capturing input."""
        self.status_win.clear()
        self.status_win.addstr(0, 0, s, curses.A_REVERSE)
        self.status_win.addstr(0, len(s), value)
        self.status_win.refresh()

    def refresh_status(self):
        """Refresh status windows."""
        if not self.inited: 
            return False
        if self.config["display"]["show_top_bar"]:
            self.show_top_status()
        if self.capturing:
            self.show_capture_status()
        if self.config["display"]["show_legend"]:
            self.show_legend()
        if self.config["display"]["show_bottom_bar"]:
            self.show_bottom_status()
