#!/usr/bin/python
#-*- coding:utf-8
import os
import sys
import time
import curses

#class Log:
#    def __init__(self, name="log.txt"):
#        self.filename = name
#        self.file = open(self.filename, "w")
#
#    def log(self, s):
#        self.file.write(s + "\n")
#
#    def close(self):
#        self.file.close()

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

    #def scrolled(self):
    #    return

class Editor:
    def __init__(self, parent, window):
        self.parent = parent
        self.window = window
        self.data = ""
        self.lines = [""]
        self.y_scroll = 0
        self.x_scroll = 0
        self.cursors = [
            [0,0],
            [4,0],
        ]
        #elf.cursor_style = curses.A_UNDERLINE
        self.cursor_style = curses.A_REVERSE
        self.selection_style = curses.A_REVERSE
        self.tab_width = 4

    def log(self, s):
        self.parent.log(s)

    def load(self, data=None):
        if data:
            self.set_data(data)
            self.cursors = [ [0,0] ]
        self.render()
        self.refresh()

    def set_data(self, data):
        self.data = data
        self.lines = []
        lines = self.data.split("\n")
        for line in lines:
            self.lines.append(Line(line))

    def get_data(self):
        data = "\n".join(map(str,self.lines))
        return data

    def size(self):
        y,x = self.window.getmaxyx()
        return (x,y)

    def cursor(self):
        """Return the main cursor."""
        return self.cursors[0]

    def pad_lnum(self, n):
        s = str(n)
        while len(s) < self.line_offset()-1:
            s = "0" + s
        return s

    def max_line_length(self):
        return self.size()[0]-self.line_offset()

    def line_offset(self):
        return len(str(len(self.lines)))+1

    def render(self):
        """
        TODO
        - FULL SCREEN X_SCROLL!? ftw
        - Use line.x_scroll to position line
        - Remove excess characters
        - Reposition cursors accordingly
        """
        self.window.clear()
        max_y = self.size()[1]
        i = 0
        x_offset = self.line_offset()
        max_len = self.max_line_length()
        while i < max_y:
            lnum = i+self.y_scroll
            if lnum == len(self.lines): break
            line = self.lines[lnum]
            line_part = line[min(self.x_scroll, len(line)):]
            if len(line_part) >= max_len: line_part = line_part[:max_len-1]
            self.window.addstr(i, 0, self.pad_lnum(lnum+1)+" "+line_part)
            #self.window.addstr(i, 0, self.pad_lnum(lnum+1)+" "+line_part, curses.color_pair(curses.COLOR_CYAN))
            self.window.chgat(i, 0, x_offset-1, curses.A_STANDOUT)
            i += 1
        self.render_cursors()
        self.window.refresh()

    def render_cursors(self):
        max_y = self.size()[1]
        main = self.cursor()
        for cursor in self.cursors:
            x = cursor[0] - self.x_scroll + self.line_offset()
            y = cursor[1] - self.y_scroll
            if y >= max_y: break
            if x < self.line_offset(): continue 
            self.window.chgat(y, cursor[0]+self.line_offset()-self.x_scroll, 1, self.cursor_style)
            #if cursor == main:
                #self.window.addstr(">", curses.color_pair(1))
                #self.window.chgat(y, cursor[0]+3, 1, self.cursor_style)

    def escape(self):
        self.cursors = [self.cursors[0]]
        self.render()

    def relative_cursors(self):
        pass

    def refresh(self):
        self.window.refresh()

    def resize(self, yx = None):
        self.parent.msg("resize")
        #c = self.cursor()
        #self.parent.msg("")
        #if c[1]-self.y_scroll+self.size()[1] >= self.size()[1]:
        #    self.y_scroll = c[1]+self.size()[1]-1
        self.move_cursors()
        self.refresh()

    def move_y_scroll(self, delta):
        self.y_scroll += delta

    def move_cursors(self, delta=None):
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
            self.y_scroll += 1
        elif c[1]-self.y_scroll < 0:
            self.y_scroll -= 1
        self.parent.msg(str(c[0]-self.x_scroll))
        if c[0]-self.x_scroll+offset > size[0]-1:
            self.x_scroll = len(self.lines[c[1]])-size[0]+offset+1
        if c[0]-self.x_scroll < 0:
            self.x_scroll -= abs(c[0]-self.x_scroll) # FIXME
        if c[0]-self.x_scroll+offset < offset:
            self.x_scroll -= 1
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
                cursor[1]+=1
                cursor[0] = 0
        self.move_cursors((1 ,0))

    def arrow_left(self):
        #self.move_cursors((-1 ,0))
        for cursor in self.cursors:
            if cursor[1] != 0 and cursor[0] == 0:
                cursor[1]-=1
                cursor[0] = len(self.lines[cursor[1]])+1
        self.move_cursors((-1 ,0))
        

    def arrow_up(self):
        self.move_cursors((0 ,-1))

    def arrow_down(self):
        self.move_cursors((0 ,1))

    def new_cursor_up(self):
        cursor = self.get_first_cursor()
        if cursor[1] == 0: return
        new = [cursor[0], cursor[1]-1]
        self.cursors.append(new)
        self.purge_cursors()

    def new_cursor_down(self):
        cursor = self.get_last_cursor()
        if cursor[1] == len(self.lines)-1: return
        new = [cursor[0], cursor[1]+1]
        self.cursors.append(new)
        self.purge_cursors()

    def new_cursor_left(self):
        new = []
        for cursor in self.cursors:
            if cursor[0] == 0: continue
            new.append( [cursor[0]-1, cursor[1]] )
        for c in new:
            self.cursors.append(c)
        self.purge_cursors()

    def new_cursor_right(self):
        new = []
        for cursor in self.cursors:
            new.append( [cursor[0]+1, cursor[1]] )
        for c in new:
            self.cursors.append(c)
        self.purge_cursors()

    def page_up(self):
        for i in range(self.size()[1]/2):
            self.move_cursors((0 ,1))

    def page_down(self):
        for i in range(self.size()[1]/2):
            self.move_cursors((0, -1))

    def home(self):
        for cursor in self.cursors:
            cursor[0] = 0
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
        self.purge_cursors()

    def backspace(self):
        for cursor in self.cursors:
            if cursor[0] == 0 and cursor[1] == 0:
                return
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
        self.purge_cursors()

    def enter(self):
        #curs = self.cursors.copy()
        #curs.sort()
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

            #self.parent.msg(start+" - "+end+"->"+str(cursor))
            self.lines.insert(cursor[1]+1, end)
            self.move_y_cursors(cursor[1], 1)
            cursor[0] = 0
            cursor[1] += 1
            #self.move_y_cursors(0, 1)
            self.render()
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
        #for i in range(self.tab_width):
        #    self.type(" ")

    def cut(self):
        for cursor in self.cursors:
            if len(self.lines) == 1:
                self.lines[0] = ""
                break
            self.lines.pop(cursor[1])
            self.move_y_cursors(cursor[1],-1)
            if cursor[1] > len(self.lines)-1:
                cursor[1] = len(self.lines)-1
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

    def got_chr(self, char):
        if char == curses.KEY_RIGHT: self.arrow_right()
        elif char == curses.KEY_LEFT: self.arrow_left()
        elif char == curses.KEY_UP: self.arrow_up()
        elif char == curses.KEY_DOWN: self.arrow_down()
        elif char == curses.KEY_NPAGE: self.page_up()
        elif char == curses.KEY_PPAGE: self.page_down()

        elif char == 563: self.new_cursor_up()                   #Alt + up
        elif char == 522: self.new_cursor_down()                 #Alt + down
        elif char == 542: self.new_cursor_left()                 #Alt + left
        elif char == 557: self.new_cursor_right()                #Alt + right
        elif char == 24: self.cut()                              # Ctrl + X

        elif char == curses.KEY_HOME: self.home()
        elif char == curses.KEY_END: self.end()
        elif char == curses.KEY_BACKSPACE: self.backspace()
        elif char == curses.KEY_DC: self.delete()
        elif char == curses.KEY_ENTER: self.enter()
        elif char == 9: self.tab()                              # Tab
        elif char == 353: self.untab()                            # Shigt + Tab
        elif char == 10: self.enter()                           # Enter
        elif char == 27: self.escape()                          # Escape
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


