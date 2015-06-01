#-*- encoding: utf-8
"""
Text viewer component subclassed by Editor.
"""

import os
import re
import sys
import imp
import time
import curses

from line import *
from cursor import *
from helpers import *

class Viewer:
    def __init__(self, app, window):
        """
        Handle Viewer initialization
        
        :param App app: The main App class of Suplemon
        :param Window window: The ui window to use for the viewer
        """
        self.app = app
        self.window = window
        self.config = {}
        self.data = ""
        self.lines = [Line()]
        self.file_extension = ""
        
        # Map special extensions to generic ones for highlighting
        self.extension_map = {
            "scss": "css",
        }
        self.show_line_ends = True

        self.cursor_style = curses.A_UNDERLINE

        self.y_scroll = 0
        self.x_scroll = 0
        self.cursors = [Cursor()]

        self.syntax = None
        self.setup_linelight()

    def log(self, s):
        """Log to the app."""
        #TODO: log types: ERROR | WARNING | NOTICE
        self.app.log(s)

    def setup_linelight(self):
        """Setup line based highlighting."""
        ext = self.file_extension
        # Check if a file extension is redefined
        # Maps e.g. 'scss' to 'css'
        if ext in self.extension_map.keys():
            ext = self.extension_map[ext] # Use it
        curr_path = os.path.dirname(os.path.realpath(__file__))

        filename = ext + ".py"
        path = os.path.join(curr_path, "linelight", filename)

        module = False
        if os.path.isfile(path):
            self.app.log("Syntax file found...", LOG_INFO)
            try:
                module = imp.load_source(ext, path)
                self.app.log("File loaded...", LOG_INFO)
            except:
                self.app.log(get_error_info())
        else:
            return False

        if not module or not "Syntax" in dir(module):
            self.app.log("File doesn't match API!")
            return False
        self.syntax = module.Syntax()

    def size(self):
        """Get editor size (x,y). (Deprecated, use get_size)."""
        self.log("size() is deprecated, please use get_size()")
        return self.get_size()
        
    def cursor(self):
        """Return the main cursor. (Deprecated, use get_cursor)"""
        self.log("cursor() is deprecated, please use get_cursor()")
        return self.get_cursor()

    def get_size(self):
        """Get editor size (x,y)."""
        y,x = self.window.getmaxyx()
        return (x,y)
        
    def get_cursor(self):
        """Return the main cursor."""
        return self.cursors[0]

    def get_cursors(self):
        """Return list of all cursors."""
        return self.cursors[0]

    def get_first_cursor(self):
        """Get the first (primary) cursor."""
        highest = None
        for cursor in self.cursors:
            if highest == None or cursor.y <  highest.y:
                highest = cursor
        return highest

    def get_last_cursor(self):
        """Get the last cursor."""
        lowest = None
        for cursor in self.cursors:
            if lowest == None:
                lowest = cursor
            elif cursor.y > lowest.y:
                lowest = cursor
            elif cursor.y == lowest.y and cursor.x > lowest.x:
                 lowest = cursor
        return lowest

    def get_cursors_on_line(self, line_no):
        """Return all cursors on a specific line."""
        cursors = []
        for cursor in self.cursors:
            if cursor.y == line_no:
                cursors.append(cursor)
        return cursors

    def get_lines_with_cursors(self):
        """Return all line indices that have cursors.

        :return: A list of line numbers that have cursors.
        :rtype: list
        """
        line_nums = []
        for cursor in self.cursors:
            if not cursor.y in line_nums:
                line_nums.append(cursor.y)
        line_nums.sort()
        return line_nums

    def get_line_color(self, raw_line):
        """Return a color based on line contents.
        
        :param str raw_line: The line from which to get a color value.
        :return: A color value for given raw_data.
        :rtype: int
        """
        if self.syntax:
            try:
                return self.syntax.get_color(raw_line)
            except:
                return 0
        return 0

    def get_data(self):
        """Get editor contents.
        
        :return: Editor contents.
        :rtype: str
        """
        str_lines = []
        for line in self.lines:
            if type(line) == type(""):
                str_lines.append(line)
            else:
                str_lines.append(line.get_data())
        data = str(self.config["end_of_line"].join(str_lines))
        return data

    def set_data(self, data):
        """Set editor data or contents.
        
        :param str data: Set the editor contents to data.
        """
        self.data = data
        self.lines = []
        lines = self.data.split(self.config["end_of_line"])
        for line in lines:
            self.lines.append(Line(line))

    def set_config(self, config):
        """Set the viewer configuration dict.
        
        :param dict config: Editor config dict with any supported fields. See config.py.
        """
        self.config = config
        self.set_cursor_style(self.config["cursor"])

    def set_cursor_style(self, cursor):
        """Set cursor style.
        
        :param str cursor: Cursor type, either 'underline' or 'reverse'.
        """
        if cursor == "underline":
            self.cursor_style = curses.A_UNDERLINE
        elif cursor == "reverse":
            self.cursor_style = curses.A_REVERSE
        else:
            return False
        return True
        
    def set_cursor(self, cursor):
        self.log("set_cursor is deprecated, use set_cursor_style instead.")
        return self.set_cursor_style(cursor)

    def set_single_cursor(self, cursor):
        """Discard all cursors and place a new one."""
        self.cursors = [Cursor(cursor)]

    def set_cursors(self, cursors):
        """Replace cursors with new cursor list."""
        self.cursors = cursors

    def set_file_extension(self, ext):
        """Set the file extension."""
        ext = ext.lower()
        if ext and ext != self.file_extension:
            self.file_extension = ext
            self.setup_linelight()

    def pad_lnum(self, n):
        """Pad line number with zeroes."""
        #TODO: move to helpers
        s = str(n)
        while len(s) < self.line_offset()-1:
            s = "0" + s
        return s

    def max_line_length(self):
        """Get maximum line length that fits in the editor."""
        return self.get_size()[0]-self.line_offset()-1

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

    def render(self):
        """Render the editor curses window."""
        self.window.clear()
        max_y = self.get_size()[1]
        i = 0
        x_offset = self.line_offset()
        max_len = self.max_line_length()
        # Iterate through visible lines
        while i < max_y:
            lnum = i + self.y_scroll
            if lnum >= len(self.lines): # Make sure we have a line to show
                break
            
            # Get line for current row
            line = self.lines[lnum]
            if self.config["show_line_nums"]:
                self.window.addstr(i, 0, self.pad_lnum(lnum+1)+" ", curses.color_pair(8))

            # Normal rendering
            line_part = line[min(self.x_scroll, len(line)):]
            if self.show_line_ends:
                line_part += self.config["line_end_char"]
            if len(line_part) >= max_len:
                # Clamp line length to view width
                line_part = line_part[:max_len]

            # Replace unsafe whitespace with normal space or visible replacement
            # For example tab characters make cursors go out of sync with line contents
            for key in self.config["white_space_map"].keys():
                char = " "
                if self.config["show_white_space"]:
                    char = self.config["white_space_map"][key]
                line_part = line_part.replace(key, char);
            # Use unicode support on Python 3.3 and higher
            if sys.version_info[0] == 3 and sys.version_info[1] > 2:
                line_part = line_part.encode("utf-8")
            try:
                if self.config["show_line_colors"]:
                    self.window.addstr(i, x_offset, line_part, curses.color_pair(self.get_line_color(line)))
                else:
                    self.window.addstr(i, x_offset, line_part)
            except Exception as inst:
                self.log(type(inst))    # the exception instance
                self.log(inst.args)     # arguments stored in .args
                self.log(inst)          # __str__ allows args to be printed directly,
            i += 1
        self.render_cursors()

    def render_cursors(self):
        """Render editor window cursors."""
        max_x, max_y = self.get_size()
        main = self.get_cursor()
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
        if not yx:
            yx = self.window.getmaxyx()
        self.window.resize(yx[0], yx[1])
        self.move_cursors()
        self.refresh()

    def move_win(self, yx):
        """Move the editor window to position yx."""
        # Must try & catch since mvwin might
        # crash with incorrect coordinates
        try:
            self.window.mvwin( yx[0], yx[1] )
        except:
            self.app.log(get_error_info(), LOG_WONTFIX)

    def move_y_scroll(self, delta):
        """Add delta the y scroll axis scroll"""
        self.y_scroll += delta
        
    def scroll_up(self):
        """Scroll view up if neccesary."""
        cursor = self.get_first_cursor()
        if cursor.y - self.y_scroll < 0:
            # Scroll up
            self.y_scroll = cursor.y
    
    def scroll_down(self):
        """Scroll view up if neccesary."""
        cursor = self.get_last_cursor()
        size = self.get_size()
        if cursor.y - self.y_scroll >= size[1]:
            # Scroll down
            self.y_scroll = cursor.y - size[1]+1

    def move_cursors(self, delta=None, noupdate=False):
        """Move all cursors with delta. To avoid refreshing the screen set noupdate to True."""
        for cursor in self.cursors:
            if delta:
                if delta[0] != 0 and cursor.x >= 0:
                    cursor.move_right(delta[0])
                if delta[1] != 0 and cursor.y >= 0:
                    cursor.move_down(delta[1])

            if cursor.x < 0: cursor.x = 0
            if cursor.y < 0: cursor.y = 0
            if cursor.y >= len(self.lines)-1: cursor.y = len(self.lines)-1
            if cursor.x >= len(self.lines[cursor.y]): cursor.x = len(self.lines[cursor.y])

        cur = self.get_cursor() # Main cursor
        size = self.get_size()
        offset = self.line_offset()
        # Check if we should scroll horizontally
        if cur.x - self.x_scroll+offset > size[0] - 1:
            # -1 to allow space for cursor at line end
            self.x_scroll = len(self.lines[cur.y]) - size[0]+offset+1
        if cur.x - self.x_scroll < 0:
            self.x_scroll  -= abs(cur.x - self.x_scroll) # FIXME
        if cur.x - self.x_scroll+offset < offset:
            self.x_scroll -= 1            
        if not noupdate:
            self.purge_cursors()

    def scroll_to_line(self, line_no):
        """Center the viewport on line_no."""
        if line_no >= len(self.lines):
            line_no = len(self.lines)-1
        new_y = line_no - int(self.get_size()[1] / 2)
        if new_y < 0:
            new_y = 0
        self.y_scroll = new_y

    def move_x_cursors(self, line, col, delta):
        """Move all cursors starting at line and col with delta on the x axis."""
        for cursor in self.cursors:
            if cursor.y == line:
                if cursor.x > col:
                    cursor.move_right(delta)

    def move_y_cursors(self, line, delta, exclude = None):
        """Move all cursors starting at line and col with delta on the y axis.
        Exlude a cursor by passing it via the exclude argument."""
        for cursor in self.cursors:
            if cursor == exclude:
                continue
            if cursor.y > line:
                cursor.move_down(delta)

    def cursor_exists(self, cursor):
        """Check if a given cursor exists."""
        return cursor.tuple() in [cursor.tuple() for cursor in self.cursors]

    def remove_cursor(self, cursor):
        """Remove a cursor object from the cursor list."""
        try:
            index = self.cursors.index(cursor)
        except:
            return False
        self.cursors.pop(index)
        return True

    def purge_cursors(self):
        """Remove duplicate cursors that have the same position."""
        new = []
        # This sucks: can't use "if .. in .." for different instances (?)
        # Use a reference list instead. FIXME: use a generator
        ref = []
        for cursor in self.cursors:
            if not cursor.tuple() in ref:
                ref.append(cursor.tuple())
                new.append(cursor)
        self.cursors = new
        self.render()

    def purge_line_cursors(self, line_no):
        """Remove all but first cursor on given line."""
        line_cursors = []
        for cursor in self.cursors:
            if cursor.y == line_no:
                line_cursors.append(cursor)
        if len(line_cursors) < 2:
            return False

        # Leave the first cursor out
        line_cursors.pop(0)
        # Remove the rest
        for line_cursors in cursor:
            self.remove_cursor(cursor)
        return True
