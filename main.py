#!/usr/bin/python
#-*- coding:utf-8
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

Usage: python main.py [filename]

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
        self.path = ""
        self.data = ""
        self.last_save = None
        self.opened = time.time()
        self.editor = None

    def _path(self):
        return os.path.join(self.path, self.name)

    def log(self, s):
        app.logger.log(s)

    def set_data(self, data):
        self.data = data
        if self.editor:
            self.editor.set_data(data)
        
    def set_path(self, path):
        ab = os.path.abspath(path)
        self.path, self.name = os.path.split(ab)
        
    def set_editor(self, editor):
        self.editor = editor

    def set_saved(self, m):
         self.last_save = time.time()

    def save(self):
        self.log("Saving: "+self._path())
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
        self.log("loading: "+self._path())
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
        curses.start_color()
        curses.use_default_colors()

        if curses.can_change_color(): # Can't get these to work :(
            pass
            #curses.init_color(11, 254, 0, 1000)
        
        # This only works with: TERM=xterm-256color ./main.py
        #curses.init_pair(1, curses.COLOR_BLACK, 91) # Black on yellow

        #curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLUE)
        curses.init_pair(4, curses.COLOR_WHITE, -1)
        #curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # Higlight colors:
        curses.init_pair(10, -1, -1) # Default (white on black)
        curses.init_pair(11, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(12, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(13, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(14, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(15, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(16, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(17, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        
        curses.cbreak()
        curses.noecho()
        curses.curs_set(0)
        self.screen.keypad(1)
        
        # Mouse mode kills scroll wheel...
        #curses.mousemask(curses.BUTTON1_CLICKED)

        self.current_yx = self.screen.getmaxyx()
        yx = self.screen.getmaxyx()
        self.text_input = None

        self.header_win = curses.newwin(1, yx[1], 0, 0)
        y_sub = 0
        y_start = 0
        if self.config["display"]["show_top_bar"]:
            y_sub +=1
            y_start = 1
        if self.config["display"]["show_bottom_bar"]:
            y_sub +=1
        self.editor_win = curses.newwin(yx[0]-y_sub, yx[1], y_start, 0)
        self.status_win = curses.newwin(1, yx[1], yx[0]-y_sub+1, 0)

        self.inited = 1 # Indicate that windows etc. have been created.
        
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
                
        self.header_win = curses.newwin(1, yx[1], 0, 0)
        y_sub = 0
        y_start = 0
        if self.config["display"]["show_top_bar"]:
            y_sub +=1
            y_start = 1
        if self.config["display"]["show_bottom_bar"]:
            y_sub +=1
        #self.editor_win = curses.newwin(yx[0], yx[1], y_start, 0)
        self.editor().resize( (yx[0]-y_sub, yx[1]) )
        self.editor().move_win( (y_start, 0) )
        #self.editor().window.mvwin(y_start, 0)
        self.status_win = curses.newwin(1, yx[1], yx[0]-y_sub+1, 0)
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

    def editor(self):
        return self.files[self.current_file].editor
        
    def new_editor(self):
        editor = Editor(self, self.editor_win)
        editor.set_tab_width(self.config["editor"]["tab_width"])
        editor.set_cursor(self.config["editor"]["cursor"])
        editor.show_line_nums = self.config["display"]["show_line_nums"]
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
        head = "Suplemon Editor v0.1 "
        if self.config["display"]["show_clock"]:
            head += "- " + curr_time()

        filenames = ""
        
        # Weird looping for warping current file to first index
        # FIXME: Move to dedicated method
        cur = self.current_file
        target = cur-1
        if target < 0:
            target = len(self.files)-self.current_file-1
        f_ind = 0    # File count index
        while f_ind < len(self.files):
            f = self.files[cur]
            if f_ind == 0:
                filenames += "["+f.name
                if f.is_changed():
                    filenames += "*"
                filenames += "] "
            else:
                filenames += f.name+(["","*"][f.is_changed()])+" "
            cur += 1
            if cur >= len(self.files):
                cur = 0
            f_ind += 1
        
        head += " - "+filenames
        head = head + ( " " * (self.screen.getmaxyx()[1]-len(head)-1) )
        if len(head) >= size[0]:
            head = head[:size[0]-1]
        self.header_win.addstr(0,0, head, curses.color_pair(0) | curses.A_REVERSE)
        self.header_win.refresh()

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

    def refresh_status(self):
        if not self.inited: return False
        if self.config["display"]["show_top_bar"]:
            self.show_top_status()
        if self.capturing:
            self.show_capture_status()
        else:
            if self.config["display"]["show_bottom_bar"]:
                self.show_bottom_status()

    def open(self):
        name = self.query("Filename:")
        if not name:
            return False
        if not self.open_file(name):
            self.status("Failed to load '"+name+"'")

    def open_file(self, filename, new = False):
        result = ""
        file = File()
        file.set_path(filename)
        file.set_editor(self.new_editor())
        loaded = file.load()
        self.files.append(file)
        return loaded

    def read_file(self, filename):
        try:
            f = open(filename)
            data = f.read()
            f.close()
            return data
        except:
            return False

    def load(self):
        loaded = True
        if len(sys.argv) > 1:
            names = sys.argv[1:]
            for name in names:
                if self.open_file(name):
                    loaded = True
        else:
            self.load_default()
        
    def save(self):
        fi = self.file()
        if fi.save():
            self.status("Saved '" + fi.name + "'")
            return True
        self.status("Couldn't write to '" + fi.name + "'")
        return False

    def load_default(self):
        file = self.default_file()
        self.files.append(file)

    def default_file(self):
        file = File()
        file.set_editor(self.new_editor())
        file.set_data(quick_help)
        return file

    def reload(self):
        data = self.read_file(self.file().name)
        if self.file().reload(data):
            return True
        return False

    def switch_to_file(self, index):
        self.current_file = index
        yx = self.screen.getmaxyx()
        self.editor().resize( (yx[0]-2, yx[1]) )
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
        self.switch_to_file(cur)

    def handle_char(self, char):
        editor = self.editor()
        if char == 265: # F1
            self.save()
            return True
        elif char == 266:           # F2
            self.reload()
            return True
        elif char == 276:
            self.config["display"]["show_top_bar"] = not self.config["display"]["show_top_bar"]
            self.config["display"]["show_bottom_bar"] = not self.config["display"]["show_bottom_bar"]
            self.resize()
            self.refresh()
        elif char == 12:
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
            lineno = self.query("Go:")
            editor.go_to_pos(lineno)
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
            self.next_file()
        elif char == 549:
            self.prev_file()
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
