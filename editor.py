#!/usr/bin/python
#-*- coding:utf-8
import os
import re
import sys
import time
import curses

try:
    from pygments import highlight
    from pygments.lexers import PythonLexer
    from pygments.formatters import TerminalFormatter
    from pygments.formatters import Terminal256Formatter
    from curses_formatter import * 
    from term_colors import *
    pygments = True
except:
    pygments = False


class Line:
    def __init__(self, data):
        self.data = data
        self.x_scroll = 0

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, i, v):
        self.data[i] = v

    def __str__(self):
        return self.data

    def __add__(self, other):
        return str(self) + other
    
    def __radd__(self, other):
        return other + str(self)

    def __len__(self):
        return len(self.data)

    def decode(self, enc):
        return self.data.decode(enc)

    def encode(self, enc):
        return self.data.encode(enc)

    def find(self, what):
        return self.data.find(what)

class Cursor:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        
    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y

    def __setitem__(self, i, v):
        if i == 0:
            self.x = v
        elif i == 1:
            self.y = v

class Editor:
    def __init__(self, parent, window):
        self.parent = parent
        self.window = window
        self.data = ""
        self.lines = [""]
        self.show_line_nums = True
        self.show_line_ends = False
        self.line_end_char = "<"
        self.last_find = ""
        self.show_highlighting = False
        if pygments != False:
            self.setup_highlighting()
        self.y_scroll = 0
        self.x_scroll = 0
        #self.cursors = [
        #    [0,0],
        #]
        self.cursors = [Cursor()]
        self.buffer = []
        self.cursor_style = curses.A_UNDERLINE
        #self.selection_style = curses.A_REVERSE # Unused...

        self.tab_width = 4
        self.punctuation = ["(", ")", "{", "}", "[", "]", "'", "\"", "=", "+", "-", "/", "*", ".", ":", ",", ";", "_", " "]

    def setup_highlighting(self):
        return # Incomplete implementation
        self.show_highlighting = True
        self.lexer = PythonLexer(encoding = 'utf-8')
        self.term_fmt = CursesFormatter(encoding = 'utf-8')
        self.outfile = HighlightFile()
        self.colors = Colors()

    def log(self, s):
        self.parent.log(s)

    def load(self, data=None):
        if data:
            self.set_data(data)
            self.cursors = [ [0,0] ]
            self.move_cursors()
        #self.render()
        #self.refresh()

    def set_data(self, data):
        self.data = data
        self.lines = []
        lines = self.data.split("\n")
        for line in lines:
            self.lines.append(Line(line))

    def set_tab_width(self, w):
        self.tab_width = w

    def set_cursor(self, cursor):
        if cursor == "underline":
            self.cursor_style = curses.A_UNDERLINE
        elif cursor == "reverse":
            self.cursor_style = curses.A_REVERSE
        else:
            return False
        return True

    def get_data(self):
        data = "\n".join(map(str,self.lines))
        return data

    def size(self):
        y,x = self.window.getmaxyx()
        return (x,y)

    def cursor(self):
        """Return the main cursor."""
        return self.cursors[0]

    def toggle_line_nums(self):
        self.show_line_nums = not self.show_line_nums
        self.render()

    def toggle_line_ends(self):
        self.show_line_ends = not self.show_line_ends
        self.render()

    def toggle_highlight(self):
        self.show_highlighting = not self.show_highlighting
        self.render()

    def pad_lnum(self, n):
        s = str(n)
        while len(s) < self.line_offset()-1:
            s = "0" + s
        return s

    def max_line_length(self):
        return self.size()[0]-self.line_offset()-1

    def line_offset(self):
        if not self.show_line_nums:
            return 0
        return len(str(len(self.lines)))+1

    def whitespace(self, line):
        i = 0
        for char in line:
            if char != " ":
                break
            i += 1
        return i

    def render(self):
        self.window.clear()
        max_y = self.size()[1]
        i = 0
        x_offset = self.line_offset()
        max_len = self.max_line_length()
        while i < max_y:
            lnum = i + self.y_scroll
            if lnum == len(self.lines): break

            line = self.lines[lnum]

            if self.show_line_nums:
                self.window.addstr(i, 0, self.pad_lnum(lnum+1)+" ", curses.color_pair(4))

            # Higlight rendering
            if self.show_highlighting:
                self.outfile.clear()

                highlight(line, self.lexer, self.term_fmt, self.outfile)
                items = self.outfile.get(self.x_scroll, max_len)
                part_offset = x_offset
                for item in items:
                    text = item[0]
                    color = self.colors.get(item[1])
                    self.window.addstr(i, part_offset, text, curses.color_pair(color))
                    part_offset += len(text)
                    #if len(s)+part_offset > max_len:
                    #    s = s[:max_len+part_offset-len(s)-1]
                    #if part_offset > 20:
                    #    break
                #self.window.addstr(i, x_offset, line_part)

            # Normal rendering
            else:
                line_part = line[min(self.x_scroll, len(line)):]
                if self.show_line_ends:
                    line_part += self.line_end_char
                if len(line_part) >= max_len:
                    line_part = line_part[:max_len]
                self.window.addstr(i, x_offset, line_part)
            i += 1
        self.render_cursors()
        self.window.refresh()

    def render_cursors(self):
        max_x, max_y = self.size()
        main = self.cursor()
        for cursor in self.cursors:
            x = cursor[0] - self.x_scroll + self.line_offset()
            y = cursor[1] - self.y_scroll
            if y < 0: continue
            if y >= max_y: break
            if x < self.line_offset(): continue 
            if x > max_x-1: continue 
            self.window.chgat(y, cursor[0]+self.line_offset()-self.x_scroll, 1, self.cursor_style)
            #if cursor == main:
                #self.window.addstr(">", curses.color_pair(1))
                #self.window.chgat(y, cursor[0]+3, 1, self.cursor_style)

    def refresh(self):
        self.window.refresh()

    def resize(self, yx = None):
        self.window.resize(yx[0], yx[1])
        self.move_cursors()
        self.refresh()

    def move_y_scroll(self, delta):
        self.y_scroll += delta

    def move_cursors(self, delta=None, noupdate=False):
        if delta != None:
            for cursor in self.cursors:
                if delta[0] != 0 and cursor[0] >= 0:
                    cursor[0] += delta[0]
                if delta[1] != 0 and cursor[1] >= 0:
                    cursor[1] += delta[1]

                if cursor[0] < 0: cursor[0] = 0
                if cursor[1] < 0: cursor[1] = 0
                if cursor[1] >= len(self.lines)-1: cursor[1] = len(self.lines)-1
                if cursor[0] >= len(self.lines[cursor[1]]): cursor[0] = len(self.lines[cursor[1]])

        c = self.cursor()
        size = self.size()
        offset = self.line_offset()
        if c[1]-self.y_scroll >= size[1]:
            self.y_scroll = c[1]-size[1]+1
        elif c[1]-self.y_scroll < 0:
            #self.y_scroll -= 1
            self.y_scroll = c[1]
        if c[0]-self.x_scroll+offset > size[0]-1:
            #self.x_scroll = len(self.lines[c[1]])-size[0]+offset+1
            self.x_scroll = len(self.lines[c[1]])-size[0]+offset
        if c[0]-self.x_scroll < 0:
            self.x_scroll -= abs(c[0]-self.x_scroll) # FIXME
        if c[0]-self.x_scroll+offset < offset:
            self.x_scroll -= 1
        if not noupdate:
            self.purge_cursors()

    def move_x_cursors(self, line, col, delta):
        for cursor in self.cursors:
            if cursor[1] == line:
                if cursor[0] > col:
                    cursor[0] += delta

    def move_y_cursors(self, line, delta, exclude = None):
        for cursor in self.cursors:
            if cursor == exclude: continue
            if cursor[1] > line:
                    cursor[1] += delta

    def get_first_cursor(self):
        highest = None
        for cursor in self.cursors:
            if highest == None or highest[1] > cursor[1]:
                highest = cursor
        return highest

    def get_last_cursor(self):
        lowest = None
        for cursor in self.cursors:
            if lowest == None or cursor[1] > lowest[1]:
                lowest = cursor
        return lowest

    def purge_cursors(self):
        new = []
        for cursor in self.cursors:
            if not cursor in new:
                new.append(cursor)
        self.cursors = new
        self.render()
        self.refresh()

    def arrow_right(self):
        for cursor in self.cursors:
            if cursor[1] != len(self.lines)-1 and cursor[0] == len(self.lines[cursor[1]]):
                cursor[1] += 1
                cursor[0] = 0
            else:
                cursor[0] += 1
        self.move_cursors()

    def arrow_left(self):
        for cursor in self.cursors:
            if cursor[1] != 0 and cursor[0] == 0:
                cursor[1]-=1
                cursor[0] = len(self.lines[cursor[1]])+1
        self.move_cursors((-1 ,0))

    def arrow_up(self):
        self.move_cursors((0 ,-1))

    def arrow_down(self):
        self.move_cursors((0 ,1))

    def jump_left(self):
        chars = self.punctuation
        for cursor in self.cursors:
            line = self.lines[cursor[1]]
            if cursor[0] == 0:
                continue
            if cursor[0] <= len(line):
                cur_chr = line[cursor[0]-1]
            else:
                cur_chr = line[cursor[0]]
            while cursor[0] > 0:
                next = cursor[0]-2
                if next < 0: next = 0
                if cur_chr == " ":
                    cursor[0] -= 1
                    if line[next] != " ":
                        break
                else:
                    cursor[0] -= 1
                    if line[next] in chars:
                        break
                    #self.move_cursors()
                    #self.parent.status("next:"+line[next]+" cur:"+cur_chr)
                    #self.render()
                    #time.sleep(.5)
        self.move_cursors()
    
    def jump_right(self):
        chars = self.punctuation
        for cursor in self.cursors:
            line = self.lines[cursor[1]]
            if cursor[0] == len(line):
                continue
            cur_chr = line[cursor[0]]
            while cursor[0] < len(line):
                next = cursor[0]+1
                if next == len(line):next-=1
                if cur_chr == " ":
                    cursor[0] += 1
                    if line[next] != " ":
                        break
                else:
                    cursor[0] += 1
                    if line[next] in chars:
                        break
        self.move_cursors()   

    def jump_up(self):
        self.move_cursors((0, -3))

    def jump_down(self):
        self.move_cursors((0, 3))

    def new_cursor_up(self):
        cursor = self.get_first_cursor()
        if cursor[1] == 0: return
        new = Cursor(cursor[0], cursor[1]-1)
        self.cursors.append(new)
        self.move_cursors()

    def new_cursor_down(self):
        cursor = self.get_last_cursor()
        if cursor[1] == len(self.lines)-1: return
        new = Cursor(cursor[0], cursor[1]+1)
        self.cursors.append(new)
        self.move_cursors()

    def new_cursor_left(self):
        new = []
        for cursor in self.cursors:
            if cursor[0] == 0: continue
            new.append( Cursor(cursor[0]-1, cursor[1]) )
        for c in new:
            self.cursors.append(c)
        self.move_cursors()

    def new_cursor_right(self):
        new = []
        for cursor in self.cursors:
            if cursor[0]+1 > len(self.lines[cursor[1]]): continue
            new.append( Cursor(cursor[0]+1, cursor[1]) )
        for c in new:
            self.cursors.append(c)
        self.move_cursors()

    def escape(self):
        self.cursors = [self.cursors[0]]
        self.render()

    def page_up(self):
        for i in range(int(self.size()[1]/2)):
            self.move_cursors((0 ,1), noupdate = True)
        self.move_cursors()

    def page_down(self):
        for i in range(int(self.size()[1]/2)):
            self.move_cursors((0, -1), noupdate = True)
        self.move_cursors()

    def home(self):
        for cursor in self.cursors:
            wspace = self.whitespace(self.lines[cursor[1]])
            if cursor[0] == wspace:
                cursor[0] = 0
            else:
                cursor[0] = wspace
        self.move_cursors()

    def end(self):
        for cursor in self.cursors:
            cursor[0] = len(self.lines[cursor[1]])
        self.move_cursors()

    def delete(self):
        for cursor in self.cursors:
            line = self.lines[cursor[1]]
            start = line[:cursor[0]]
            end = line[cursor[0]+1:]
            self.lines[cursor[1]] = start+end
            self.move_x_cursors(cursor[1], cursor[0], -1)
        self.move_cursors()

    def backspace(self):        
        curs = reversed(sorted(self.cursors, key = lambda c: (c[1], c[0])))
        for cursor in curs: # order?
            if cursor[0] == 0 and cursor[1] == 0:
                continue
            if cursor[0] == 0 and cursor[1] != 0:
                prev_line = self.lines[cursor[1]-1]
                line = self.lines[cursor[1]]
                self.lines.pop(cursor[1])
                self.lines[cursor[1]-1]+=line
                length = len(self.lines[cursor[1]-1])
                cursor[1] -= 1
                cursor[0] = len(prev_line)
                self.move_y_cursors(cursor[1], -1)
            else:
                # TODO: tab backspace
                line = self.lines[cursor[1]]
                #if cursor[0] >=
                start = line[:cursor[0]-1]
                end = line[cursor[0]:]
                self.lines[cursor[1]] = start+end
                cursor[0] -= 1
                self.move_x_cursors(cursor[1], cursor[0], -1)
        # Ensure we keep the view scrolled
        self.move_cursors()

    def enter(self):
        # We sort the cursors, and loop through them from last to first
        # That way we avoid messing with the relative positions of the higher cursors
        curs = reversed(sorted(self.cursors, key = lambda c: (c[1], c[0])))
        for cursor in curs: # order?
            # The current line this cursor is on
            line = self.lines[cursor[1]]
            
            # Start of the line
            start = line[:cursor[0]]

            # End of the line
            end = line[cursor[0]:]

            # Leave the beginning of the line
            self.lines[cursor[1]] = start

            wspace = self.whitespace(self.lines[cursor[1]])*" "
            self.lines.insert(cursor[1]+1, wspace+end)
            self.move_y_cursors(cursor[1], 1)
            cursor[0] = len(wspace)
            cursor[1] += 1
            self.render()
        self.move_cursors()

    def insert(self):
        cur = self.cursor()
        buffer = list(self.buffer)
        if len(self.buffer) == len(self.cursors):
            curs = sorted(self.cursors, key = lambda c: (c[1], c[0]))
            for cursor in curs:
                line = self.lines[cursor[1]]
                buf = buffer[0]
                line = line[:cursor[0]]+buf+line[cursor[0]:]
                self.lines[cursor[1]] = line
                buffer.pop(0)
                self.move_x_cursors(cursor[1], cursor[0]-1, len(buf))
        else:
            for buf in self.buffer:
                y = cur[1]
                if y < 0: y = 0
                self.lines.insert(y, buf)
                self.move_y_cursors(cur[1]-1, 1)
        self.move_cursors()
            
    def push_up(self):
        used_y = []
        curs = sorted(self.cursors, key = lambda c: (c[1], c[0]))
        for cursor in curs:
            if cursor[1] in used_y: continue
            used_y.append(cursor[1])
            
            if cursor[1] == 0: break
            old = self.lines[cursor[1]-1]
            self.lines[cursor[1]-1] = self.lines[cursor[1]]
            self.lines[cursor[1]] = old
            cursor[1] -= 1
        self.move_cursors()
        
    def push_down(self):
        used_y = []
        curs = reversed(sorted(self.cursors, key = lambda c: (c[1], c[0])))
        for cursor in curs:
            if cursor[1] in used_y: continue
            if cursor[1] >= len(self.lines)-1:break
            used_y.append(cursor[1])
            old = self.lines[cursor[1]+1]
            self.lines[cursor[1]+1] = self.lines[cursor[1]]
            self.lines[cursor[1]] = old
            cursor[1] += 1
        self.move_cursors()

    def tab(self):
        for i in range(self.tab_width):
            self.type(" ")

    def untab(self):  
        linenums = []
        for cursor in self.cursors:
            if cursor[1] in linenums:
                cursor[0] = 0
                continue
            line = self.lines[cursor[1]]
            if line[:self.tab_width] == " "*self.tab_width:
                linenums.append(cursor[1])
                cursor[0] = 0
                self.lines[cursor[1]] = line[self.tab_width:]

    def cut(self):
        buf = []
        for cursor in self.cursors:
            if len(self.lines) == 1:
                buf.append(self.lines[0])
                self.lines[0] = ""
                break
            buf.append(self.lines[cursor[1]])
            self.lines.pop(cursor[1])
            self.move_y_cursors(cursor[1],-1)
            if cursor[1] > len(self.lines)-1:
                cursor[1] = len(self.lines)-1
        self.buffer = buf
        self.move_cursors()

    def type(self, letter):
        for cursor in self.cursors:
            line = self.lines[cursor[1]]
            start = line[:cursor[0]]
            end = line[cursor[0]:]
            self.lines[cursor[1]] = start+letter+end
            self.move_x_cursors(cursor[1], cursor[0], 1)
            cursor[0] += 1
        self.move_cursors()

    def go_to_pos(self, line, col = 0):
        try:
            line = abs(int(line)-1)
        except:
            return False

        cur = self.cursor()
        if col != None:
            cur[0] = col
        cur[1] = line
        if cur[1] >= len(self.lines):
            cur[1] = len(self.lines)-1
        self.move_cursors()

    def click(self, x, y):
        x = x - self.line_offset()
        self.go_to_pos(self.y_scroll+y+1, x)

    def find(self, what, findall = False):
        self.last_find = what
        ncursors = len(self.cursors)
        last_cursor = list(reversed(sorted(self.cursors, key = lambda c: (c[1], c[0]))))[-1]
        y = last_cursor[1]
        cur = []
        found = False
        while y < len(self.lines):
            line = self.lines[y]
            indices = [m.start() for m in re.finditer(re.escape(what), str(line))]
            for i in indices:
                new = [i, y]
                if not new in self.cursors:
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
        what = self.last_find
        if what == "":
            cursor = self.cursor()
            search = "^([\w\-]+)"
            line = self.lines[cursor[1]][cursor[0]:]
            matches = re.match(search, line)
            if matches == None: return
            what = matches.group(0)
            self.last_find = what
            #self.parent.status("what:"+str(what))
        #self.parent.status("Finding '"+what+"'")
        self.find(what)

    def find_all(self):
        self.find(self.last_find, True)

    def got_chr(self, char):
        if char == curses.KEY_RIGHT: self.arrow_right()        # Arrow Right
        elif char == curses.KEY_LEFT: self.arrow_left()        # Arrow Left
        elif char == curses.KEY_UP: self.arrow_up()            # Arrow Up
        elif char == curses.KEY_DOWN: self.arrow_down()        # Arrow Down
        elif char == curses.KEY_NPAGE: self.page_up()          # Page Up    
        elif char == curses.KEY_PPAGE: self.page_down()        # Page Down

        elif char == 273: self.toggle_line_nums()              # F9
        elif char == 274: self.toggle_line_ends()              # F10
        elif char == 275: self.toggle_highlight()              # F11
        elif char == 331: self.insert()                        # Insert

        elif char == 563: self.new_cursor_up()                 # Alt + up
        elif char == 522: self.new_cursor_down()               # Alt + down
        elif char == 542: self.new_cursor_left()               # Alt + left
        elif char == 557: self.new_cursor_right()              # Alt + right

        elif char == 4: self.find_next()                       # Ctrl + D
        elif char == 1: self.find_all()                        # Ctrl + D
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
        else:
            try:
                letter = chr(char)
                self.type(letter)
            except:
                pass

        self.render()
        self.refresh()

    def loop(self):
        pass
