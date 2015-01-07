#!/usr/bin/python
#-*- coding:utf-8
"""
Text Viewer component subclassed by Editor.
"""

import os
import re
import sys
import time
import curses
import imp

from line import *
from cursor import *
from helpers import *

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

class Viewer:
    def __init__(self, parent, window):
        self.parent = parent
        self.window = window
        self.config = []
        self.data = ""
        self.lines = [Line()]
        self.file_extension = ""
        
        self.linelighter = lambda line: 0 # Dummy linelighter returns default color
        self.show_highlighting = False
        if pygments != False:
            self.setup_highlighting()
        self.show_line_ends = True

        self.cursor_style = curses.A_UNDERLINE

        self.y_scroll = 0
        self.x_scroll = 0
        self.cursors = [Cursor()]

    def set_config(self, config):
        self.config = config
        self.set_cursor(self.config["cursor"])

    def setup_linelight(self):
        """Setup line based highlighting."""
        if not self.file_extension:
            # TODO: Create default linelighter
            return False
        filename = self.file_extension + ".py"
        curr_path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(curr_path, "linelight", filename)
        try:
            mod = imp.load_source(self.file_extension, path)
        except:
            self.parent.logger.log(get_error_info())
            self.parent.logger.log("no linelight found")
            return False
        if not "parse" in dir(mod):
            return False
        self.linelighter = mod.parse

    def setup_highlighting(self):
        """Setup pygments syntax highlighting."""
        return # Incomplete implementation
        #self.show_highlighting = True
        #self.lexer = PythonLexer(encoding = 'utf-8')
        #self.term_fmt = CursesFormatter(encoding = 'utf-8')
        #self.outfile = HighlightFile()
        #self.colors = Colors()

    def size(self):
        """Get editor size (x,y)."""
        y,x = self.window.getmaxyx()
        return (x,y)

    def cursor(self):
        """Return the main cursor."""
        return self.cursors[0]

    def get_line_color(self, raw_line):
        """Return a color based on line contents."""
        try:
            return self.linelighter(raw_line)
        except:
            return 0

    def log(self, s):
        """Log to the app."""
        self.parent.log(s)

    def set_data(self, data):
        """Set editor data or contents."""
        self.data = data
        self.lines = []
        lines = self.data.split("\n")
        for line in lines:
            self.lines.append(Line(line))

    def get_data(self):
        """Get editor contents."""
        # FIXME: Unify storing lines as Line instances
        str_lines = []
        for line in self.lines:
            if type(line) == type(""):
                str_lines.append(line)
            else:
                str_lines.append(line.data)
        data = u"\n".join(str_lines)
        return data

    def set_cursor(self, cursor):
        """Set cursor style."""
        if cursor == "underline":
            self.cursor_style = curses.A_UNDERLINE
        elif cursor == "reverse":
            self.cursor_style = curses.A_REVERSE
        else:
            return False
        return True

    def set_file_extension(self, ext):
        """Set the file extension."""
        if ext:
            self.file_extension = ext.lower()
            self.setup_linelight()

    def pad_lnum(self, n):
        """Pad line number with zeroes."""
        s = str(n)
        while len(s) < self.line_offset()-1:
            s = "0" + s
        return s

    def max_line_length(self):
        """Get maximum line length that fits in the editor."""
        return self.size()[0]-self.line_offset()-1

    def line_offset(self):
        """Get the x coordinate of beginning of line."""
        if not self.config["show_line_nums"]:
            return 0
        return len(str(len(self.lines)))+1

    def whitespace(self, line):
        """Return index of first non whitespace character on a line."""
        i = 0
        for char in line:
            if char != " ":
                break
            i += 1
        return i

    def toggle_line_nums(self):
        """Toggle display of line numbers."""
        self.config["show_line_nums"] = not self.config["show_line_nums"]
        self.render()

    def toggle_line_ends(self):
        """Toggle display of line ends."""
        self.show_line_ends = not self.show_line_ends
        self.render()

    def toggle_highlight(self):
        """Toggle syntax highlighting."""
        return False
        #self.show_highlighting = not self.show_highlighting
        #self.render()

    def render(self):
        """Render the editor curses window."""
        self.window.clear()
        max_y = self.size()[1]
        i = 0
        x_offset = self.line_offset()
        max_len = self.max_line_length()
        while i < max_y:
            lnum = i + self.y_scroll
            if lnum == len(self.lines): break

            line = self.lines[lnum]

            if self.config["show_line_nums"]:
                self.window.addstr(i, 0, self.pad_lnum(lnum+1)+" ", curses.color_pair(4))

            # Higlight rendering
            if self.show_highlighting and pygments:
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

            # Normal rendering
            else:
                line_part = line[min(self.x_scroll, len(line)):]
                if self.show_line_ends:
                    line_part += self.config["line_end_char"]
                if len(line_part) >= max_len:
                    line_part = line_part[:max_len]

                line_part = line_part.encode("utf-8")
                if self.config["show_line_colors"]:
                    self.window.addstr(i, x_offset, line_part, curses.color_pair(self.get_line_color(line)))
                else:
                    self.window.addstr(i, x_offset, line_part)
            i += 1
        self.render_cursors()
        self.window.refresh()

    def render_cursors(self):
        """Render editor window cursors."""
        max_x, max_y = self.size()
        main = self.cursor()
        for cursor in self.cursors:
            x = cursor.x - self.x_scroll + self.line_offset()
            y = cursor.y - self.y_scroll
            if y < 0: continue
            if y >= max_y: break
            if x < self.line_offset(): continue 
            if x > max_x-1: continue 
            self.window.chgat(y, cursor.x+self.line_offset()-self.x_scroll, 1, self.cursor_style)

    def refresh(self):
        """Refresh the editor curses window."""
        self.window.refresh()

    def resize(self, yx = None):
        """Resize the UI."""
        self.window.resize(yx[0], yx[1])
        self.move_cursors()
        self.refresh()

    def move_win(self, yx):
        """Move the editor window to position yx."""
        self.window.mvwin( yx[0], yx[1] )

    def move_y_scroll(self, delta):
        """Add delta the y scroll axis scroll"""
        self.y_scroll += delta

    def move_cursors(self, delta=None, noupdate=False):
        """Move all cursors with delta. To avoid refreshing the screen set noupdate to True."""
        if delta != None:
            for cursor in self.cursors:
                if delta[0] != 0 and cursor.x >= 0:
                    cursor.x += delta[0]
                if delta[1] != 0 and cursor.y >= 0:
                    cursor.y += delta[1]

                if cursor.x < 0: cursor.x = 0
                if cursor.y < 0: cursor.y = 0
                if cursor.y >= len(self.lines)-1: cursor.y = len(self.lines)-1
                if cursor.x >= len(self.lines[cursor.y]): cursor.x = len(self.lines[cursor.y])

        cur = self.cursor() # Main cursor
        size = self.size()
        offset = self.line_offset()
        if cur.y - self.y_scroll >= size[1]:
            self.y_scroll = cur.y - size[1]+1
        elif cur.y - self.y_scroll < 0:
            self.y_scroll = cur.y
        if cur.x - self.x_scroll+offset > size[0] - 1:
            # +1 to allow space for cursor at line end
            self.x_scroll = len(self.lines[cur.y]) - size[0]+offset+1
        if cur.x - self.x_scroll < 0:
            self.x_scroll  -= abs(cur.x - self.x_scroll) # FIXME
        if cur.x - self.x_scroll+offset < offset:
            self.x_scroll -= 1
        if not noupdate:
            self.purge_cursors()

    def move_x_cursors(self, line, col, delta):
        """Move all cursors starting at line and col with delta on the x axis."""
        for cursor in self.cursors:
            if cursor.y == line:
                if cursor.x > col:
                    cursor.x += delta

    def move_y_cursors(self, line, delta, exclude = None):
        """Move all cursors starting at line and col with delta on the y axis.
        Exlude a cursor by passing it via the exclude argument."""
        for cursor in self.cursors:
            if cursor == exclude: continue
            if cursor.y > line:
                    cursor.y += delta

    def get_first_cursor(self):
        """Get the first (primary) cursor."""
        highest = None
        for cursor in self.cursors:
            if highest == None or highest[1] > cursor.y:
                highest = cursor
        return highest

    def get_last_cursor(self):
        """Get the last cursor."""
        lowest = None
        for cursor in self.cursors:
            if lowest == None or cursor.y > lowest[1]:
                lowest = cursor
        return lowest

    def cursor_exists(self, cursor):
        """Check if a given cursor exists."""
        return cursor.tuple() in [cursor.tuple() for cursor in self.cursors]

    def purge_cursors(self):
        """Remove duplicate cursors that have the same position."""
        new = []
        # This sucks: can't use "in" for different instances (?)
        # Use a reference list instead. FIXME: use a generator
        ref = []
        for cursor in self.cursors:
            if not cursor.tuple() in ref:
                ref.append( cursor.tuple() )
                new.append(cursor)
        self.cursors = new
        self.render()
        self.refresh()
