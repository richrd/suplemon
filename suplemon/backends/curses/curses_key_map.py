# -*- encoding: utf-8
"""
This file maps ugly curses keycodes to human readable versions.
"""

key_map = {
    # Single keys
    "KEY_F(1)": "f1",
    "KEY_F(2)": "f2",
    "KEY_F(3)": "f3",
    "KEY_F(4)": "f4",
    "KEY_F(5)": "f5",
    "KEY_F(6)": "f6",
    "KEY_F(7)": "f7",
    "KEY_F(8)": "f8",
    "KEY_F(9)": "f9",
    "KEY_F(10)": "f10",
    "KEY_F(11)": "f11",
    "KEY_F(12)": "f12",

    "KEY_UP": "up",
    "KEY_DOWN": "down",
    "KEY_LEFT": "left",
    "KEY_RIGHT": "right",

    "KEY_ENTER": "shift+enter",
    "\n": "enter",
    "^J": "enter",

    "KEY_BACKSPACE": "backspace",
    "^?": "backspace",

    "KEY_DC": "delete",
    "KEY_HOME": "home",
    "KEY_END": "end",
    "KEY_PPAGE": "pageup",
    "KEY_NPAGE": "pagedown",

    "KEY_IC": "insert",
    "\t": "tab",
    "^I": "tab",
    "^[": "escape",
    "\x1b": "escape",

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
    "^Z": "ctrl+z",  # Conflicts with suspend

    "kLFT5": "ctrl+left",
    "kRIT5": "ctrl+right",
    "kUP5": "ctrl+up",
    "kDN5": "ctrl+down",

    "kIC5": "ctrl+insert",
    "kDC5": "ctrl+delete",
    "kHOM5": "ctrl+home",
    "kEND5": "ctrl+end",

    "kNXT5": "ctrl+pagedown",
    "kPRV5": "ctrl+pageup",

    "O5P": "ctrl+f1",
    "O5Q": "ctrl+f2",
    "O5R": "ctrl+f3",
    "O5S": "ctrl+f4",

    "KEY_F(29)": "ctrl+f5",
    "KEY_F(30)": "ctrl+f6",
    "KEY_F(31)": "ctrl+f7",
    "KEY_F(32)": "ctrl+f8",
    "KEY_F(33)": "ctrl+f9",
    "KEY_F(34)": "ctrl+f10",
    "KEY_F(35)": "ctrl+f11",
    "KEY_F(36)": "ctrl+f12",

    # Alt
    "kUP3": "alt+up",
    "kDN3": "alt+down",
    "kLFT3": "alt+left",
    "kRIT3": "alt+right",

    "kIC3": "alt+insert",
    "kDC3": "alt+delete",
    "kHOM3": "alt+home",
    "kEND3": "alt+end",

    "kPRV3": "alt+pageup",
    "kNXT3": "alt+pagedown",

    "KEY_F(53)": "alt+f5",
    "KEY_F(54)": "alt+f6",
    "KEY_F(55)": "alt+f7",
    "KEY_F(56)": "alt+f8",
    "KEY_F(57)": "alt+f9",
    "KEY_F(58)": "alt+f10",
    "KEY_F(59)": "alt+f11",
    "KEY_F(60)": "alt+f12",

    # Shift
    "KEY_SLEFT": "shift+left",
    "KEY_SRIGHT": "shift+right",
    "KEY_SR": "shift+up",
    "KEY_SF": "shift+down",

    "KEY_BTAB": "shift+tab",

    "KEY_SDC": "shift+delete",
    "KEY_SHOME": "shift+home",
    "KEY_SEND": "shift+end",

    "O2P": "shift+f1",
    "O2Q": "shift+f2",
    "O2R": "shift+f3",
    "O2S": "shift+f4",

    "KEY_F(17)": "shift+f5",
    "KEY_F(18)": "shift+f6",
    "KEY_F(19)": "shift+f7",
    "KEY_F(20)": "shift+f8",
    "KEY_F(21)": "shift+f9",
    "KEY_F(22)": "shift+f10",
    "KEY_F(23)": "shift+f11",
    "KEY_F(24)": "shift+f12",


    # Alt Gr
    "O1P": "altgr+f1",
    "O1Q": "altgr+f2",
    "O1R": "altgr+f3",
    "O1S": "altgr+f4",


    # Shift + Alt
    "kUP4": "shift+alt+up",
    "kDN4": "shift+alt+down",
    "kLFT4": "shift+alt+left",
    "kRIT4": "shift+alt+right",

    "kIC4": "shift+alt+inset",
    "kDC4": "shift+alt+delete",
    "kHOM4": "shift+alt+home",
    "kEND4": "shift+alt+end",


    # Control + Shift
    "kUP6": "ctrl+shift+up",
    "kDN6": "ctrl+shift+down",
    "kLFT6": "ctrl+shift+left",
    "kRIT6": "ctrl+shift+right",

    "kDC6": "ctrl+shift+delete",
    "kHOM6": "ctrl+shift+home",
    "kEND6": "ctrl+shift+end",

    "KEY_F(41)": "ctrl+shift+f5",
    "KEY_F(42)": "ctrl+shift+f6",
    "KEY_F(43)": "ctrl+shift+f7",
    "KEY_F(44)": "ctrl+shift+f8",
    "KEY_F(45)": "ctrl+shift+f9",
    "KEY_F(46)": "ctrl+shift+f10",
    "KEY_F(47)": "ctrl+shift+f11",
    "KEY_F(48)": "ctrl+shift+f12",

    # Control + Alt
    "kUP7": "ctrl+alt+up",
    "kDN7": "ctrl+alt+down",
    "kLFT7": "ctrl+alt+left",
    "kRIT7": "ctrl+alt+right",

    "kPRV7": "ctrl+alt+pageup",
    "kNXT7": "ctrl+alt+pagedown",

    "kIC7": "ctrl+alt+insert",
    "kDC7": "ctrl+alt+delete",
    "kHOM7": "ctrl+alt+home",
    "kEND7": "ctrl+alt+end",

    # Special events
    "KEY_RESIZE": "resize",
}
