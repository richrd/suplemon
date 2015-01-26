"""
File object for storing an opened file and editor.
"""

import os
import time

class File:
    def __init__(self, parent = None):
        self.parent = parent
        self.name = ""
        self.fpath = ""
        self.data = None
        self.read_only = False
        self.last_save = None
        self.opened = time.time()
        self.editor = None

    def _path(self):
        return os.path.join(self.fpath, self.name)

    def path(self):
        return self._path()

    def parse_path(self, path):
        if path[:2] == "~"+os.sep:
            p  = os.path.expanduser("~")
            path = os.path.join(p+os.sep, path[2:])
        ab = os.path.abspath(path)
        parts = os.path.split(ab)
        return parts

    def log(self, s):
        self.parent.logger.log(s)
            
    def set_name(self, name):
        # TODO: sanitize
        self.name = name
        
    def set_path(self, path):
        self.fpath, self.name = self.parse_path(path)

    def set_data(self, data):
        self.data = data
        if self.editor:
            self.editor.set_data(data)
                
    def set_editor(self, editor):
        self.editor = editor
        ext = self.name.split(".")
        if len(ext) > 1:
            editor.set_file_extension(ext[-1])

    def set_saved(self, m):
         self.last_save = time.time()

    def save(self):
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
        return self.load()
        
    def is_changed(self):
        return self.editor.get_data() != self.data
