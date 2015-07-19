# -*- encoding: utf-8
"""
Curses user interface.
"""

import os

from helpers import *


class InputEvent:
    """Represents a keyboard or mouse event."""
    def __init__(self):
        self.type = None  # 'key' or 'mouse'
        self.key_name = None
        self.key_code = None
        self.mouse_code = None
        self.mouse_pos = (0, 0)

    def parse_key_code(self, code):
        """Parse a key namoe or code from curses."""
        self.type = "key"
        self.key_code = code
        self.key_name = self._key_name(code)

    def set_key_name(self, name):
        """Manually set the event key name."""
        self.type = "key"
        self.key_name = name

    def parse_mouse_state(self, state):
        """Parse curses mouse events."""
        self.type = "mouse"
        self.mouse_code = state[4]
        self.mouse_pos = (state[1], state[2])

    def _key_name(self, key):
        """Return the curses key name for keys received from get_wch (and getch)."""
        # Handle multibyte get_wch input in Python 3.3
        if isinstance(key, str):
            return str(curses.keyname(ord(key)).decode("utf-8"))
        # Fallback to try and handle Python < 3.3
        if isinstance(key, int):  # getch fallback
            try:  # Try to convert to a curses key name
                return str(curses.keyname(key).decode("utf-8"))
            except:  # Otherwise try to convert to a character
                try:
                    return chr(key)
                except:
                    return False
        return key

    def __str__(self):
        parts = [
            str(self.type),
            str(self.key_name),
            str(self.key_code),
            str(self.mouse_code),
            str(self.mouse_pos)
        ]
        return " ".join(parts)


