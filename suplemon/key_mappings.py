# -*- encoding: utf-8
"""
This file maps ugly curses keycodes to human readable versions.
"""

import curses


key_map = {
    # Single keys
    # F1
    curses.KEY_F1: "f1",    # 265
    curses.KEY_F2: "f2",    # 266
    curses.KEY_F3: "f3",    # 267
    curses.KEY_F4: "f4",    # 268
    curses.KEY_F5: "f5",    # 269
    curses.KEY_F6: "f6",    # 270
    curses.KEY_F7: "f7",    # 271
    curses.KEY_F8: "f8",    # 272
    curses.KEY_F9: "f9",    # 273
    curses.KEY_F10: "f10",  # 274
    curses.KEY_F11: "f11",  # 275
    curses.KEY_F12: "f12",  # 276

    curses.KEY_UP: "up",
    curses.KEY_DOWN: "down",
    curses.KEY_LEFT: "left",
    curses.KEY_RIGHT: "right",
    curses.KEY_ENTER: "enter",
    "\n": "enter",
    "^J": "enter",
    curses.KEY_BACKSPACE: "backspace",
    "^?": "backspace",
    curses.KEY_DC: "delete",
    curses.KEY_HOME: "home",
    curses.KEY_END: "end",
    curses.KEY_PPAGE: "pageup",
    curses.KEY_NPAGE: "pagedown",
    331: "insert",
    "\t": "tab",
    "^I": "tab",
    "^[": "escape",

    # Control
    "^A": "ctrl+a",
    "^B": "ctrl+b",
    "^C": "ctrl+c",
    "^D": "ctrl+d",
    "^E": "ctrl+e",
    "^F": "ctrl+f",
    "^G": "ctrl+g",
    "^H": "ctrl+h",
    # "^I": "ctrl+i",  # Conflicts with 'tab'
    # "^J": "ctrl+j",  # Conflicts with 'enter'
    "^K": "ctrl+k",
    "^L": "ctrl+l",
    # "^M": "ctrl+m",  # Conflicts with 'enter'
    "^N": "ctrl+n",
    "^O": "ctrl+o",
    "^P": "ctrl+p",
    "^Q": "ctrl+q",
    "^R": "ctrl+r",
    "^S": "ctrl+s",
    "^T": "ctrl+t",
    "^U": "ctrl+u",
    "^V": "ctrl+v",
    "^W": "ctrl+w",
    "^X": "ctrl+x",
    "^Y": "ctrl+y",
    # "^Z": "ctrl+z",  # Conflicts with suspend

    544: "ctrl+left",
    559: "ctrl+right",
    565: "ctrl+up",
    524: "ctrl+down",
    "kLFT5": "ctrl+left",
    "kRIT5": "ctrl+right",
    "kUP5": "ctrl+up",
    "kDN5": "ctrl+down",
    554: "ctrl+pageup",
    549: "ctrl+pagedown",
    "kNXT5": "ctrl+pageup",
    "kPRV5": "ctrl+pagedown",

    # Alt
    563: "alt+up",
    522: "alt+down",
    542: "alt+left",
    557: "alt+right",
    "kUP3": "alt+up",
    "kDN3": "alt+down",
    "kLFT3": "alt+left",
    "kRIT3": "alt+right",
    552: "alt+pageup",
    547: "alt+pagedown",
    "kPRV3": "alt+pageup",
    "kNXT3": "alt+pagedown",

    # Shift
    353: "shift+tab",
}
