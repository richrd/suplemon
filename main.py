#!/usr/bin/python
#-*- coding:utf-8

__version__ = "0.0.1"

import os
import sys
import time
import curses
import curses.textpad

from logger import *
from config import *
from editor import *
from helpers import *

quick_help = """
Welcome to suplemon!
====================

Usage: ```python main.py [filename]```


Warning: beta software, bugs may occur.

# Keyboard shortcuts:

 * Alt + Arrow Keys
   > Add new curors in arrow direction

 * Ctrl + Left / Right
   > Jump to previous or next word

 * ESC
   > Revert to a single cursor

 * Ctrl + X
   > Cut line(s) to buffer

 * Insert
   > Insert buffer

 * Ctrl + G
   > Go to line number

 * Ctrl + F
   > Find text

 * Ctrl + D
   > Add a new cursor at the next occurance

 * Alt + Page Up
   > Move line(s) up

 * Alt + Page Down
   > Move line(s) down

 * F1
   > Save current file

 * F2
   > Reload current file

 * F9
   > Toggle line numbers

"""

class File:
    def __init__(self):
        self.name = ""
        self.fpath = ""
        self.data = None
        self.read_only = False
        self.last_save = None
        self.opened = time.time()
        self.editor = None

    def _path(self):
        return os.path.join(self.fpath, self.name)

    def path(self):
        return self._path()

    def log(self, s):
        app.logger.log(s)

    def set_data(self, data):
        self.data = data
        if self.editor:
            self.editor.set_data(data)
        
    def set_path(self, path):
        ab = os.path.abspath(path)
        self.fpath, self.name = os.path.split(ab)
        
    def set_editor(self, editor):
        self.editor = editor

    def set_saved(self, m):
         self.last_save = time.time()

    def save(self):
        path = self._path()
        data = self.editor.get_data()
        try:
            f = open(self._path(), "w")
            f.write(data)
            f.close()
        except:
            return False
        self.data = data
        self.last_save = time.time()
        return True

    def load(self):
        path = self._path()
        try:
            f = open(self._path())
            data = f.read()
            f.close()
        except:
            return False
        self.data = data
        self.editor.set_data(data)
        return True

    def reload(self):
        return self.load()
        
    def is_changed(self):
        return self.editor.get_data() != self.data

