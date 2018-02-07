# -*- encoding: utf-8
"""
Curses user interface.
"""

import os
import sys
import logging

from .prompt import Prompt, PromptBool, PromptFiltered, PromptFile, PromptAutocmp
from .key_mappings import key_map
from .color_manager_curses import ColorManager
from .statusbar import StatusBarManager

# Curses can't be imported yet but we'll
# predefine it to avoid confusing flake8
curses = None


class InputEvent:
    """Represents a keyboard or mouse event."""
    def __init__(self):
        self.type = None  # 'key' or 'mouse'
        self.key_name = ""
        self.key_code = None
        self.is_typeable = False
        self.curses_key_name = None
        self.mouse_code = None
        self.mouse_pos = (0, 0)
        self.logger = logging.getLogger("{0}.InputEvent".format(__name__))

    def parse_key_code(self, key_code):
        """Parse a key code (or character) from curses."""
        self.type = "key"
        self.key_code = key_code
        self.key_name = self._key_name(key_code)
        self.curses_key_name = self._curses_key_name(key_code)

    def set_key_name(self, name):
        """Manually set the event key name."""
        self.type = "key"
        self.key_name = name

    def parse_mouse_state(self, state):
        """Parse curses mouse events."""
        self.type = "mouse"
        self.mouse_code = state[4]
        self.mouse_pos = (state[1], state[2])

    def _key_name(self, key_code):
        """Return a normalized key name for key_code."""
        if isinstance(key_code, int):
            if key_code in key_map.keys():
                return key_map[key_code]
        curs_key_name = self._curses_key_name(key_code)
        if curs_key_name:
            if curs_key_name in key_map.keys():
                return key_map[curs_key_name]
            self.is_typeable = True  # We'll assume the key is typeable if it's not found in the key map
            return curs_key_name
        else:
            char = None
            if key_code in key_map.keys():
                return key_map[key_code]

            if sys.version_info[0] >= 3:
                if isinstance(key_code, str):
                    self.is_typeable = True
                    return key_code

            try:
                char = chr(key_code)
            except:
                pass
            if char is not None:
                self.is_typeable = True
                return char
        return False

    def _curses_key_name(self, key):
        """Return the curses key name for keys received from get_wch (and getch)."""
        # Handle multibyte get_wch input in Python 3.3
        if isinstance(key, str):
            return str(curses.keyname(ord(key)).decode("utf-8"))
        # Fallback to try and handle Python < 3.3
        # Special keys can also be ints on Python > 3.3
        if isinstance(key, int):  # getch fallback
            try:  # Try to convert to a curses key name
                name = str(curses.keyname(key).decode("utf-8"))
                return name
            except:  # Otherwise try to convert to a character
                return False
        return False

    def __str__(self):
        parts = [
            "type=" + str(self.type),
            "key_name=" + str(self.key_name),
            "key_code=" + str(self.key_code),
            "curses_key_name=" + str(self.curses_key_name),
            "mouse_code=" + str(self.mouse_code),
            "mouse_pos=" + str(self.mouse_pos),
        ]
        return " ".join(parts)


