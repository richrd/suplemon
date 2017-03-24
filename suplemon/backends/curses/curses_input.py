

from ..base_input import InputBackend
from ..base_input_event import InputEvent

from .curses_key_map import key_map as curses_key_map


curses = None


class CursesInput(InputBackend):
    """
    Curses implementation of InputBackend.
    """
    def init(self):
        # Root window used for interfacing with curses
        self._root = None

        # Encoding used to decode curses input
        self._encoding = "utf-8"

        # Wether keyboard interrupts should be converted to ctrl+c
        self._handle_kbd_interrupt = True

        # Use halfdelay mode (semi-blocking, times out with error if no input)
        self._halfdelay = True

        # Tenths of tenths of seconds to block (1 - 255) in halfdelay mode
        # We set it to 1 which is calculates to 10ms.
        self._halfdelay_tenths = 1

        # Wether the mouse should be used
        self._enable_mouse = 0

        # Mouse interval, how long to wait for detecting clicks
        self._mouse_interval = 200

        # What mouse events to detect
        self._mouse_mask = -1  # All events. curses.ALL_MOUSE_EVENTS wasn't enough

        # Mouse button states. True means pressed.
        self._mouse_btns = {
            1: False,
            2: False,
            3: False,
            4: False,
        }

        # Map curses mouse events to states
        self._mouse_states = {}

    def _setup(self):
        self._mouse_states = {
            curses.BUTTON1_RELEASED:        {"btn": 1, "type": "up"},
            curses.BUTTON2_RELEASED:        {"btn": 2, "type": "up"},
            curses.BUTTON3_RELEASED:        {"btn": 3, "type": "up"},
            curses.BUTTON4_RELEASED:        {"btn": 4, "type": "up"},
            curses.BUTTON1_PRESSED:         {"btn": 1, "type": "down"},
            curses.BUTTON2_PRESSED:         {"btn": 2, "type": "down"},
            curses.BUTTON3_PRESSED:         {"btn": 3, "type": "down"},
            curses.BUTTON4_PRESSED:         {"btn": 4, "type": "down"},
            curses.BUTTON1_CLICKED:         {"btn": 1, "type": "click"},
            curses.BUTTON2_CLICKED:         {"btn": 2, "type": "click"},
            curses.BUTTON3_CLICKED:         {"btn": 3, "type": "click"},
            curses.BUTTON4_CLICKED:         {"btn": 4, "type": "2-click"},
            curses.BUTTON1_DOUBLE_CLICKED:  {"btn": 1, "type": "2-click"},
            curses.BUTTON2_DOUBLE_CLICKED:  {"btn": 2, "type": "2-click"},
            curses.BUTTON3_DOUBLE_CLICKED:  {"btn": 3, "type": "2-click"},
            curses.BUTTON4_DOUBLE_CLICKED:  {"btn": 4, "type": "2-click"},
            curses.BUTTON1_TRIPLE_CLICKED:  {"btn": 1, "type": "3-click"},
            curses.BUTTON2_TRIPLE_CLICKED:  {"btn": 2, "type": "3-click"},
            curses.BUTTON3_TRIPLE_CLICKED:  {"btn": 3, "type": "3-click"},
            curses.BUTTON4_TRIPLE_CLICKED:  {"btn": 4, "type": "3-click"},
        }

    def _start(self):
        """Setup curses for input."""
        global curses
        if not curses:
            import curses
        self._setup()
        if self._halfdelay:
            curses.halfdelay(self._halfdelay_tenths)
        if self._enable_mouse:
            self._use_mouse(1)

        # Let curses try to handle escape sequences for special keys.
        # Its not enough, but it makes it easier to normalize the input.
        self._root.keypad(True)

    def _stop(self):
        pass

    def _use_mouse(self, yes):
        self._enable_mouse = yes
        if self._running:
            if yes:
                curses.mouseinterval(self._mouse_interval)
                curses.mousemask(self._mouse_mask)
            else:
                curses.mousemask(0)

    def _set_root(self, root):
        """Set the curses root window."""
        self._root = root

    def _get_char(self):
        """
        Return input from curses via get_wch or None if no input is available.
        """
        # Fixes resize evens being sometimes reported incorrectly
        curses.doupdate()
        try:
            return self._root.get_wch()
        except KeyboardInterrupt:
            raise
        except:
            return None

    def get_events(self):
        """Get an array of new events."""
        # TODO: Figure out how this should be used
        events = []
        max = 1
        i = 0
        while i < max:
            event = self.get_input()
            if not event:
                break
            events.append(event)
            i += 1

        return events

    def get_input(self):
        """
        Get input and return sanitized InputEvent or None if no input is available.
        """
        # Try to get input from curses
        # We also handle KeyboardInterrupt as a special case for "ctrl+c"
        # NOTE: Detecting KeyboardInterrupt is only reliable when using
        #       halfdelay or blocking mode with curses.
        try:
            # Input is a string or int value if available, otherwise None
            char = self._get_char()
        except KeyboardInterrupt:
            if self._handle_kbd_interrupt:
                # Return a "ctrl+c" event
                event = InputEvent()
                event.set_key("c")
                event.add_modifier(InputEvent.MOD_CTRL)
                return event
            raise

        # Return None if no input is available
        if char is None:
            return None

        # Handle mouse events
        if char == curses.KEY_MOUSE:
            return self._handle_mouse()

        # Handle resize event
        if char == curses.KEY_RESIZE:
            if self._backend:
                self._backend.output.update_size()
            return None

        # Create an empty event
        event = InputEvent()

        # Detect when ALT is pressed to add the alt modifier to the next character
        alt_pressed = 0
        if char == "\x1b":  # ASCII ESC
            # If we get input right after the escape sequence:
            # 1. Set ALT as active
            # 2. Process the new input as the entered character
            # Otherwise we just handle the original char (ASCII ESC '\x1b')
            alt_char = self._get_char()
            if alt_char is not None:
                # ALT is detected
                alt_pressed = 1
                char = alt_char

        # Now handle the normalizing of the actual key
        if type(char) == int:
            # Curses gives special keys as ints
            # We convert the int to a curses keyname. If the keyname is in
            # the key map we use that, otherwise we just use the original value
            keyname = curses.keyname(char).decode(self._encoding)
            key = keyname
            if keyname in curses_key_map:
                key = curses_key_map[keyname]
            event.from_string(key)
        else:
            # When curses gives us a string it's usually printable but we check
            # for some special cases that might be in the key map.
            keyname = curses.keyname(ord(char)).decode(self._encoding)
            # Check if the raw character is in the keymap
            if char in curses_key_map:
                # Convert keymap value
                # Value is formatted as: 'alt+a', 'shift+up', 'escape' etc.
                event.from_string(curses_key_map[char])
            elif len(keyname) == 2 and keyname[0] == "^" and keyname in curses_key_map:
                # Map control keys: "^A", "^Z" etc.
                # We don't process other keynames since they can conflict with printable keys
                event.from_string(curses_key_map[keyname])
            else:
                # When key not found in map set the character directly
                # These are printable if ALT isn't pressed
                event.set_key(char)
                if not alt_pressed:
                    event.set_printable(True)

        # Finally apply the ALT modifier if present
        if alt_pressed:
            event.add_modifier(InputEvent.MOD_ALT)
            # If the key is uppercase we add shift modifier
            if event.key_value.isupper():
                event.set_key(event.key_value.lower())
                event.add_modifier(InputEvent.MOD_SHIFT)

        return event

    def _handle_mouse(self):
        """
        Get and sanitize a mouse event from curses.
        WARNING: This is still very experimental, and somewhat unreliable.
        TODO: Explain the logic with comments
        """
        try:
            devid, x, y, z, bstate = curses.getmouse()
        except:
            return None

        event = InputEvent()
        event.set_pos(x, y)

        state = None
        for key in self._mouse_states:
            if bstate & key:
                state = self._mouse_states[key]

        if state:
            if state["type"] == "up":
                self._mouse_btns[state["btn"]] = False
            elif state["type"] == "down":
                self._mouse_btns[state["btn"]] = True
            if state["btn"] == 4:
                event.set_mouse_event("wheel-up")
            else:
                event.set_mouse_event(state["type"])
                event.set_mouse_button(state["btn"])

        # This happens when dragging mouse or scrolling down
        elif bstate == 134217728:
            if self._mouse_btns[1] or self._mouse_btns[2] or self._mouse_btns[3]:
                # If a mouse button is down it's a drag event
                event.set_mouse_event("drag")
            else:
                event.set_mouse_event("wheel-down")

        return event