class App:
    def __init__(self):
        self.version = __version__
        self.inited = 0
        self.running = 0
        self.last_key = None
        self.status_msg = ""
        self.capturing = 0

        self.files = []
        self.current_file = 0

        self.logger = Logger()
        self.config = Config(self)
        self.config.load()

        self.screen = curses.initscr()
        self.setup_colors()

        curses.cbreak()
        curses.noecho()
        curses.curs_set(0)
        self.screen.keypad(1)
        # Mouse mode kills scroll wheel...
        #curses.mousemask(curses.BUTTON1_CLICKED)

        self.current_yx = self.screen.getmaxyx() # For checking resize
        self.setup_windows()
        self.inited = 1 # Indicate that windows etc. have been created.

    def setup_colors(self):
        curses.start_color()
        curses.use_default_colors()

        if curses.can_change_color(): # Can't get these to work :(
            #curses.init_color(11, 254, 0, 1000)
            pass

        # This only works with: TERM=xterm-256color ./main.py
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
            curses.init_pair(11, 69, black) # blue
            curses.init_pair(12, 81, black) # cyan
            curses.init_pair(13, 119, black) # green
            curses.init_pair(14, 171, black) # magenta
            curses.init_pair(15, 197, black) # red
            curses.init_pair(17, 221, black) # yellow
            # curses.init_pair(17, 202, curses.COLOR_BLACK) #orange
        except:
            self.logger.log("Better colors failed to load.")

    def setup_windows(self, resize=False):
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
        self.editor_win = curses.newwin(yx[0]-y_sub-1, yx[1], y_start, 0)
        self.legend_win = curses.newwin(2, yx[1], yx[0]-y_sub+1, 0)

        if resize:
            self.editor().resize( (yx[0]-y_sub, yx[1]) )
            self.editor().move_win( (y_start, 0) )

    def reload_config(self):
        self.config.reload()
        for f in self.files:
            self.setup_editor(f.editor)
        
        self.resize()
        self.refresh()

    def max_editor_height(self):
        d = self.config["display"]
        subtract = int(d["show_top_bar"]) + int(d["show_bottom_bar"]) + [0,2][d["show_legend"]]
        return self.size()[1] - subtract

    def log(self, s):
        self.logger.log(s)
        self.parent.status(s)

    def size(self):
        y, x = self.screen.getmaxyx()
        return (x, y)

    def resize(self, yx=None):
        if yx == None:
            yx = self.screen.getmaxyx()
        self.screen.clear()
        curses.resizeterm(yx[0], yx[1])
        self.setup_windows(resize = True)
        self.screen.refresh()

    def check_resize(self):
        yx = self.screen.getmaxyx()
        if self.current_yx != yx:
            self.current_yx = yx
            self.resize(yx)

    def refresh(self):
        self.editor().render()
        self.refresh_status()
        self.screen.refresh()

    def status(self, s):
        self.status_msg = s
        self.refresh_status()

    def file(self):
        return self.files[self.current_file]

    def file_exists(self, path):
        for file in self.files:
            if file.path() == os.path.abspath(path):
                return file
        return False

    def find_file(self, s):
        i = 0
        for file in self.files:
            if file.name[:len(s)] == s:
                return i
            i += 1
        return -1

    def editor(self):
        return self.files[self.current_file].editor

    def setup_editor(self, editor):
        ed = self.config["editor"]
        editor.set_tab_width(ed["tab_width"])
        editor.set_cursor(ed["cursor"])
        editor.set_punctuation(ed["punctuation"])
        
        display = self.config["display"]
        editor.show_line_colors = display["show_line_colors"]
        editor.show_line_nums = display["show_line_nums"]
        editor.line_end_char = display["line_end_char"]
        
    def new_editor(self):
        editor = Editor(self, self.editor_win)
        self.setup_editor(editor)
        return editor

    def query(self, text):
        self.show_capture_status(text)
        self.text_input = curses.textpad.Textbox(self.status_win)
        try:
            out = self.text_input.edit()
        except:
            return -1

        # If input begins with prompt, remove the prompt text
        if len(out) >= len(text):
           if out[:len(text)] == text:
                out = out[len(text):]
        if len(out) > 0 and out[-1] == " ": out = out[:-1]
        out = out.rstrip("\r\n")
        return out

    def show_top_status(self):
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
        # Rotate file list to begin at current file
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
        # FIXME: Seems to write to max_y+1 line and crash
        editor = self.editor()
        size = self.size()
        cur = editor.cursor()
        data = "@ "+str(cur[0])+","+str(cur[1])+" "+\
            "cur:"+str(len(editor.cursors))+" "+\
            "buf:"+str(len(editor.buffer))+""

        if self.config["display"]["show_last_key"]:
            data += " key:"+str(self.last_key)
        if self.config["display"]["show_term_size"]:
            data += " ["+str(size[0])+"x"+str(size[1])+"]"

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

    def show_capture_status(self, s=""):
        self.status_win.clear()
        self.status_win.addstr(0, 0, s, curses.color_pair(1))
        self.status_win.refresh()

    def show_legend(self):
        self.legend_win.clear()
        keys = [
            ("F1", "Save"),
            ("F2", "Reload"),
            ("^O", "Open"),
            ("^F", "Find next"),
            ("^X", "Cut"),
            ("INS", "Paste"),
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

    def refresh_status(self):
        if not self.inited: return False
        if self.config["display"]["show_top_bar"]:
            self.show_top_status()
        if self.capturing:
            self.show_capture_status()
        if self.config["display"]["show_legend"]:
            self.show_legend()
        if self.config["display"]["show_bottom_bar"]:
            self.show_bottom_status()

    def open(self):
        name = self.query("Open:")
        if not name or name == -1:
            return False
        exists = self.file_exists(name)
        if exists:
            self.switch_to_file(self.files.index(exists))
            return True

        if not self.open_file(name):
            self.status("Failed to load '"+name+"'")
            return False
        self.switch_to_file(self.last_file())
        return True

    def open_file(self, filename, new = False):
        result = ""
        file = File()
        file.set_path(filename)
        file.set_editor(self.new_editor())
        loaded = file.load()
        if not loaded and not new:
            return False
        self.files.append(file)
        return loaded

    def load(self):
        loaded = True
        if len(sys.argv) > 1:
            names = sys.argv[1:]
            for name in names:
                if self.file_exists(name): continue
                if self.open_file(name):
                    loaded = True
                else:
                    self.open_file(name, new=True)
        else:
            self.load_default()
        
    def save(self):
        fi = self.file()
        if fi.save():
            self.status("Saved [" + curr_time_sec() + "] '" + fi.name + "'")
            if fi.path() == self.config.path():
                self.reload_config()
            return True
        self.status("Couldn't write to '" + fi.name + "'")
        return False

    def load_default(self):
        file = self.default_file()
        file.set_data(quick_help)
        self.files.append(file)

    def default_file(self):
        file = File()
        file.set_editor(self.new_editor())
        return file

    def reload(self):
        if self.file().reload():
            return True
        return False

    def switch_to_file(self, index):
        self.current_file = index
        yx = self.screen.getmaxyx()
        height = self.max_editor_height()
        self.editor().resize( (height, yx[1]) )
        self.refresh()

    def next_file(self):
        self.status("Next file...")
        if len(self.files) < 2: return
        cur = self.current_file
        cur += 1
        if cur > len(self.files)-1:
            cur = 0
        self.switch_to_file(cur)

    def prev_file(self):
        self.status("Previous file...")
        if len(self.files) < 2: return
        cur = self.current_file
        cur -= 1
        if cur < 0:
            cur = len(self.files)-1
        self.switch_to_file(cur)

    def last_file(self):
        cur = len(self.files)-1
        return cur
        
    def help(self):
        f = self.default_file()
        f.set_data(quick_help)
        self.files.append(f)
        self.switch_to_file(self.last_file())
    
    def handle_char(self, char):
        editor = self.editor()
        if char == 265: # F1
            self.save()
            return True
        elif char == 266:           # F2
            self.reload()
            return True
        elif char == 276:           # F12
            display = self.config["display"]
            display["show_top_bar"] = not display["show_top_bar"]
            display["show_bottom_bar"] = not display["show_bottom_bar"]
            self.resize()
            self.refresh()
        elif char == 8:
            self.help()
        elif char == 5:
            # TODO: Replace this with command modules
            data = self.query("Eval:")
            res = ""
            try:
                res = eval(data)
            except:
                res = "[ERROR]"
            self.status(res)
            return True
        elif char == 6:             # Ctrl + F
            what = self.query("Find:")
            if what != -1:
                editor.find(what)
            return True
        elif char == 7:             # Ctrl + G
            result = self.query("Go to:")
            try:
                result = int(result)
                editor.go_to_pos(result)
            except:
                index = self.find_file(result)
                if index != -1:
                    self.switch_to_file(index)
            return True
        elif char == 15:             # Ctrl + O
            self.open()
            return True
        elif char == 410:
            return True
        elif char == 409:           # Mouse
            mousedata = curses.getmouse()
            x = mousedata[1]
            y = mousedata[2]
            editor.click(x, y-1)
            return True
        elif char == 554:
            self.prev_file()
        elif char == 549:
            self.next_file()
        return False
        
    def keyboard_interrupt(self):
        try:
            yes = self.query("Exit?")
        except:
            self.running = 0
            return True
        if yes:
            self.running = 0
            return True
        return False

    def run(self):
        self.load()
        self.running = 1
        self.refresh()
        while self.running:
            editor = self.editor()
            self.check_resize()
            try:
                char = self.screen.getch()
                self.last_key = char
            except KeyboardInterrupt:
                if self.keyboard_interrupt():
                    break
                continue
                
            if not self.handle_char(char):
                editor.got_chr(char)
            self.refresh_status()
            self.refresh()

        curses.endwin()

def main(*args):
    global app
    app = App()
    app.run()

if __name__ == "__main__":
    curses.wrapper(main)

app.logger.output()
