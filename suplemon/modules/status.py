# -*- encoding: utf-8

from suplemon.suplemon_module import Module
from suplemon.statusbar import StatusComponent
import curses


class AppStatusComponent(StatusComponent):
    """ Return current app status message (no truncate) """
    def __init__(self, app):
        self.app = app
        StatusComponent.__init__(self, "n/a", 2)

    def compute(self):
        # TODO: this could have some style based
        #       on warn level from self.app applied
        text = self.app.get_status()
        if text != self._text:
            self.text = text
        return self._serial


class AppIndicatorDocumentLines(StatusComponent):
    """ Return amount of lines in buffer """
    def __init__(self, app):
        self.app = app
        StatusComponent.__init__(self, "0")
        self._lines = 0

    def compute(self):
        lines = len(self.app.get_editor().lines)
        if self._lines != lines:
            self._lines = lines
            self.text = str(lines)
        return self._serial


class AppIndicatorDocumentPosition(StatusComponent):
    """ Return $current_line/$amount_of_lines """
    def __init__(self, app):
        self.app = app
        StatusComponent.__init__(self, "0/0")
        self._lines = 0
        self._pos = 0

    def compute(self):
        editor = self.app.get_editor()
        lines = len(editor.lines)
        pos = editor.get_cursor()[1] + 1
        if self._lines != lines or self._pos != pos:
            self._lines = lines
            self._pos = pos
            self.text = "{}/{}".format(pos, lines)
        return self._serial


class AppIndicatorDocumentPosition2(StatusComponent):
    """ Return @$current_col,$current_line/$amount_of_lines """
    def __init__(self, app):
        self.app = app
        StatusComponent.__init__(self, "@0,0/0", curses.A_DIM)
        self._state = (0, 0, 0)

    def compute(self):
        editor = self.app.get_editor()
        _cursor = editor.get_cursor()
        # x, y, y-len
        state = (_cursor[0] + 1, _cursor[1] + 1, len(editor.lines))
        if self._state != state:
            self._state = state
            self.text = "@{},{}/{}".format(*state)
        return self._serial


class AppIndicatorCursors(StatusComponent):
    """ Return amount of cursors """
    def __init__(self, app):
        self.app = app
        StatusComponent.__init__(self, "n/a")
        self._cursors = None

    def compute(self):
        cursors = len(self.app.get_editor().cursors)
        if cursors != self._cursors:
            self._cursors = cursors
            self.text = str(cursors)
        return self._serial


class AppIndicatorPosition(StatusComponent):
    """ Return @$current_col,$current_line """
    def __init__(self, app):
        self.app = app
        StatusComponent.__init__(self, "n/a")
        self._posY = None
        self._posX = None
        self.style = curses.A_DIM

    def compute(self):
        position = self.app.get_editor().get_cursor()
        posY = position[1]
        posX = position[0]
        if posY != self._posY or posX != self._posX:
            self._posY = posY
            self._posX = posX
            self.text = "@{},{}".format(posY + 1, posX + 1)
        return self._serial


class _AppIndicatorPositionSingle(StatusComponent):
    """ Internal helper """
    def __init__(self, app, index):
        self.app = app
        StatusComponent.__init__(self, "n/a")
        self._pos = None
        self._index = index

    def compute(self):
        position = self.app.get_editor().get_cursor()
        pos = position[self._index]
        if pos != self._pos:
            self._pos = pos
            self.text = str(pos + 1)
        return self._serial


class AppIndicatorPositionY(_AppIndicatorPositionSingle):
    """ Return $current_line """
    def __init__(self, app):
        _AppIndicatorPositionSingle.__init__(self, app, 1)


class AppIndicatorPositionX(_AppIndicatorPositionSingle):
    """ Return $current_col """
    def __init__(self, app):
        _AppIndicatorPositionSingle.__init__(self, app, 0)


class EditorLogo(StatusComponent):
    """ Return Editor logo """
    def __init__(self, app):
        # TODO: check for config: use_unicode_symbols
        StatusComponent.__init__(self, "n/a")
        self.app = app

    def compute(self):
        # TODO: check for config: use_unicode_symbols
        logo = self.app.config["modules"][__name__]["logo_char"]
        if self._text != logo:
            self.text = logo
        return self._serial


class EditorName(StatusComponent):
    """ Return Editor name """
    def __init__(self, app):
        StatusComponent.__init__(self, "Suplemon Editor")


class EditorVersion(StatusComponent):
    """ Return Editor version """
    def __init__(self, app):
        version = app.version
        StatusComponent.__init__(self, "v{}".format(version))


class AppStatus(Module):
    """Show app status"""
    def get_components(self):
        return [
            ("app_status", AppStatusComponent),
            ("cursor_count", AppIndicatorCursors),
            ("cursor_position", AppIndicatorPosition),
            ("cursor_posY", AppIndicatorPositionY),
            ("cursor_posX", AppIndicatorPositionX),
            ("document_lines", AppIndicatorDocumentLines),
            ("document_position", AppIndicatorDocumentPosition2),
            ("editor_logo", EditorLogo),
            ("editor_name", EditorName),
            ("editor_version", EditorVersion)
        ]

    def get_default_config(self):
        return {
            "logo_char": "\u2688",      # not so fancy lemon
            # "logo_char": "\U0001f34b" # fancy lemon
        }


module = {
    "class": AppStatus,
    "name": "status"
}
