#-*- encoding: utf-8
"""
File object for storing an opened file and editor.
"""

import os
import time

from helpers import *

class File:
    def __init__(self, app = None):
        self.app = app
        self.name = ""
        self.fpath = ""
        self.data = None
        self.read_only = False # Currently unused
        self.last_save = None
        self.opened = time.time()
        self.editor = None
        self.writable = True

    def _path(self):
        """Get the full path of the file."""
        return os.path.join(self.fpath, self.name)

    def path(self):
        """Get the full path of the file."""
        return self._path()

    def parse_path(self, path):
        """Parse a relative path and return full directory and filename as a tuple."""
        if path[:2] == "~" + os.sep:
            p  = os.path.expanduser("~")
            path = os.path.join(p+os.sep, path[2:])
        ab = os.path.abspath(path)
        parts = os.path.split(ab)
        return parts

    def log(self, s, type=None):
        self.app.logger.log(s, type)

    def get_name(self):
        """Get the file name."""
        return self.name

    def get_editor(self):
        """Get the associated editor."""
        return self.editor

    def set_name(self, name):
        """Set the file name."""
        # TODO: sanitize
        self.name = name
        self.update_editor_extension()
        
    def set_path(self, path):
        """Set the file path. Relative paths are sanitized."""
        self.fpath, self.name = self.parse_path(path)
        self.update_editor_extension()

    def set_data(self, data):
        """Set the file data and apply to editor if it exists."""
        self.data = data
        if self.editor:
            self.editor.set_data(data)
                
    def set_editor(self, editor):
        """The editor instance set its file extension."""
        self.editor = editor
        self.update_editor_extension()

    def on_load(self):
        """Does checks after file is loaded."""
        self.writable = os.access(self._path(), os.W_OK)
        if not self.writable:
            self.log("File not writable.")

    def update_editor_extension(self):
        """Set the editor file extension from the current file name."""
        if not self.editor:
            return False
        ext = self.name.split(".")
        if len(ext) > 1:
            self.editor.set_file_extension(ext[-1])

    def save(self):
        """Write the editor data to file."""
        path = self._path()
        data = self.editor.get_data()
        try:
            f = open(self._path(), "w")
            f.write(data)
            f.close()
        except:
            return False
        self.data = data
        self.last_save = time.time()
        return True

    def load(self, read=True):
        """Try to read the actual file and load the data into the editor instance."""
        if not read:
            return True
        path = self._path()
        if not os.path.isfile(path):
            self.log("Given path isn't a file.")
            return False
        data = self._read_text(path)
        if data == False:
            self.log("Normal file read failed.", LOG_WARNING)
            data = self._read_binary(path)
        if data == False:
            self.log("Fallback file read failed.", LOG_WARNING)
            return False
        self.data = data
        self.editor.set_data(data)
        self.on_load()
        return True

    def _read_text(self, file):
        # Read text file
        try:
            f = open(self._path())
            data = f.read()
            f.close()
            return data
        except:
            return False

    def _read_binary(self, file):
        # Read binary file and try to autodetect encoding
        try:
            f = open(self._path(), "rb")
            data = f.read()
            f.close()
            import chardet
            detection = chardet.detect(data)
            charenc = detection['encoding']
            if charenc == None:
                self.log("Failed to detect file encoding.", LOG_WARNING)
                return False
            self.log("Trying to decode with encoding '" + charenc + "'", LOG_INFO)
            return data.decode(charenc)
        except Exception as inst:
            self.log(type(inst))    # the exception instance
            self.log(inst.args)     # arguments stored in .args
            self.log(inst)          # __str__ allows args to be printed directly,
        return False

    def reload(self):
        """Reload file data."""
        return self.load()

    def is_changed(self):
        """Check if the editor data is different from the file."""
        return self.editor.get_data() != self.data

    def is_writable(self):
        """Check if the file is writable."""
        return self.writable
        