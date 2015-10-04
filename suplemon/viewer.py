# -*- encoding: utf-8
"""
Text viewer component subclassed by Editor.
"""

import os
import sys
import imp
import curses
import logging


from .line import Line
from .cursor import Cursor
from .themes import scope_to_pair

try:
    import pygments.lexers
    from .lexer import Lexer
except ImportError:
    pygments = False


class Viewer:
    def __init__(self, app, window):
        """
        Handle Viewer initialization

        :param App app: The main App class of Suplemon
        :param Window window: The ui window to use for the viewer
        """
        self.app = app
        self.window = window
        self.logger = logging.getLogger(__name__)
        self.config = {}
        self.data = ""
        self.lines = [Line()]
        self.file_extension = ""

        # Map special extensions to generic ones for highlighting
        self.extension_map = {
            "scss": "css",
            "less": "css",
        }
        self.show_line_ends = True

        self.cursor_style = curses.A_UNDERLINE

        self.y_scroll = 0
        self.x_scroll = 0
        self.cursors = [Cursor()]

        # Lexer for translating tokens to strings
        self.lexer = None
        # Built in syntax definition (for commenting etc.)
        self.syntax = None
        # Normal Pygments lexer
        self.pygments_syntax = None

        self.setup_linelight()
        if self.app.config["editor"]["show_highlighting"]:
            self.setup_highlight()

    def setup_linelight(self):
        """Setup line based highlighting."""
        ext = self.file_extension
        # Check if a file extension is redefined
        # Maps e.g. 'scss' to 'css'
        if ext in self.extension_map.keys():
            ext = self.extension_map[ext]  # Use it
        curr_path = os.path.dirname(os.path.realpath(__file__))

        filename = ext + ".py"
        path = os.path.join(curr_path, "linelight", filename)
        module = False
        if os.path.isfile(path):
            try:
                module = imp.load_source(ext, path)
            except:
                self.logger.error("Failed to load syntax file '{0}'!".format(path), exc_info=True)
        else:
            return False

        if not module or "Syntax" not in dir(module):
            self.logger.error("File doesn't match API!")
            return False
        self.syntax = module.Syntax()

    def setup_highlight(self):
        """Setup Pygments based highlighting."""
        if not pygments:
            # If Pygments lib not available
            self.logger.info("Pygments not available, please install it for proper syntax highlighting.")
            return False
        self.lexer = Lexer(self.app)
        ext = self.file_extension.lower()
        if not ext:
            return False
        # Check if a file extension is redefined
        # Maps e.g. 'scss' to 'css'
        if ext in self.extension_map.keys():
            ext = self.extension_map[ext]  # Use it
        try:
            self.pygments_syntax = pygments.lexers.get_lexer_by_name(ext)
            self.logger.info("Loaded Pygments lexer '{0}'.".format(ext))
        except:
            self.logger.warning("Failed to load Pygments lexer '{0}'.".format(ext))
            return False
        if ext == "php":
            # Hack to highlight PHP even without <?php ?> tags
            self.pygments_syntax.options.update({"startinline": 1})
            self.pygments_syntax.startinline = 1

    def size(self):
        """Get editor size (x,y). (Deprecated, use get_size)."""
        self.logger.warning("size() is deprecated, please use get_size()")
        return self.get_size()

    def cursor(self):
        """Return the main cursor. (Deprecated, use get_cursor)"""
        self.logger.warning("cursor() is deprecated, please use get_cursor()")
        return self.get_cursor()

    def get_size(self):
        """Get editor size (x,y)."""
        y, x = self.window.getmaxyx()
        return (x, y)

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
            if highest is None or cursor.y < highest.y:
                highest = cursor
        return highest

    def get_last_cursor(self):
        """Get the last cursor."""
        lowest = None
        for cursor in self.cursors:
            if lowest is None:
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

    def get_line(self, n):
        """Return line at index n.

        :param n: Index of line to get.
        :return: The Line instance.
        """
        return self.lines[n]

    def get_lines_with_cursors(self):
        """Return all line indices that have cursors.

        :return: A list of line numbers that have cursors.
        :rtype: list
        """
        line_nums = []
        for cursor in self.cursors:
            if cursor.y not in line_nums:
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
            if isinstance(line, str):
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
        self.set_cursor_style(self.config["cursor_style"])

    def set_cursor_style(self, cursor_style):
        """Set cursor style.

        :param str cursor_style: Cursor type, either 'underline' or 'reverse'.
        """
        if cursor_style == "underline":
            self.cursor_style = curses.A_UNDERLINE
        elif cursor_style == "reverse":
            self.cursor_style = curses.A_REVERSE
        else:
            return False
        return True

    def set_cursor(self, cursor):
        self.logger.warning("set_cursor is deprecated, use set_cursor_style instead.")
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
            if self.app.config["editor"]["show_highlighting"]:
                self.setup_highlight()

    def add_cursor(self, cursor):
        """Add a new cursor. Accepts a x,y tuple or a Cursor instance."""
        self.cursors.append(Cursor(cursor))

    def pad_lnum(self, n):
        """Pad line number with zeroes."""
        # TODO: move to helpers
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
        self.window.erase()
        i = 0
        max_y = self.get_size()[1]
        max_len = self.max_line_length()
        # Iterate through visible lines
        while i < max_y:
            x_offset = self.line_offset()
            lnum = i + self.y_scroll
            if lnum >= len(self.lines):  # Make sure we have a line to show
                break
            # Get line for current row
            line = self.lines[lnum]
            if self.config["show_line_nums"]:
                curs_color = curses.color_pair(line.number_color)
                self.window.addstr(i, 0, self.pad_lnum(lnum+1)+" ", curs_color)

            pos = (x_offset, i)
            try:
                self.render_line_contents(line, pos, x_offset, max_len)
            except:
                self.logger.error("Failed rendering line #{0} @{1} DATA:'{2}'!".format(lnum+1, pos, line),
                                  exc_info=True)
            i += 1
        self.render_cursors()

    def render_line_contents(self, line, pos, x_offset, max_len):
        """Render the contents of a line to the screen

        Renders a line to the screen with the appropriate rendering method
        based on settings.

        :param line: Line instance to render.
        :param pos: Position (x, y) for beginning of line.
        :param x_offset: Offset from left edge of screen. Currently same as x position.
        :param max_len: Maximum amount of chars that will fit on screen.
        """
        show_highlighting = self.app.config["editor"]["show_highlighting"]
        if pygments and show_highlighting and self.pygments_syntax and self.app.themes.current_theme:
            self.render_line_pygments(line, pos, x_offset, max_len)
        elif self.app.config["editor"]["show_line_colors"]:
            self.render_line_linelight(line, pos, x_offset, max_len)
        else:
            self.render_line_normal(line, pos, x_offset, max_len)

    def render_line_pygments(self, line, pos, x_offset, max_len):
        """Render line with Pygments syntax highlighting."""
        x, y = pos
        line_data = line.get_data()
        # Lazily prepare and slice the line,
        # even though it affects highlighting.
        line_data = self._prepare_line_for_rendering(line_data,
                                                     max_len,
                                                     no_wspace=True)
        # TODO:
        # 1) The line should not be prepared for rendering like this
        #    because it can get sliced. Sliced lines won't always get
        #    completely highlighted (partial words). Syntax highlighting
        #    should be done first and then only render visible words.
        # 2) Additionaly highlighing should be done for all lines at once
        #    and tokens should be cached in line instances. That way we can
        #    support multi line comment syntax etc. It should also perform
        #    better, since we only need to re-highlight lines when they change.
        tokens = self.lexer.lex(line_data, self.pygments_syntax)
        for token in tokens:
            if token[1] == "\n":
                break
            scope = token[0]
            text = self.replace_whitespace(token[1])
            if token[1].isspace() and not self.app.ui.limited_colors:
                # Color visible whitespace with gray
                # TODO: get whitespace color from theme
                pair = 9  # Gray text on normal background
                curs_color = curses.color_pair(pair)
                self.window.addstr(y, x_offset, text, curs_color)
            else:
                # Color with pygments
                settings = self.app.themes.get_scope(scope)
                pair = scope_to_pair.get(scope)
                if settings and pair is not None:
                    fg = int(settings.get("foreground") or -1)
                    bg = int(settings.get("background") or -1)
                    curses.init_pair(pair, fg, bg)
                    curs_color = curses.color_pair(pair)
                    self.window.addstr(y, x_offset, text, curs_color)
                else:
                    self.window.addstr(y, x_offset, text)
            x_offset += len(text)

    def render_line_linelight(self, line, pos, x_offset, max_len):
        """Render line with naive line based highlighting."""
        x, y = pos
        line_data = line.get_data()
        line_data = self._prepare_line_for_rendering(line_data, max_len)
        curs_color = curses.color_pair(self.get_line_color(line))
        self.window.addstr(y, x_offset, line_data, curs_color)

    def render_line_normal(self, line, pos, x_offset, max_len):
        """Render line without any highlighting."""
        x, y = pos
        line_data = line.get_data()
        line_data = self._prepare_line_for_rendering(line_data, max_len)
        self.window.addstr(y, x_offset, line_data)

    def replace_whitespace(self, data):
        """Replace unsafe whitespace with alternative safe characters

        Replace unsafe whitespace with normal space or visible replacement.
        For example tab characters make cursors go out of sync with line
        contents.
        """
        for key in self.config["white_space_map"].keys():
            char = " "
            if self.config["show_white_space"]:
                char = self.config["white_space_map"][key]
            data = data.replace(key, char)
        # Remove newlines, they cause curses errors
        data = data.replace("\n", "")
        return data

    def _prepare_line_for_rendering(self, line_data, max_len, no_wspace=False):
        if self.show_line_ends:
            line_data += self.config["line_end_char"]
        line_data = self._slice_line_for_rendering(line_data, max_len)
        if not no_wspace:
            line_data = self.replace_whitespace(line_data)

        # Use unicode support on Python 3.3 and higher
        if sys.version_info[0] == 3 and sys.version_info[1] > 2:
            line_data = line_data.encode("utf-8")
        return line_data

    def _slice_line_for_rendering(self, line, max_len):
        """Return sliced line data.

        Returns what's left of line data after scrolling it horizontally
        and removing excess characters from the end.

        :param line: Line to slice.
        :param max_len: Maximum length of line.
        :return: Sliced line.
        """
        line = line[min(self.x_scroll, len(line)):]
        if not line:
            return ""
        # Clamp line length to view width
        line = line[:min(len(line), max_len)]
        return line

    def render_cursors(self):
        """Render editor window cursors."""
        max_x, max_y = self.get_size()
        for cursor in self.cursors:
            x = cursor.x - self.x_scroll + self.line_offset()
            y = cursor.y - self.y_scroll
            if y < 0:
                continue
            if y >= max_y:
                break
            if x < self.line_offset():
                continue
            if x > max_x-1:
                continue
            self.window.chgat(y, cursor.x+self.line_offset()-self.x_scroll, 1, self.cursor_style)

    def refresh(self):
        """Refresh the editor curses window."""
        self.window.refresh()

    def resize(self, yx=None):
        """Resize the UI."""
        if not yx:
            yx = self.window.getmaxyx()
        self.window.resize(yx[0], yx[1])
        self.move_cursors()
        self.refresh()

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

    def scroll_to_line(self, line_no):
        """Center the viewport on line_no."""
        if line_no >= len(self.lines):
            line_no = len(self.lines)-1
        new_y = line_no - int(self.get_size()[1] / 2)
        if new_y < 0:
            new_y = 0
        self.y_scroll = new_y

    def move_win(self, yx):
        """Move the editor window to position yx."""
        # Must try & catch since mvwin might
        # crash with incorrect coordinates
        try:
            self.window.mvwin(yx[0], yx[1])
        except:
            self.logger.warning("Moving window failed!", exc_info=True)

    def move_y_scroll(self, delta):
        """Add delta the y scroll axis scroll"""
        self.y_scroll += delta

    def move_cursors(self, delta=None, noupdate=False):
        """Move all cursors with delta. To avoid refreshing the screen set noupdate to True."""
        for cursor in self.cursors:
            if delta:
                if delta[0] != 0 and cursor.x >= 0:
                    cursor.move_right(delta[0])
                if delta[1] != 0 and cursor.y >= 0:
                    cursor.move_down(delta[1])

            if cursor.x < 0:
                cursor.x = 0
            if cursor.y < 0:
                cursor.y = 0
            if cursor.y >= len(self.lines)-1:
                cursor.y = len(self.lines)-1
            if cursor.x >= len(self.lines[cursor.y]):
                cursor.x = len(self.lines[cursor.y])
            elif cursor.persistent_x != cursor.x:
                # Retain the 'desired' x coordinate
                cursor.x = min(cursor.persistent_x, len(self.lines[cursor.y]))

        cur = self.get_cursor()  # Main cursor
        size = self.get_size()
        offset = self.line_offset()
        # Check if we should scroll horizontally
        if cur.x - self.x_scroll+offset > size[0] - 1:
            # -1 to allow space for cursor at line end
            self.x_scroll = len(self.lines[cur.y]) - size[0]+offset+1
        if cur.x - self.x_scroll < 0:
            self.x_scroll -= abs(cur.x - self.x_scroll)  # FIXME
        if cur.x - self.x_scroll+offset < offset:
            self.x_scroll -= 1
        if not noupdate:
            self.purge_cursors()

    def move_x_cursors(self, line, col, delta):
        """Move all cursors starting at line and col with delta on the x axis."""
        for cursor in self.cursors:
            if cursor.y == line:
                if cursor.x > col:
                    cursor.move_right(delta)

    def move_y_cursors(self, line, delta, exclude=None):
        """Move all cursors starting at line and col with delta on the y axis.
        Exclude a cursor by passing it via the exclude argument."""
        for cursor in self.cursors:
            if cursor == exclude:
                continue
            if cursor.y > line:
                cursor.move_down(delta)

    def cursor_exists(self, cursor):
        """Check if a given cursor exists."""
        return cursor.tuple() in [cur.tuple() for cur in self.cursors]

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
