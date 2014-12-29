import os
import time

class File:
    def __init__(self):
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

    def log(self, s):
        try:
            app.logger.log(s)
        except:
            print s

    def set_data(self, data):
        self.data = data
        if self.editor:
            self.editor.set_data(data)
        
    def set_path(self, path):
        ab = os.path.abspath(path)
        self.fpath, self.name = os.path.split(ab)
        
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

    def load(self):
        path = self._path()
        try:
            f = open(self._path())
            data = f.read()
            f.close()
        except:
            return False
        self.data = data
        self.editor.set_data(data)
        return True

    def reload(self):
        return self.load()
        
    def is_changed(self):
        return self.editor.get_data() != self.data
