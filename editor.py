#!/usr/bin/python
#-*- coding:utf-8

import os
import re
import sys
import time
import curses
import imp

from line import *
from cursor import *
from helpers import *
from viewer import *

class Editor(Viewer):
    def __init__(self, parent, window):
        Viewer.__init__(self, parent, window)

        self.buffer = [] # Copy/paste
        self.last_find = ""
        self.tab_width = 4
        self.punctuation = ""
        self.auto_indent_newline = 1

    def arrow_right(self):
        """Move cursors right."""
        for cursor in self.cursors:
            line = self.lines[cursor.y]
            if cursor.y != len(self.lines)-1 and (cursor.x >= len(line) or len(line) == 0 ):
                cursor.y += 1
                cursor.x = 0
            elif cursor.x < len(self.lines[cursor.y]) and len(line) > 0:
                cursor.x += 1
        self.move_cursors()

    def arrow_left(self):
        """Move cursors left."""
        for cursor in self.cursors:
            if cursor.y != 0 and cursor.x == 0:
                cursor.y-=1
                cursor.x = len(self.lines[cursor.y])+1
        self.move_cursors((-1 ,0))

    def arrow_up(self):
        """Move cursors up."""
        self.move_cursors((0 ,-1))

    def arrow_down(self):
        """Move cursors down."""
        self.move_cursors((0 ,1))

    def jump_left(self):
        """Jump one 'word' to the left."""
        chars = self.punctuation
        for cursor in self.cursors:
            line = self.lines[cursor.y]
            if cursor.x == 0:
                continue
            if cursor.x <= len(line):
                cur_chr = line[cursor.x-1]
            else:
                cur_chr = line[cursor.x]
            while cursor.x > 0:
                next = cursor.x-2
                if next < 0: next = 0
                if cur_chr == " ":
                    cursor.x -= 1
                    if line[next] != " ":
                        break
                else:
                    cursor.x -= 1
                    if line[next] in chars:
                        break
        self.move_cursors()
    
    def jump_right(self):
        """Jump one 'word' to the right."""
        chars = self.punctuation
        for cursor in self.cursors:
            line = self.lines[cursor.y]
            if cursor.x == len(line):
                continue
            cur_chr = line[cursor.x]
            while cursor.x < len(line):
                next = cursor.x+1
                if next == len(line):next-=1
                if cur_chr == " ":
                    cursor.x += 1
                    if line[next] != " ":
                        break
                else:
                    cursor.x += 1
                    if line[next] in chars:
                        break
        self.move_cursors()   

    def jump_up(self):
        """Jump up 3 lines."""
        self.move_cursors((0, -3))

    def jump_down(self):
        """Jump down 3 lines."""
        self.move_cursors((0, 3))

    def new_cursor_up(self):
        """Add a new cursor one line up."""
        cursor = self.get_first_cursor()
        if cursor.y == 0: return
        new = Cursor(cursor.x, cursor.y-1)
        self.cursors.append(new)
        self.move_cursors()

    def new_cursor_down(self):
        """Add a new cursor one line down."""
        cursor = self.get_last_cursor()
        if cursor.y == len(self.lines)-1: return
        new = Cursor(cursor.x, cursor.y+1)
        self.cursors.append(new)
        self.move_cursors()

    def new_cursor_left(self):
        """Add a new cursor one character left."""
        new = []
        for cursor in self.cursors:
            if cursor.x == 0: continue
            new.append( Cursor(cursor.x-1, cursor.y) )
        for c in new:
            self.cursors.append(c)
        self.move_cursors()

    def new_cursor_right(self):
        """Add a new cursor one character right."""
        new = []
        for cursor in self.cursors:
            if cursor.x+1 > len(self.lines[cursor.y]): continue
            new.append( Cursor(cursor.x+1, cursor.y) )
        for c in new:
            self.cursors.append(c)
        self.move_cursors()

    def escape(self):
        """Handle escape key. Removes all except primary cursor."""
        self.cursors = [self.cursors[0]]
        self.move_cursors()
        self.render()

    def page_up(self):
        """Move half a page up."""
        for i in range(int(self.size()[1]/2)):
            self.move_cursors((0 ,1), noupdate = True)
        self.move_cursors()

    def page_down(self):
        """Move half a page down."""
        for i in range(int(self.size()[1]/2)):
            self.move_cursors((0, -1), noupdate = True)
        self.move_cursors()

    def home(self):
        """Move to start of line or text on that line."""
        for cursor in self.cursors:
            wspace = self.whitespace(self.lines[cursor.y])
            if cursor.x == wspace:
                cursor.x = 0
            else:
                cursor.x = wspace
        self.move_cursors()

    def end(self):
        """Move to end of line."""
        for cursor in self.cursors:
            cursor.x = len(self.lines[cursor.y])
        self.move_cursors()

    def delete(self):
        """Delete the next character."""
        for cursor in self.cursors:
            line = self.lines[cursor.y]
            if len(self.lines)>1 and cursor.x == len(line) and cursor.y != len(self.lines)-1:
                data = self.lines[cursor.y]
                self.lines.pop(cursor.y)
                self.lines[cursor.y] = Line(data+self.lines[cursor.y])
                self.move_x_cursors(cursor.y, cursor.x, -1)
            else:
                start = line[:cursor.x]
                end = line[cursor.x+1:]
                self.lines[cursor.y] = Line(start+end)
                self.move_x_cursors(cursor.y, cursor.x, -1)
        self.move_cursors()

    def backspace(self):
        """Delete the previous character."""
        curs = reversed(sorted(self.cursors, key = lambda c: (c[1], c[0])))
        for cursor in curs: # order?
            if cursor.x == 0 and cursor.y == 0:
                continue
            if cursor.x == 0 and cursor.y != 0:
                prev_line = self.lines[cursor.y-1]
                line = self.lines[cursor.y]
                self.lines.pop(cursor.y)
                self.lines[cursor.y-1]+=line
                length = len(self.lines[cursor.y-1])
                cursor.y -= 1
                cursor.x = len(prev_line)
                self.move_y_cursors(cursor.y, -1)
            else:
                # TODO: tab backspace
                line = self.lines[cursor.y]
                start = line[:cursor.x-1]
                end = line[cursor.x:]
                self.lines[cursor.y] = Line(start+end)
                cursor.x -= 1
                self.move_x_cursors(cursor.y, cursor.x, -1)
        # Ensure we keep the view scrolled
        self.move_cursors()

    def enter(self):
        """Insert a new line."""
        # We sort the cursors, and loop through them from last to first
        # That way we avoid messing with the relative positions of the higher cursors
        curs = reversed(sorted(self.cursors, key = lambda c: (c[1], c[0])))
        for cursor in curs: # order?
            # The current line this cursor is on
            line = self.lines[cursor.y]
            
            # Start of the line
            start = line[:cursor.x]

            # End of the line
            end = line[cursor.x:]

            # Leave the beginning of the line
            self.lines[cursor.y] = Line(start)
            wspace = ""
            if self.auto_indent_newline:
                wspace = self.whitespace(self.lines[cursor.y])*" "
            self.lines.insert(cursor.y+1, Line(wspace+end))
            self.move_y_cursors(cursor.y, 1)
            cursor.x = len(wspace)
            cursor.y += 1
        self.move_cursors()

    def insert(self):
        """Insert buffer data at cursor(s)."""
        cur = self.cursor()
        buffer = list(self.buffer)
        if len(self.buffer) == len(self.cursors):
            curs = sorted(self.cursors, key = lambda c: (c[1], c[0]))
            for cursor in curs:
                line = self.lines[cursor.y]
                buf = buffer[0]
                line = line[:cursor.x]+buf+line[cursor.x:]
                self.lines[cursor.y] = Line(line)
                buffer.pop(0)
                self.move_x_cursors(cursor.y, cursor.x-1, len(buf))
        else:
            for buf in self.buffer:
                y = cur[1]
                if y < 0: y = 0
                self.lines.insert(y, Line(buf))
                self.move_y_cursors(cur[1]-1, 1)
        self.move_cursors()
            
    def push_up(self):
        """Move current lines up by one line."""
        used_y = []
        curs = sorted(self.cursors, key = lambda c: (c[1], c[0]))
        for cursor in curs:
            if cursor.y in used_y: continue
            used_y.append(cursor.y)
            
            if cursor.y == 0: break
            old = self.lines[cursor.y-1]
            self.lines[cursor.y-1] = Line(self.lines[cursor.y])
            self.lines[cursor.y] = Line(old)
            cursor.y -= 1
        self.move_cursors()
        
    def push_down(self):
        """Move current lines down by one line."""
        used_y = []
        curs = reversed(sorted(self.cursors, key = lambda c: (c[1], c[0])))
        for cursor in curs:
            if cursor.y in used_y: continue
            if cursor.y >= len(self.lines)-1:break
            used_y.append(cursor.y)
            old = self.lines[cursor.y+1]
            self.lines[cursor.y+1] = Line(self.lines[cursor.y])
            self.lines[cursor.y] = Line(old)
            cursor.y += 1
        self.move_cursors()

    def tab(self):
        """Indent lines."""
        for i in range(self.tab_width):
            self.type(" ")

    def untab(self):
        """Unindent lines."""
        linenums = []
        for cursor in self.cursors:
            if cursor.y in linenums:
                cursor.x = 0
                continue
            line = self.lines[cursor.y]
            if line[:self.tab_width] == " "*self.tab_width:
                linenums.append(cursor.y)
                cursor.x = 0
                self.lines[cursor.y] = Line(line[self.tab_width:])

    def cut(self):
        """Cut lines to buffer."""
        buf = []
        for cursor in self.cursors:
            if len(self.lines) == 1:
                buf.append(self.lines[0])
                self.lines[0] = ""
                break
            buf.append(self.lines[cursor.y])
            self.lines.pop(cursor.y)
            self.move_y_cursors(cursor.y,-1)
            if cursor.y > len(self.lines)-1:
                cursor.y = len(self.lines)-1
        self.buffer = buf
        self.move_cursors()

    def type(self, letter):
        """Insert a character."""
        for cursor in self.cursors:
            line = self.lines[cursor.y]
            start = line[:cursor.x]
            end = line[cursor.x:]
            self.lines[cursor.y] = Line(start + letter + end)
            self.move_x_cursors(cursor.y, cursor.x, 1)
            cursor.x += 1
        self.move_cursors()

    def go_to_pos(self, line, col = 0):
        """Move primary cursor to line, col=0."""
        try:
            line = int(line)-1
            if line < 0: line = 0
        except:
            return False

        cur = self.cursor()
        if col != None:
            cur.x = col
        cur.y = line
        if cur.y >= len(self.lines):
            cur.y = len(self.lines)-1
        self.move_cursors()

    def click(self, x, y):
        """Handle a click at x, y."""
        x = x - self.line_offset()
        self.go_to_pos(self.y_scroll+y+1, x)

    def find(self, what, findall = False):
        """Find what in data. Adds a cursor when found."""
        self.last_find = what
        ncursors = len(self.cursors)
        last_cursor = list(reversed(sorted(self.cursors, key = lambda c: (c.y, c.x))))[-1]
        y = last_cursor.y
        cur = []
        found = False
        while y < len(self.lines):
            line = self.lines[y]
            x_offset = 0
            if last_cursor.y == y:
                x_offset = last_cursor.x
                indices = [m.start() for m in re.finditer(re.escape(what), str(line[x_offset:]))]
            else:
                indices = [m.start() for m in re.finditer(re.escape(what), str(line))]
            for i in indices:
                new = Cursor(i+x_offset, y)
                if not self.cursor_exists(new):
                    found = True
                    cur.append(new)
                    if not findall:
                        break
                if not new in cur:
                    cur.append(new)
            if found and not findall: break
            y += 1
        if not found:
            self.parent.status("Can't find '"+what+"'")
            return
        self.cursors = cur
        self.move_cursors()

    def find_next(self):
        """Find next occurance."""
        what = self.last_find
        if what == "":
            cursor = self.cursor()
            search = "^([\w\-]+)"
            line = self.lines[cursor.y][cursor.x:]
            matches = re.match(search, line)
            if matches == None: return
            what = matches.group(0)
            self.last_find = what
        self.find(what)

    def find_all(self):
        """Find all occurances."""
        self.find(self.last_find, True)

    def duplicate_line(self):
        """Copy current line and add it below as a new line."""
        curs = sorted(self.cursors, key = lambda c: (c.y, c.x))
        self.parent.log(curs)
        #cur_y = []
        for cursor in curs:
            line = self.lines[cursor.y]
            self.lines.insert(cursor.y+1, line)
            self.move_y_cursors(cursor.y+1, 1)
        self.move_cursors()

    def got_chr(self, char):
        """Handle character input."""
        if char == curses.KEY_RIGHT: self.arrow_right()        # Arrow Right
        elif char == curses.KEY_LEFT: self.arrow_left()        # Arrow Left
        elif char == curses.KEY_UP: self.arrow_up()            # Arrow Up
        elif char == curses.KEY_DOWN: self.arrow_down()        # Arrow Down
        elif char == curses.KEY_NPAGE: self.page_up()          # Page Up    
        elif char == curses.KEY_PPAGE: self.page_down()        # Page Down

        elif char == 563: self.new_cursor_up()                 # Alt + up
        elif char == 522: self.new_cursor_down()               # Alt + down
        elif char == 542: self.new_cursor_left()               # Alt + left
        elif char == 557: self.new_cursor_right()              # Alt + right

        elif char == 273: self.toggle_line_nums()              # F9
        elif char == 274: self.toggle_line_ends()              # F10
        elif char == 275: self.toggle_highlight()              # F11
        elif char == 331: self.insert()                        # Insert
        elif char == 22: self.insert()                         # Ctrl + V

        elif char == 4: self.find_next()                       # Ctrl + D
        elif char == 1: self.find_all()                        # Ctrl + A
        elif char == 24: self.cut()                            # Ctrl + X
        elif char == 544: self.jump_left()                     # Ctrl + Left
        elif char == 559: self.jump_right()                    # Ctrl + Right
        elif char == 565: self.jump_up()                       # Ctrl + Up
        elif char == 524: self.jump_down()                     # Ctrl + Down
        elif char == 552: self.push_up()                       # Ctrl + Page Up
        elif char == 547: self.push_down()                     # Ctrl + Down

        elif char == curses.KEY_HOME: self.home()              # Home
        elif char == curses.KEY_END: self.end()                # End
        elif char == curses.KEY_BACKSPACE: self.backspace()    # Backspace
        elif char == curses.KEY_DC: self.delete()              # Delete
        elif char == curses.KEY_ENTER: self.enter()            # Enter
        elif char == 9: self.tab()                             # Tab
        elif char == 353: self.untab()                         # Shift + Tab
        elif char == 10: self.enter()                          # Enter
        elif char == 27: self.escape()                         # Escape
        elif char == 23: self.duplicate_line()                 # Ctrl + W
        else:
            try:
                letter = chr(char)
                self.type(letter)
            except:
                pass

        self.render()
        self.refresh()
