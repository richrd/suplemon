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
        self.opened = None
        self.editor = None
        
    def save(self):
        pass
       
    def reload(self):
        pass


class App:
    def __init__(self):
        self.running = 0
        self.last_key = None
        self.status_msg = ""
        self.capturing = 0

        self.files = []
        self.current_file = 0

        self.logger = Logger()
        self.config = Config()
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
        
        self.header_win = curses.newwin(1, yx[1], 0, 0)
        self.editor_win = curses.newwin(yx[0]-2, yx[1], 1, 0)
        self.status_win = curses.newwin(1, yx[1], yx[0]-1, 0)

        self.text_input = None # Need this?

    def log(self, s):
        self.logger.log(s)

    def size(self):
        y, x = self.screen.getmaxyx()
        return (x, y)

    def resize(self, yx):
        self.screen.clear()
        curses.resizeterm(yx[0], yx[1])
        self.header_win = curses.newwin(1, yx[1], 0, 0)
        self.editor().resize( (yx[0]-2, yx[1]) )
        self.status_win = curses.newwin(1, yx[1], yx[0]-1, 0)
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

    def query(self, text):
        self.show_capture_status(text)
        self.text_input = curses.textpad.Textbox(self.status_win)
        out = self.text_input.edit()

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
        head = "Suplemon Editor v0.1 - "+curr_time()

        curr_file = self.file()
        filenames = ""
        for f in self.files:
            if f == curr_file:
                filenames += "["+f.name+"] "
            else:
                filenames += f.name+" "
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
            "buf:"+str(len(editor.buffer))+" "+\
            "key:"+str(self.last_key)+" "+\
            "["+str(size[0])+"x"+str(size[1])+"]"

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
        self.show_top_status()
        if self.capturing:
            self.show_capture_status()
        else:
            self.show_bottom_status()

    def open(self):
        name = self.query("Filename:")
        if not name:
            return False
        return self.open_file(name)

    def open_file(self, filename):
        # TODO: Get path,name from filename
        result = self.read_file(filename)
        if not result:
            return False
        file = File()
        file.name = filename
        file.data = result
        file.editor = Editor(self, self.editor_win)
        file.editor.set_data(result)
        file.opened = time.time()        
        self.files.append(file)
        self.refresh()
        return True

    def read_file(self, filename):
        try:
            f = open(filename)
            data = f.read()
            f.close()
            return data
        except:
            self.status("Failed to load '"+filename+"'")
            return False

    def load(self):
        self.log("ARGV:"+str(sys.argv))
        if len(sys.argv) > 1:
            names = sys.argv[1:]
            for name in names:
                self.open_file(name)
        else:
            self.load_default()
        
    def save(self):
        fi = self.file()
        data = fi.editor.get_data()        
        f = open(fi.name, "w")
        f.write(data)
        f.close()
        self.status("Saved '" + fi.name + "'")
        # Safety save
        #f = open(".#"+self.filename+"."+str(time.time()), "w")
        #f.write(data)
        #f.close()

    def load_default(self):
        file = self.default_file()
        self.files.append(file)
        #self.render()

    def default_file(self):
        file = File()
        file.opened = time.time()
        file.editor = Editor(self, self.editor_win)
        file.data = quick_help
        file.path = ""
        file.name = ""
        file.editor.set_data(quick_help)
        return file

    def reload(self):
        self.read_file(self.filename)

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

    def switch_to_file(self, index):
        self.current_file = index
        self.editor().resize(self.screen.getmaxyx())
        self.refresh()

    def handle_char(self, char):
        editor = self.editor()
        #if char == 265 or char == 15: # F1 / Ctrl + O
        if char == 265: # F1
            self.save()
            return True
        elif char == 266:           # F2
            self.reload()
            return True
        #elif char == 51:            # Ctrl + Del
        # Testing query method. Has problems with undetected trailing whitespace :(
        # elif char == 7:             # AltGr + Insert
        #     what = self.query("Echo:")
        #     self.status("'"+what+"'")
        #     return True
        elif char == 6:             # Ctrl + F
            what = self.query("Find:")
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