class App:
    def __init__(self):
        self.running = 0
        self.filename = None
        self.last_key = None
        self.status_msg = ""    
        self.screen = curses.initscr()
        curses.start_color()
        curses.use_default_colors()

        curses.cbreak()
        curses.noecho()
        #curses.curs_set(False)
        #self.screen.nodelay(1)
        self.screen.keypad(1)

        self.current_yx = self.screen.getmaxyx()
        yx = self.screen.getmaxyx()
        #self.resize()
        self.header_win = curses.newwin(1, yx[1], 0, 0)
        self.editor_win = curses.newwin(yx[0]-2, yx[1], 1, 0)
        self.status_win = curses.newwin(1, yx[1], yx[0]-1, 0)

        self.editor = Editor(self, self.editor_win)
        #self.editor.load(thedata)
        self.refresh()

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

    def status(self):
        data = "key:"+str(self.last_key)+\
            " size:"+str(self.editor.size())+\
            " pos:"+str(self.editor.cursor())+\
            " x:"+str(self.editor.x_scroll)+\
            " y:"+str(self.editor.y_scroll)+\
            " status:"+self.status_msg
        self.header_win.clear()
        self.header_win.addstr(0,0, "Editor test...")

        self.status_win.clear()
        #self.status_win.addstr(0,0, "MAXYX:"+str(self.screen.getmaxyx())+"LAST:"+str(self.last_key)+" "+str(self.editor.cursors))
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
            self.read_file(sys.argv[1])

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
        if char == 265:
            self.save()             # F1

    def keyboard_interrupt(self):
        self.query_exit()

    def run(self):
        self.load()
        self.running = 1
        self.editor.render()
        while self.running:
            self.editor.loop()
            # try:
            char = self.screen.getch()
            # except Exception, e:
            #     self.keyboard_interrupt()
            self.check_resize()
            if char != -1:
                if not self.handle_char(char):
                    self.editor.got_chr(char)
                self.last_key = char
                self.status()
                self.refresh()
            #time.sleep(000000.1)

        curses.endwin()

a = App()
a.run()