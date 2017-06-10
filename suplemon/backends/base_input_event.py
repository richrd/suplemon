

class InputEvent(object):
    """An input event that represents a keyboard or mouse interaction."""
    # These events are created by normalizing input from different libraries like curses.

    # Modifiers in same order as used when concatenating key to string
    MOD_CTRL = "ctrl"
    MOD_SHIFT = "shift"
    MOD_ALT = "alt"

    def __init__(self):
        self._dev_id = None
        self._x = None
        self._y = None
        self._mouse_type = None
        self._mouse_btn = None

        self.is_keyboard = False
        self.is_mouse = False
        self.is_resize = False
        self.is_printable = False

        self.key_value = ""
        self.key_string = None  # e.g. "a", "A", "ctrl+a" etc. Same as sublime-text bindings.
        self.modifiers = []

    def __str__(self):
        if self.is_keyboard:
            return "KEY[{} / {}, printable: {}]".format(self.to_string(), self.key_value, str(self.is_printable))
        return "MOUSE[{},{}] {} {}".format(self._x, self._y, self._mouse_type, self._mouse_btn)

    def __repr__(self):
        return str(self)

    #
    # Mouse Events
    #

    def set_pos(self, x, y):
        """Set mouse x,y position."""
        self._x = x
        self._y = y

    def get_pos(self):
        """Get mouse x,y position."""
        return self._x, self._y

    def set_mouse_event(self, event_type):
        self._mouse_type = event_type

    def set_mouse_button(self, btn):
        """Set the mouse button integer id."""
        self._mouse_btn = btn

    #
    # Keyboard Events
    #

    @property
    def key(self):
        return self.to_string()

    def set_key(self, val):
        """Set the key value for the input event."""
        self.is_keyboard = True
        self.key_value = val

    def set_printable(self, printable):
        """Set wether the input event is printable, as in a char that can be shown properly on a line."""
        self.is_keyboard = True
        self.is_printable = printable

    def get_modifiers(self):
        """Get list of keyboard modifiers."""
        return self.modifiers

    def add_modifier(self, mod):
        """Add a keyboard modifier to the event."""
        if mod not in self.modifiers:
            self.modifiers.append(mod)
            return True
        return False

    def remove_modifier(self, mod):
        """Remove a keyboard modifier from the event."""
        if mod in self.modifiers:
            self.modifiers.remove(mod)
            return True
        return False

    #
    # Parse and encode sublime-text style key binding strings
    #

    def from_string(self, s):
        """Construct the event by parsing a sublime-text style string."""
        self.is_keyboard = True
        parts = s.split("+")
        if len(parts) == 1:
            self.key_value = parts[0]
            return
        self.key_value = parts.pop()
        self.modifiers = [mod.lower() for mod in parts]

    def to_string(self):
        """Return string version of event in sublime-text config format."""
        key_str = self.key_value
        # The following order must be preserved
        if InputEvent.MOD_ALT in self.modifiers:
            key_str = "alt+" + key_str
        if InputEvent.MOD_SHIFT in self.modifiers:
            key_str = "shift+" + key_str
        if InputEvent.MOD_CTRL in self.modifiers:
            key_str = "ctrl+" + key_str
        return key_str
