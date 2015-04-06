#-*- encoding: utf-8
"""
Editor class for handling, well, editing.
"""

import os
import re
import sys
import time
import curses

from line import *
from cursor import *
from helpers import *
from viewer import *

class State:
    """Store editor state for undo/redo."""
    def __init__(self, editor=None):
        self.cursors = [Cursor()]
        self.lines = [Line()]
        self.y_scroll = 0
        self.x_scroll = 0
        self.last_find = ""
        if editor != None:
            self.store(editor)

    def store(self, editor):
        """Store the state of editor instance."""
        self.cursors = [cursor.tuple() for cursor in editor.cursors]
        self.lines = [line.data for line in editor.lines]
        self.y_scroll = editor.y_scroll
        self.x_scroll = editor.x_scroll
        self.last_find = editor.last_find

    def restore(self, editor):
        """Restore stored state into the editor instance."""
        editor.cursors = [Cursor(cursor) for cursor in self.cursors]
        editor.lines = [Line(line) for line in self.lines]
        editor.y_scroll = self.y_scroll
        editor.x_scroll = self.x_scroll
        editor.last_find = self.last_find

class Editor(Viewer):
    """Extends Viewer with editing capabilities."""
    def __init__(self, app, window):
        Viewer.__init__(self, app, window)
        self.buffer = []               # Copy/paste buffer
        self.last_find = ""            # Last search used in 'find'
        self.history = [State()]       # History of editor states for undo/redo
        self.current_state = 0         # Current state index of the editor
        self.last_action = None        # Last editor action that was used (for undo/redo)

    def set_data(self, data):
        """Set the editor text contents."""
        Viewer.set_data(self, data)
        if len(self.buffer) > 1:
            self.store_state()
        else:
            state = State()
            state.store(self)
            self.history[0] = state

    def store_action_state(self, action, state = None):
        """Store the editor state if a new action is taken."""
        if self.last_action != action:
            self.last_action = action
            self.store_state(state)
        else:
            # TODO:This if is here just for safety. current_state might be wrong ;.<
            if self.current_state < len(self.history)-1:
                self.history[self.current_state].store(self)

    def store_state(self, state = None, action = None):
        """Store the current editor state for undo/redo."""
        if state == None:
            state = State()
            state.store(self)
        if len(self.history) > 1:
            if self.current_state < len(self.history)-1:
                self.history = self.history[:self.current_state]

        self.history.append(state)
        self.current_state = len(self.history)-1

        if len(self.history) > self.config["max_history"]:
            self.history.pop(0)

    def restore_state(self, index=None):
        """Restore an editor state."""
        if len(self.history) <= 1:
            return False
        if index == None:
            index = self.current_state-1

        if index < 0 or index >= len(self.history):
            return False

        #if self.current_state < len(self.history):
        #    self.current_state = self.current_state-1

        state = self.history[index]
        state.restore(self)
        self.current_state = index
        self.refresh()

    def undo(self):
        """Undo the last command or change."""
        self.last_action = "undo"
        self.restore_state()

    def redo(self):
        """Redo the last command or change."""
        self.last_action = "redo"
        if self.current_state == len(self.history)-1:
            return False
        index = self.current_state+1
        self.restore_state(index)

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
        chars = self.config["punctuation"]
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
        chars = self.config["punctuation"]
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
        x = self.cursor().x
        cursor = self.get_first_cursor()
        if cursor.y == 0:
            return
        new = Cursor(x, cursor.y-1)
        self.cursors.append(new)
        self.move_cursors()

    def new_cursor_down(self):
        """Add a new cursor one line down."""
        x = self.cursor().x
        cursor = self.get_last_cursor()
        if cursor.y == len(self.lines)-1:
            return
        new = Cursor(x, cursor.y+1)
        self.cursors.append(new)
        self.move_cursors()

    def new_cursor_left(self):
        """Add a new cursor one character left."""
        new = []
        for cursor in self.cursors:
            if cursor.x == 0:
                continue
            new.append( Cursor(cursor.x-1, cursor.y) )
        for c in new:
            self.cursors.append(c)
        self.move_cursors()

    def new_cursor_right(self):
        """Add a new cursor one character right."""
        new = []
        for cursor in self.cursors:
            if cursor.x+1 > len(self.lines[cursor.y]):
                continue
            new.append( Cursor(cursor.x+1, cursor.y) )
        for c in new:
            self.cursors.append(c)
        self.move_cursors()

    def escape(self):
        """Handle escape key. Removes last_find and all cursors except primary cursor."""
        self.last_find = ""
        self.cursors = [self.cursors[0]]
        self.move_cursors()
        self.render()

    def page_up(self):
        """Move half a page up."""
        amount = int(self.size()[1]/2)
        self.move_cursors((0 ,amount), noupdate = True)

    def page_down(self):
        """Move half a page down."""
        amount = int(self.size()[1]/2)
        self.move_cursors((0 ,amount * -1), noupdate = True)

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
        # Add a restore point if previous action != delete
        self.store_action_state("delete")

    def backspace(self):
        """Delete the previous character."""
        curs = reversed(sorted(self.cursors, key = lambda c: (c[1], c[0])))
        # Iterate through all cursors from bottom to top
        for cursor in curs:
            line_no = cursor.y
            # If we're at the beginning of file don't do anything
            if cursor.x == 0 and cursor.y == 0:
                continue
            # If were operating at the beginning of a line
            if cursor.x == 0 and cursor.y != 0:
                curr_line = self.lines.pop(line_no)
                prev_line = self.lines[line_no-1]
                length = len(prev_line) # Get the length of previous line
                self.lines[cursor.y-1] += curr_line # Add the current line to the previous one
                line_cursors = self.get_cursors_on_line(line_no) # Get all cursors on current line
                for line_cursor in line_cursors: # Move the cursors
                    line_cursor.y -= 1 # One line up
                    # Add the length of previous line to each x coordinate
                    # so that their relative positions
                    line_cursor.x += length
                # Move all cursors below up one line (since a line was removed above them)
                self.move_y_cursors(cursor.y, -1)
            # Handle all other cases
            else:
                # TODO: tab backspace
                curr_line = self.lines[line_no]
                # Slice one character out of the line
                start = curr_line[:cursor.x-1]
                end = curr_line[cursor.x:]
                self.lines[line_no] = Line(start+end) # Store the new line
                cursor.x -= 1 # Move the operating curser back one
                self.move_x_cursors(line_no, cursor.x, -1) # Do the same to the rest
        # Ensure we keep the view scrolled
        self.move_cursors()
        # Add a restore point if previous action != backspace
        self.store_action_state("backspace")

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
            if self.config["auto_indent_newline"]:
                wspace = self.whitespace(self.lines[cursor.y])*" "
            self.lines.insert(cursor.y+1, Line(wspace+end))
            self.move_y_cursors(cursor.y, 1)
            cursor.x = len(wspace)
            cursor.y += 1
        self.move_cursors()

        # Add a restore point if previous action != enter
        self.store_action_state("enter")

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
        # Add a restore point if previous action != insert
        self.store_action_state("insert")

    def comment(self):
        """Comment the current line(s)."""
        comment = "#"
        used_y = []
        curs = sorted(self.cursors, key = lambda c: (c[1], c[0]))
        for cursor in curs:
            if cursor.y in used_y:
                continue
            used_y.append(cursor.y)
            line = self.lines[cursor.y].data
            w = self.whitespace(line)
            start = line[:w]
            self.app.set_status(start)
            if starts(line[w:], comment):
                self.lines[cursor.y] = Line(start + line.lstrip()[len(comment):])
                self.move_x_cursors(cursor.y, w, 0-len(comment))
            else:
                self.lines[cursor.y] = Line(start + comment + line.lstrip())
                self.move_x_cursors(cursor.y, w, len(comment))
        self.move_cursors()
        self.store_action_state("comment")

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
        # Add a restore point if previous action != push_up
        self.store_action_state("push_up")
            
        
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
        # Add a restore point if previous action != push_down
        self.store_action_state("push_down")

    def tab(self):
        """Indent lines."""
        # Add a restore point if previous action != tab
        self.store_action_state("tab")
        for i in range(self.config["tab_width"]):
            self.type(" ")

    def untab(self):
        """Unindent lines."""
        linenums = []
        for cursor in self.cursors:
            if cursor.y in linenums:
                cursor.x = 0
                continue
            line = self.lines[cursor.y]
            if line[:self.config["tab_width"]] == " "*self.config["tab_width"]:
                linenums.append(cursor.y)
                cursor.x = 0
                self.lines[cursor.y] = Line(line[self.config["tab_width"]:])
        # Add a restore point if previous action != untab
        self.store_action_state("untab")

    def cut(self):
        """Cut lines to buffer."""
        # Store cut lines in buffer
        cut_buffer = []
        # Get all lines with cursors on them
        line_nums = self.get_lines_with_cursors()
        # Sort from last to first (invert order)
        line_nums = line_nums[::-1]
        i = 0
        while i < len(line_nums): # Iterate from last to first
            # Make sure we don't completely remove the last line
            if len(self.lines) == 1:
                cut_buffer.append(self.lines[0])
                self.lines[0] = Line()
                break
            line_no = line_nums[i] # Get the current line
            line = self.lines.pop(line_no) # Get and remove the line
            cut_buffer.append(line) # Put it in our temporary buffer
            self.move_y_cursors(line_no, -1) # Move all cursors below the current line up
            i += 1
        self.move_cursors() # Make sure cursors are in valid places
        # Reverse the buffer to get correct order and store it
        self.buffer = cut_buffer[::-1]
        self.store_action_state("cut")

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
        # Add a restore point if previous action != type
        self.store_action_state("type")

    def go_to_pos(self, line_no, col = 0):
        """Move primary cursor to line_no, col=0."""
        if line_no < 0:
            line_no = len(self.lines)-1
        else:
            line_no = line_no-1

        self.store_state()
        cur = self.cursor()
        if col != None:
            cur.x = col
        cur.y = line_no
        if cur.y >= len(self.lines):
            cur.y = len(self.lines)-1
        self.move_cursors()

    def find(self, what, findall = False):
        """Find what in data (from top to bottom). Adds a cursor when found."""
        if not what:
            return
        last_cursor = self.get_last_cursor()
        y = last_cursor.y

        found = False
        new_cursors = []
        # Loop through all lines starting from the last cursor
        while y < len(self.lines):
            line = self.lines[y]
            
            x_offset = 0 # Which character to begin searching from
            if y == last_cursor.y:
                # On the current line begin from the last cursor x pos
                x_offset = last_cursor.x
            
            # Find all occurances of search string
            pattern = re.escape(what) # Default to non regex pattern
            if self.config["regex_find"]:
                try: # Try to search with the actual regex
                    indices = [match.start() for match in re.finditer(what, str(line[x_offset:]))]
                except: # Revert to normal search
                    indices = [match.start() for match in re.finditer(pattern, str(line[x_offset:]))]
            else:
                indices = [match.start() for match in re.finditer(pattern, str(line[x_offset:]))]

            # Loop through the indices and add cursors if they don't exist yet
            for i in indices:
                new = Cursor(i+x_offset, y)
                if not self.cursor_exists(new):
                    found = True
                    new_cursors.append(new)
                    if not findall:
                        break
                if not new in new_cursors:
                    new_cursors.append(new)
            if found and not findall: break
            y += 1

        if not new_cursors:
            self.app.set_status("Can't find '" + what + "'")
            #self.last_find = ""
            return
        else:
            # If we only have one cursor, and it's not
            # where the first occurance is, just remove it
            if len(self.cursors) == 1 and self.cursors[0].tuple() != new_cursors[0].tuple():
                self.cursors = []
        self.last_find = what   # Only store string if it's really found

        # Add the new cursors
        for cursor in new_cursors:
            self.cursors.append(cursor)

        destination = self.get_last_cursor().y
        self.scroll_to_line(destination)
        self.store_action_state("find") # Store undo point

    def find_next(self):
        """Find next occurance."""
        what = self.last_find
        if what == "":
            cursor = self.cursor()
            search = "^([\w\-]+)"
            line = self.lines[cursor.y][cursor.x:]
            matches = re.match(search, line)
            if matches:
                what = matches.group(0)
            else:
                if line:
                    what = line[0]
            # Escape the data if regex is enabled
            if self.config["regex_find"]:
                what = re.escape(what)
                
            self.last_find = what
        self.find(what)

    def find_all(self):
        """Find all occurances."""
        self.find(self.last_find, True)

    def duplicate_line(self):
        """Copy current line and add it below as a new line."""
        curs = sorted(self.cursors, key = lambda c: (c.y, c.x))
        for cursor in curs:
            line = Line(self.lines[cursor.y])
            self.lines.insert(cursor.y+1, line)
            self.move_y_cursors(cursor.y, 1)
        self.move_cursors()
        self.store_action_state("duplicate_line")

    def handle_input(self, event):
        """Handle input."""
        if event.type == "mouse":
            return False
        key = event.key_code
        name = event.key_name
        if key == curses.KEY_RIGHT: self.arrow_right()        # Arrow Right
        elif key == curses.KEY_LEFT: self.arrow_left()        # Arrow Left
        elif key == curses.KEY_UP: self.arrow_up()            # Arrow Up
        elif key == curses.KEY_DOWN: self.arrow_down()        # Arrow Down
        elif key == curses.KEY_NPAGE: self.page_up()          # Page Up
        elif key == curses.KEY_PPAGE: self.page_down()        # Page Down

        elif key == 563: self.new_cursor_up()                 # Alt + Up
        elif key == 522: self.new_cursor_down()               # Alt + Down
        elif key == 542: self.new_cursor_left()               # Alt + Left
        elif key == 557: self.new_cursor_right()              # Alt + Right
        elif key == 552: self.push_up()                       # Alt + Page Up
        elif key == 547: self.push_down()                     # Alt + Page Down

        elif key == 269: self.undo()                          # F5
        elif key == 270: self.redo()                          # F6
        elif key == 273: self.toggle_line_nums()              # F9
        elif key == 274: self.toggle_line_ends()              # F10
        elif key == 275: self.toggle_highlight()              # F11
        elif key == 563: self.new_cursor_up()                 # Alt + up
        elif key == 522: self.new_cursor_down()               # Alt + down
        elif key == 542: self.new_cursor_left()               # Alt + left
        elif key == 557: self.new_cursor_right()              # Alt + right

        elif key == 331: self.insert()                        # Insert

        elif name == "^C": self.cut()                         # Ctrl + C
        elif name == "^W": self.duplicate_line()              # Ctrl + W
        elif name == "^V": self.insert()                      # Ctrl + V
        elif name == "^P": self.comment()                     # Ctrl + P
        elif name == "^D": self.find_next()                   # Ctrl + D
        elif name == "^A": self.find_all()                    # Ctrl + A
        elif name == "^?": self.backspace()                   # Backspace (fix for Mac)
        elif key == 544: self.jump_left()                     # Ctrl + Left
        elif key == 559: self.jump_right()                    # Ctrl + Right
        elif key == 565: self.jump_up()                       # Ctrl + Up
        elif key == 524: self.jump_down()                     # Ctrl + Down

        elif key == curses.KEY_HOME: self.home()              # Home
        elif key == curses.KEY_END: self.end()                # End
        elif key == curses.KEY_BACKSPACE: self.backspace()    # Backspace
        elif key == curses.KEY_DC: self.delete()              # Delete
        elif key == curses.KEY_ENTER: self.enter()            # Enter
        elif name == "^J": self.enter()                       # Enter (fallback for 'getch')
        elif key == "\t": self.tab()                          # Tab
        elif key == 353: self.untab()                         # Shift + Tab
        elif key == "\n": self.enter()                        # Enter
        elif name == "^[": self.escape()                      # Escape
        else:
            try:
                if type(key) == type(""):
                    self.type(key)
                elif not event.name.startswith("KEY_"):
                    self.type(name)
            except:
                pass