class UI:
    def __init__(self, app):
        self.app = app
        self.warned_old_curses = 0

    def init(self):
        """Set ESC delay and then import curses."""
        global curses
        # Set ESC detection time
        os.environ["ESCDELAY"] = str(self.app.config["app"]["escdelay"])
        # Now import curses, otherwise ESCDELAY won't have any effect
        import curses
        import curses.textpad

    def run(self, func):
        """Run the application main function via the curses wrapper for safety."""
        curses.wrapper(func)

    def load(self, *args):
        """Setup curses."""
        # Log the terminal type
        self.app.log("Loading UI for terminal: " + curses.termname().decode("utf-8"), LOG_INFO)

        self.screen = curses.initscr()
        self.setup_colors()

        curses.cbreak()
        curses.noecho()
        try:
            # Might fail on vt100 terminal emulators
            curses.curs_set(0)
        except:
            self.app.log("curses.curs_set(0) failed!", LOG_WARNING)

        self.screen.keypad(1)

        self.current_yx = self.screen.getmaxyx()  # For checking resize
        self.setup_mouse()
        self.setup_windows()

    def unload(self):
        """Unload curses."""
        curses.endwin()

    def setup_mouse(self):
        # Mouse support
        curses.mouseinterval(10)
        if self.app.config["editor"]["use_mouse"]:
            curses.mousemask(-1)  # All events
        else:
            curses.mousemask(0)  # All events

    def setup_colors(self):
        """Initialize color support and define colors."""
        curses.start_color()
        try:
            curses.use_default_colors()
        except:
            self.app.logger.log("Failed to load curses default colors. You could try 'export TERM=xterm-256color'.")
            return False

        # Default foreground color (could also be set to curses.COLOR_WHITE)
        fg = -1
        # Default background color (could also be set to curses.COLOR_BLACK)
        bg = -1

        # This gets colors working in TTY's as well as terminal emulators
        # curses.init_pair(10, -1, -1) # Default (white on black)
        # Colors for xterm (not xterm-256color)
        # Dark Colors
        curses.init_pair(0, curses.COLOR_BLACK, bg)      # 0 Black
        curses.init_pair(1, curses.COLOR_RED, bg)        # 1 Red
        curses.init_pair(2, curses.COLOR_GREEN, bg)      # 2 Green
        curses.init_pair(3, curses.COLOR_YELLOW, bg)     # 3 Yellow
        curses.init_pair(4, curses.COLOR_BLUE, bg)       # 4 Blue
        curses.init_pair(5, curses.COLOR_MAGENTA, bg)    # 5 Magenta
        curses.init_pair(6, curses.COLOR_CYAN, bg)       # 6 Cyan
        curses.init_pair(7, fg, bg)                      # White on Black
        curses.init_pair(8, fg, curses.COLOR_BLACK)  # White on Black (Line number color)

        # Nicer shades of same colors (if supported)
        if curses.can_change_color():
            try:
                # TODO: Define RGB for these to avoid getting
                # different results in different terminals
                # xterm-256color chart http://www.calmar.ws/vim/256-xterm-24bit-rgb-color-chart.html
                curses.init_pair(0, 242, bg)  # 0 Black
                curses.init_pair(1, 204, bg)  # 1 Red
                curses.init_pair(2, 119, bg)  # 2 Green
                curses.init_pair(3, 221, bg)  # 3 Yellow
                curses.init_pair(4, 69, bg)   # 4 Blue
                curses.init_pair(5, 171, bg)  # 5 Magenta
                curses.init_pair(6, 81, bg)   # 6 Cyan
                curses.init_pair(7, 15, bg)   # 7 White
                # curses.init_pair(8, 8, bg)   # 8 Gray (Line number color)
                curses.init_pair(8, 8, curses.COLOR_BLACK)  # 8 Gray on Black (Line number color)
            except:
                self.app.logger.log("Enhanced colors failed to load. You could try 'export TERM=xterm-256color'.")
                self.app.config["editor"]["show_highlighting"] = False
        else:
            self.app.logger.log("Enhanced colors not supported. You could try 'export TERM=xterm-256color'.", LOG_INFO)
            self.app.config["editor"]["show_highlighting"] = False

        self.app.themes.use(self.app.config["editor"]["theme"])

    def setup_windows(self, resize=False):
        """Initialize windows."""
        yx = self.screen.getmaxyx()
        self.text_input = None
        self.header_win = curses.newwin(1, yx[1], 0, 0)
        self.status_win = curses.newwin(1, yx[1], yx[0]-1, 0)

        # Test for new curses
        if "get_wch" not in dir(self.header_win):
            # Notify only once
            if not self.warned_old_curses:
                self.app.log("Using old curses! Some keys and special characters might not work.", LOG_WARNING)
                self.warned_old_curses = 1

        y_sub = 0
        y_start = 0
        if self.app.config["display"]["show_top_bar"]:
            y_sub += 1
            y_start = 1
        if self.app.config["display"]["show_bottom_bar"]:
            y_sub += 1
        if self.app.config["display"]["show_legend"]:
            y_sub += 2
        self.editor_win = curses.newwin(yx[0]-y_sub, yx[1], y_start, 0)
        if self.app.config["display"]["show_top_bar"]:
            self.legend_win = curses.newwin(2, yx[1], yx[0]-y_sub+1, 0)
        else:
            self.legend_win = curses.newwin(2, yx[1], yx[0]-y_sub, 0)

        if resize:
            self.app.get_editor().resize((yx[0]-y_sub, yx[1]))
            self.app.get_editor().move_win((y_start, 0))

    def get_size(self):
        """Get terminal size."""
        y, x = self.screen.getmaxyx()
        return (x, y)

    def update(self):
        self.check_resize()

    def refresh(self):
        self.refresh_status()
        self.screen.refresh()

    def resize(self, yx=None):
        """Resize UI to yx."""
        if yx is None:
            yx = self.screen.getmaxyx()
        self.screen.erase()
        curses.resizeterm(yx[0], yx[1])
        self.setup_windows(resize=True)
        self.screen.refresh()

    def check_resize(self):
        """Check if terminal has resized."""
        yx = self.screen.getmaxyx()
        if self.current_yx != yx:
            self.current_yx = yx
            self.resize(yx)

    def refresh_status(self):
        """Refresh status windows."""
        if self.app.config["display"]["show_top_bar"]:
            self.show_top_status()
        if self.app.config["display"]["show_legend"]:
            self.show_legend()
        if self.app.config["display"]["show_bottom_bar"]:
            self.show_bottom_status()

    def show_top_status(self):
        """Show top status row."""
        self.header_win.erase()
        size = self.get_size()
        display = self.app.config["display"]
        head_parts = []
        if display["show_app_name"]:
            name_str = "Suplemon Editor v" + self.app.version + " -"
            if self.app.config["app"]["use_unicode_symbols"]:
                logo = "\u2688"      # Simple lemon (filled)
                name_str = " " + logo + " " + name_str
            head_parts.append(name_str)

        # Add module statuses to the status bar
        for name in self.app.modules.modules.keys():
            module = self.app.modules.modules[name]
            if module.options["status"] == "top":
                status = module.get_status()
                if status:
                    head_parts.append(status)

        if display["show_file_list"]:
            head_parts.append(self.file_list_str())

        head = " ".join(head_parts)
        head = head + (" " * (self.screen.getmaxyx()[1]-len(head)-1))
        if len(head) >= size[0]:
            head = head[:size[0]-1]
        if self.app.config["display"]["invert_status_bars"]:
            self.header_win.addstr(0, 0, head, curses.color_pair(0) | curses.A_REVERSE)
        else:
            self.header_win.addstr(0, 0, head, curses.color_pair(0))
        self.header_win.refresh()

    def file_list_str(self):
        """Return rotated file list beginning at current file as a string."""
        curr_file_index = self.app.current_file_index()
        files = self.app.get_files()
        file_list = files[curr_file_index:] + files[:curr_file_index]
        str_list = []
        no_write_symbol = ["!", "\u2715"][self.app.config["app"]["use_unicode_symbols"]]
        is_changed_symbol = ["*", "\u2732"][self.app.config["app"]["use_unicode_symbols"]]
        for f in file_list:
            prepend = [no_write_symbol, ""][f.is_writable()]
            append = ["", is_changed_symbol][f.is_changed()]
            fname = prepend + f.name + append
            if not str_list:
                str_list.append("[" + fname + "]")
            else:
                str_list.append(fname)
        return " ".join(str_list)

    def show_bottom_status(self):
        """Show bottom status line."""
        editor = self.app.get_editor()
        size = self.get_size()
        cur = editor.get_cursor()
        data = "@ " + str(cur[0]) + "," + str(cur[1]) + " " + \
            "cur:" + str(len(editor.cursors)) + " " + \
            "buf:" + str(len(editor.get_buffer()))
        if self.app.config["app"]["debug"]:
            data += " cs:"+str(editor.current_state)+" hist:"+str(len(editor.history))  # Undo / Redo debug
        # if editor.last_find:
        #     find = editor.last_find
        #     if len(find) > 10:find = find[:10]+"..."
        #     data = "find:'"+find+"' " + data

        # Add module statuses to the status bar
        for name in self.app.modules.modules.keys():
            module = self.app.modules.modules[name]
            if module.options["status"] == "bottom":
                data += " " + module.get_status()

        self.status_win.erase()
        status = self.app.get_status()
        extra = size[0] - len(status+data) - 1
        line = status+(" "*extra)+data

        if len(line) >= size[0]:
            line = line[:size[0]-1]
        if self.app.config["display"]["invert_status_bars"]:
            self.status_win.addstr(0, 0, line, curses.color_pair(0) | curses.A_REVERSE)
        else:
            self.status_win.addstr(0, 0, line, curses.color_pair(0))

        self.status_win.refresh()

    def show_legend(self):
        """Show keyboard legend."""
        # TODO: get from key bindings
        self.legend_win.erase()
        keys = [
            ("^S", "Save"),
            ("F1", "Save as"),
            ("F2", "Reload"),
            ("F5", "Undo"),
            ("F6", "Redo"),
            ("^O", "Open"),
            ("^C", "Cut"),
            ("^V", "Paste"),
            ("^F", "Find"),
            ("^D", "Find next"),
            ("^A", "Find all"),
            ("^W", "Duplicate line"),
            ("ESC", "Single cursor"),
            ("^G", "Go to"),
            ("^E", "Run command"),
            ("F8", "Mouse mode"),
            ("^X", "Exit"),
        ]
        x = 0
        y = 0
        max_y = 1
        for key in keys:
            if x+len(" ".join(key)) >= self.get_size()[0]:
                x = 0
                y += 1
                if y > max_y:
                    break
            self.legend_win.addstr(y, x, key[0], curses.A_REVERSE)
            x += len(key[0])
            self.legend_win.addstr(y, x, " "+key[1])
            x += len(key[1])+2
        self.legend_win.refresh()

    def show_capture_status(self, s="", value=""):
        """Show status when capturing input."""
        self.status_win.erase()
        self.status_win.addstr(0, 0, s, curses.A_REVERSE)
        self.status_win.addstr(0, len(s), value)

    def _process_query_key(self, key):
        """Process keystrokes from the Textbox window."""
        # TODO: implement this to improve interacting in the input box
        if self.app.config["app"]["debug"]:
            self.app.log("Query key input:"+str(key), LOG_INFO)
        return key

    def _query(self, text, initial=""):
        """Ask for text input via the status bar."""
        self.show_capture_status(text, initial)
        self.text_input = curses.textpad.Textbox(self.status_win)
        try:
            out = self.text_input.edit(self._process_query_key)
        except:
            return False

        # If input begins with prompt, remove the prompt text
        if len(out) >= len(text):
            if out[:len(text)] == text:
                out = out[len(text):]
        if len(out) > 0 and out[-1] == " ":
            out = out[:-1]
        out = out.rstrip("\r\n")
        return out

    def query(self, text, initial=""):
        """Get a single line input string from the user."""
        result = self._query(text, initial)
        return result

    def query_bool(self, text, default=False):
        """Get a boolean from the user."""
        indicator = "[y/N]"
        initial = ""
        if default:
            indicator = "[Y/n]"
            initial = "y"

        result = self._query(text + " " + indicator, initial)
        if result in ["Y", "y"]:
            return True
        if result == "":
            return default
        return False

    def get_input(self):
        """Get an input event from keyboard or mouse. Returns an InputEvent instance or False."""
        event = InputEvent()  # Initialize new empty event
        char = False
        input_func = None
        if "get_wch" in dir(self.screen):
            # New Python 3.3 curses method for wide characters.
            input_func = self.screen.get_wch
        else:
            # Old Python fallback. No multibyte characters.
            input_func = self.screen.getch
        try:
            char = input_func()
        except KeyboardInterrupt:
            # Handle KeyboardInterrupt as Ctrl+C
            event.set_key_name("^C")
            return event
        except:
            # No input available
            return False

        if char:
            if self.is_mouse(char):
                state = self.get_mouse_state()
                if state:
                    event.parse_mouse_state(state)
                    return event
            else:
                event.parse_key_code(char)
                return event
        return False

    def is_mouse(self, key):
        """Check for mouse events"""
        return key == curses.KEY_MOUSE

    def get_mouse_state(self):
        """Get the mouse event data."""
        try:
            mouse_state = curses.getmouse()
        except:
            self.app.log(get_error_info())
            return False
        # Translate the coordinates to the editor coordinate system
        return self._translate_mouse_to_editor(mouse_state)

    def _translate_mouse_to_editor(self, state):
        """Translate the screen coordinates to position in the editor view."""
        editor = self.app.get_editor()
        x, y = (state[1], state[2])
        if self.app.config["display"]["show_top_bar"]:
            y -= 1
        x -= editor.line_offset()
        y += editor.y_scroll
        return (state[0], x, y, state[3], state[4])
