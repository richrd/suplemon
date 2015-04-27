#-*- encoding: utf-8
"""
File object for storing an opened file and editor.
"""

import os
import time

class File:
    def __init__(self, app = None):
        self.app = app
        self.name = ""
        self.fpath = ""
        self.data = None
        self.read_only = False
        self.last_save = None
        self.opened = time.time()
        self.editor = None

    def _path(self):
        """Get the full path of the file."""
        return os.path.join(self.fpath, self.name)

    def path(self):
        """Get the full path of the file."""
        return self._path()

    def parse_path(self, path):
        """Parse a relative path and return full directory and filename as a tuple."""
        if path[:2] == "~"+os.sep:
            p  = os.path.expanduser("~")
            path = os.path.join(p+os.sep, path[2:])
        ab = os.path.abspath(path)
        parts = os.path.split(ab)
        return parts

    def log(self, s):
        self.app.logger.log(s)
            
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

    def update_editor_extension(self):
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
        try:
            f = open(self._path())
            data = f.read()
            f.close()
        except Exception as inst:
            self.log(type(inst))    # the exception instance
            self.log(inst.args)     # arguments stored in .args
            self.log(inst)          # __str__ allows args to be printed directly,
            return False
        self.data = data
        self.editor.set_data(data)
        return True

    def reload(self):
        """Reload file data."""
        return self.load()
        
    def is_changed(self):
        """Check if the editor data is different from the file."""
        return self.editor.get_data() != self.data