class UI:
    def __init__(self, app):
        self.app = app
        self.logger = logging.getLogger(__name__)
        self.statusbars = None
        self.bar_head = None
        self.bar_bottom = None
        self.screen = None
        self.current_yx = None
        self.text_input = None
        self.header_win = None
        self.status_win = None
        self.editor_win = None
        self.legend_win = None

    def init(self):
        """Set ESC delay and then import curses."""
        global curses
        # Set ESC detection time
        os.environ["ESCDELAY"] = str(self.app.config["app"]["escdelay"])
        termenv = os.environ["TERM"]
        if termenv.endswith("-256color") and self.app.config["app"].get("imitate_256color"):
            # Curses doesn't recognize 'screen-256color' or 'tmux-256color' as 256-color terminals.
            # These terminals all seem to be identical to xterm-256color, which is recognized.
            # Since this might have other consequences it's hidden behind a config flag.
            self.logger.debug("Changing terminal from '{0}' to 'xterm-256color'".format(termenv))
            os.environ["TERM"] = "xterm-256color"
        # Now import curses, otherwise ESCDELAY won't have any effect
        import curses
        self.logger.debug("Loaded curses {0}".format(curses.version.decode()))

        # Notify user if Pygments syntax highlighting isn't available
        try:
            import pygments  # noqa
        except:
            self.logger.info("Pygments not available, please install python3-pygments for proper syntax highlighting.")

    def run(self, func):
        """Run the application main function via the curses wrapper for safety."""
        curses.wrapper(func)

    def load(self, *args):
        """Setup curses."""
        # Log the terminal type
        self.termname = curses.termname().decode("utf-8")
        self.logger.debug("Loading UI for terminal: {0}".format(self.termname))

        self.screen = curses.initscr()
        self.colors = ColorManager(self.app)

        curses.raw()
        curses.noecho()

        try:
            # Hide the default cursor
            # Might fail on vt100 terminal emulators
            curses.curs_set(0)
        except:
            self.logger.warning("curses.curs_set(0) failed!")

        if "get_wch" not in dir(self.screen):
            self.logger.warning("Using old curses! Some keys and special characters might not work.")

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

    def setup_windows(self):
        """Initialize and layout windows."""
        # We are using curses.newwin instead of self.screen.subwin/derwin because
        # subwindows are getting a special treatment on resize. e.g., the legend
        # bar may automatically resize to one line if the window gets smaller.
        # Even after doing the layout by moving the legend window into its proper
        # place a call to resize() to restore the 2 line height will error out.
        # This does not happen with curses.newwin().
        #
        # https://anonscm.debian.org/cgit/collab-maint/ncurses.git/tree/ncurses/base/resizeterm.c#n274
        # https://anonscm.debian.org/cgit/collab-maint/ncurses.git/tree/ncurses/base/wresize.c#n87
        self.text_input = None
        offset_top = 0
        offset_bottom = 0
        y, x = self.screen.getmaxyx()
        config = self.app.config["display"]

        if config["show_top_bar"]:
            offset_top += 1
            if self.header_win is None:
                self.header_win = curses.newwin(1, x, 0, 0)
            elif self.header_win.getmaxyx()[1] != x:
                # Header bar don't ever need to move
                self.header_win.resize(1, x)
            self.header_win.bkgdset(" ", self.colors.get("status_top"))

        if config["show_bottom_bar"]:
            offset_bottom += 1
            if self.status_win is None:
                self.status_win = curses.newwin(1, x, y - offset_bottom, 0)
            else:
                self.status_win.mvwin(y - offset_bottom, 0)
                if self.status_win.getmaxyx()[1] != x:
                    self.status_win.resize(1, x)
            self.status_win.bkgdset(" ", self.colors.get("status_bottom"))

        if config["show_legend"]:
            offset_bottom += 2
            if self.legend_win is None:
                self.legend_win = curses.newwin(2, x, y - offset_bottom, 0)
            else:
                self.legend_win.mvwin(y - offset_bottom, 0)
                if self.legend_win.getmaxyx()[1] != x:
                    self.legend_win.resize(2, x)
            self.legend_win.bkgdset(" ", self.colors.get("legend"))

        if self.editor_win is None:
            self.editor_win = curses.newwin(y - offset_top - offset_bottom, x, offset_top, 0)
        else:
            # Not sure why editor implements this on its own
            # and if it's a good thing or not.
            self.app.get_editor().resize((y - offset_top - offset_bottom, x))
            self.app.get_editor().move_win((offset_top, 0))
            # self.editor_win.mvwin(offset_top, 0)
            # self.editor_win.resize(y - offset_top - offset_bottom, x)
        self.editor_win.bkgdset(" ", self.colors.get("editor"))

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
        self.setup_windows()
        self.screen.noutrefresh()
        self.statusbars.force_redraw()

    def check_resize(self):
        """Check if terminal has resized and resize if needed."""
        yx = self.screen.getmaxyx()
        if self.current_yx != yx:
            self.current_yx = yx
            self.resize(yx)

    def refresh_status(self):
        """Refresh status windows."""
        if not self.statusbars:
            self.statusbars = StatusBarManager(self.app)
            # FIXME: This will not react to removal of statusbars in config without restart
            if self.app.config["display"]["show_top_bar"]:
                self.bar_head = self.statusbars.add(self.header_win, "status_top")
            if self.app.config["display"]["show_bottom_bar"]:
                self.bar_bottom = self.statusbars.add(self.status_win, "status_bottom")
        self.statusbars.render()
        if self.app.config["display"]["show_legend"]:
            self.show_legend()

    def show_legend(self):
        """Show keyboard legend."""
        # Only the most important commands are displayed in the legend
        legend_commands = [
            ("save", "Save"),
            ("save_file_as", "Save as"),
            ("reload_file", "Reload"),
            ("undo", "Undo"),
            ("redo", "Redo"),
            ("prompt_open_file", "Open"),
            ("close", "Close"),
            ("copy", "Copy"),
            ("cut", "Cut"),
            ("insert", "Paste"),
            ("find", "Find"),
            ("find_next", "Find next"),
            ("find_all", "Find all"),
            ("duplicate_line", "Duplicate line"),
            ("escape", "Single cursor"),
            ("go_to", "Go to"),
            ("run_command", "Run command"),
            ("toggle_mouse", "Mouse mode"),
            ("help", "Help"),
            ("exit", "Exit"),
        ]

        # Get the key bindings for the commands
        keys = []
        for command in legend_commands:
            for item in self.app.config.keymap:
                if item["command"] == command[0]:
                    key = item["keys"][0]
                    keys.append((key, command[1]))
                    break

        # Render the keys
        self.legend_win.erase()
        x = 0
        y = 0
        max_y = 1
        for item in keys:
            key = item[0]
            label = item[1]
            key = key.upper()
            # Format some key names to look better
            if key.startswith("CTRL+"):
                key = "^"+key[5:]
            if key == "ESCAPE":
                key = "ESC"

            if x+len(" ".join((key, label))) >= self.get_size()[0]:
                x = 0
                y += 1
                if y > max_y:
                    break
            self.legend_win.addstr(y, x, key.upper(), curses.A_REVERSE)
            x += len(key)
            self.legend_win.addstr(y, x, " "+label)
            x += len(label)+2
        self.legend_win.refresh()

    def _query(self, text, initial="", cls=Prompt, inst=None):
        """Ask for text input via the status bar."""

        # Disable render blocking
        blocking = self.app.block_rendering
        self.app.block_rendering = 0

        # Create our text input
        if not inst:
            self.text_input = cls(self.app, self.status_win)
        else:
            self.text_input = inst
        self.text_input.set_config(self.app.config["editor"].copy())
        self.text_input.set_input_source(self.get_input)
        self.text_input.init()

        # Get input from the user
        out = self.text_input.get_input(text, initial)

        # Restore render blocking
        self.app.block_rendering = blocking

        return out

    def query(self, text, initial=""):
        """Get a single line input string from the user."""
        result = self._query(text, initial)
        return result

    def query_bool(self, text, default=False):
        """Get a boolean from the user."""
        result = self._query(text, default, PromptBool)
        return result

    def query_filtered(self, text, initial="", handler=None):
        """Get an arbitrary string from the user with input filtering."""
        prompt_inst = PromptFiltered(self.app, self.status_win, handler=handler)
        result = self._query(text, initial, inst=prompt_inst)
        return result

    def query_file(self, text, initial=""):
        """Get a file path from the user."""
        result = self._query(text, initial, PromptFile)
        return result

    def query_autocmp(self, text, initial="", completions=[]):
        """Get an arbitrary string from the user with autocomplete."""
        prompt_inst = PromptAutocmp(self.app, self.status_win, initial_items=completions)
        result = self._query(text, initial, inst=prompt_inst)
        return result

    def get_input(self, blocking=True):
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
            if blocking:
                self.screen.nodelay(0)
            else:
                self.screen.nodelay(1)
            char = input_func()
        except KeyboardInterrupt:
            # Handle KeyboardInterrupt as Ctrl+C
            event.set_key_name("ctrl+c")
            return event
        except:
            # No input available
            return False
        finally:
            self.screen.nodelay(0)

        if char and char != -1:
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
            self.logger.error("curses.getmouse() failed!", exc_info=True)
            return False

        # Translate the coordinates to the editor coordinate system
        return self._translate_mouse_to_editor(mouse_state)

    def _translate_mouse_to_editor(self, state):
        """Translate the screen coordinates to position in the editor view."""
        editor = self.app.get_editor()
        x, y = (state[1], state[2])
        if self.app.config["display"]["show_top_bar"]:
            y -= 1
        x -= editor.line_offset() - editor.x_scroll
        if x < 0:
            x = 0
        y += editor.y_scroll
        return (state[0], x, y, state[3], state[4])
