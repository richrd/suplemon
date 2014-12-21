#!/usr/bin/python
#-*- coding:utf-8
import os
import sys
import time
import curses
import curses.textpad

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
 
 * ESC
   > Revert to a single cursor
   
 * Ctrl + X
   > Delete line(s)
   
 * Ctrl + F
   > Find text.
   
 * Ctrl + D
   > Add a new cursor at the next occurance.
 
 * F1
   > Save current file
   
 * F2
   > Reload current file
 
 * Alt + Page Up
   > Move line(s) up
 
 * Alt + Page Down
   > Move line(s) down

"""




class App:
    def __init__(self):
        self.running = 0
        self.filename = None
        self.last_key = None
        self.status_msg = ""
        self.capturing = 0

        #self.config = Config()
        #self.config.load()

        self.screen = curses.initscr()

        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(3,curses.COLOR_RED, curses.COLOR_BLUE)

        curses.cbreak()
        curses.noecho()
        #curses.mousemask(curses.BUTTON1_CLICKED)
        self.screen.keypad(1)

        self.current_yx = self.screen.getmaxyx()
        yx = self.screen.getmaxyx()
        
        self.header_win = curses.newwin(1, yx[1], 0, 0)
        self.editor_win = curses.newwin(yx[0]-2, yx[1], 1, 0)
        self.status_win = curses.newwin(1, yx[1], yx[0]-1, 0)

        self.editor = Editor(self, self.editor_win)
        self.text_input = None

        self.refresh()

    def capture(self, yes=1):
        self.capturing = yes

    def log(self, s):
        log.log(s)
        self.status_win.clear()
        self.status_win.addstr(0,0, s)
        self.status_win.refresh()

    def resize(self, yx):
        self.screen.clear()
        curses.resizeterm(yx[0], yx[1])
        self.header_win = curses.newwin(1, yx[1], 0, 0)
        self.editor.window = curses.newwin(yx[0]-2, yx[1], 1, 0)
        self.status_win = curses.newwin(1, yx[1], yx[0]-1, 0)
        self.editor.resize(yx)
        self.screen.refresh()

    def check_resize(self):
        yx = self.screen.getmaxyx()
        if self.current_yx != yx:
            self.current_yx = yx
            self.resize(yx)

    def refresh(self):
        self.screen.refresh()

    def status(self, s):
        self.status_msg = s
        self.refresh_status()

    def query(self, text):
        self.show_capture_status(text)
        self.text_input = curses.textpad.Textbox(self.status_win)
        out = self.text_input.edit()

        # If input begins with prompt, remove the prompt text
        if len(out) >= len(text):
            if out[:len(text)] == text:
                out = out[len(text):]
        if out[-1] == " ": out = out[:-1]
        out = out.rstrip("\r\n")
        #self.status(out)
        return out

    def show_top_status(self):
        self.header_win.clear()
        head = "Suplemon Editor v0.1 - "+curr_time()
        if self.filename != None:
            head += " - "+self.filename
        head = head + ( " " * (self.screen.getmaxyx()[1]-len(head)-1) )
        self.header_win.addstr(0,0, head, curses.color_pair(1))
        self.header_win.refresh()

    def show_bottom_status(self):
        size = self.editor.size()
        cur = self.editor.cursor()
        data = "@ "+str(cur[0])+","+str(cur[1])+" "+\
            "cur:"+str(len(self.editor.cursors))+" "+\
            "buf:"+str(len(self.editor.buffer))+" "+\
            "key:"+str(self.last_key)+" "+\
            "["+str(size[0])+"x"+str(size[1])+"]"

        if self.editor.last_find:
            find = self.editor.last_find
            if len(find) > 10:find = find[:10]+"..."
            data = "find:'"+find+"' " + data

        self.status_win.clear()

        status = self.status_msg
        extra = size[0] - len(status+data)-1
        line = status+(" "*extra)+data

        if len(line)>self.screen.getmaxyx()[0]:
            line = line[:self.screen.getmaxyx()[1]-1]

        self.status_win.addstr(0, 0, line)
        self.status_win.refresh()

    def show_capture_status(self, s=""):
        self.status_win.clear()
        self.status_win.addstr(0, 0, s)
        self.status_win.refresh()

    def refresh_status(self):
        self.show_top_status()
        if self.capturing:
            self.show_capture_status()
        else:
            self.show_bottom_status()

    def read_file(self, filename):
        try:
            self.filename = filename
            f = open(filename)
            data = f.read()
            f.close()
        except:
            self.status("Failed to load '"+filename+"'")
            return False
        self.editor.load(data)

    def load(self):
        if len(sys.argv) > 1:
            self.read_file(sys.argv[1])
        else:
            self.editor.set_data(quick_help)
            
    def reload(self):
        self.read_file(self.filename)        

    def save(self):
        data = self.editor.get_data()
        f = open("#"+self.filename+"."+str(time.time()), "w")
        f.write(data)
        f.close()
        
        f = open(self.filename, "w")
        f.write(data)
        f.close()
        self.status("Saved to "+self.filename)

    def handle_char(self, char):
        if char == 265 or char == 15: # F1 / Ctrl + O
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
            self.editor.find(what)
            return True
        elif char == 7:             # Ctrl + G
            lineno = self.query("Go:")
            self.editor.go_to_pos(lineno)
            return True
        elif char == 410:
            return True
        elif char == 409:           # Mouse
            mousedata = curses.getmouse()
            x = mousedata[1]
            y = mousedata[2]
            self.editor.click(x, y-1)
            return True
        if self.capturing:
            return True
        return False
        
    def keyboard_interrupt(self):
        yes = self.query("Exit?")
        if yes:
            self.running = 0
            return True
        return False

    def run(self):
        self.load()
        self.running = 1
        self.editor.render()
        self.refresh_status()
        self.refresh()
        while self.running:
            self.check_resize()
            try:
                char = self.screen.getch()
                self.last_key = char
            except KeyboardInterrupt:
                if self.keyboard_interrupt():
                    break
                continue
                
            if not self.handle_char(char):
                self.editor.got_chr(char)
            #time.sleep(1)
            self.refresh_status()
            self.refresh()

        curses.endwin()

def main(*args):
    a = App()
    a.run()

if __name__ == "__main__":
    curses.wrapper(main)