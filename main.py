#!/usr/bin/python
#-*- coding:utf-8
import os
import sys
import time
import curses

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
        curses.def_shell_mode()
        curses.start_color()
        curses.use_default_colors()
        
        curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(3,curses.COLOR_RED, curses.COLOR_BLUE)

        curses.cbreak()
        curses.noecho()
        self.screen.keypad(1)

        self.current_yx = self.screen.getmaxyx()
        yx = self.screen.getmaxyx()
        #self.resize()
        self.header_win = curses.newwin(1, yx[1], 0, 0)
        self.editor_win = curses.newwin(yx[0]-2, yx[1], 1, 0)
        self.status_win = curses.newwin(1, yx[1], yx[0]-1, 0)

        self.editor = Editor(self, self.editor_win)
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

    def msg(self, s):
        self.status_msg = s
        self.status()

    def query(self, text):
        return ""
    
    def status(self):
        data = "key:"+str(self.last_key)+\
            " size:"+str(self.editor.size())+\
            " pos:"+str(self.editor.cursor())+\
            " x:"+str(self.editor.x_scroll)+\
            " y:"+str(self.editor.y_scroll)+\
            " status:"+self.status_msg
        self.header_win.clear()
    
        head = "Suplemon Editor v0.1 - "+curr_time()
        if self.filename != None:
            head += " - "+self.filename
        head = head + ( " " * (self.screen.getmaxyx()[1]-len(head)-1) )
        self.header_win.addstr(0,0, head, curses.color_pair(1))

        self.status_win.clear()
        if len(data)>self.screen.getmaxyx()[0]:
            data = data[:self.screen.getmaxyx()[1]-1]
        self.status_win.addstr(0,0,data)

        self.header_win.refresh()
        self.status_win.refresh()

    def read_file(self, filename):
        self.filename = filename
        f = open(filename)
        data = f.read()
        f.close()
        self.editor.load(data)

    def load(self):
        if len(sys.argv) > 1:
            self.msg("Loading!")
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
        self.msg("Saved to "+self.filename)

    def handle_char(self, char):       
        if char == 265:             # F1
            self.save()
            return True             
        elif char == 266:           # F2
            self.reload()
            return True
        if self.capturing:
            return True
        return False
        
    def keyboard_interrupt(self):
        #yes = self.query("Exit?")
        yes = True
        if yes:
            curses.reset_shell_mode()
            curses.endwin()
            self.running = 0
            sys.exit(1)
            return True

    def run(self):
        self.load()
        self.running = 1
        self.editor.render()
        self.status()
        self.refresh()
        while self.running:
            self.check_resize()
            try:
                char = self.screen.getch()
            except KeyboardInterrupt:
                if self.keyboard_interrupt():
                    break
                
            if not self.handle_char(char):
                self.editor.got_chr(char)
            self.last_key = char
            self.status()
            self.refresh()

        curses.endwin()

a = App()
a.run()