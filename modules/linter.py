# -*- encoding:utf-8

import subprocess
from mod_base import *


class Linter(Command):
    def init(self):
        self.bind_event("app_loaded", self.lint_files)
        self.bind_event("mainloop", self.mainloop)
        self.bind_event("after:save_file", self.lint_files)
        self.bind_event("after:save_file_as", self.lint_files)

    def lint_files(self, event):
        self.log("LINTER EVENT " + str(event))
        """Do linting check for all open files and store results."""
        for file in self.app.files:
            self.lint_file(file)
        return False

    def lint_file(self, file):
        path = file.get_path()
        if not path: # Unsaved file
            return False
        linting = self.get_file_linting(path)
        editor = file.get_editor()
        #for line_no in linting.keys():
        line_no = 0
        while line_no < len(editor.lines):
            line = editor.lines[line_no]
            if line_no+1 in linting.keys():
                line.linting = linting[line_no+1]
                line.set_number_color(1)
            else:
                line.linting = False
                line.reset_number_color()
            line_no += 1

    def get_msgs_on_line(self, editor, line_no):
        line = editor.lines[line_no]
        if not hasattr(line, "linting") or not line.linting:
            return False
        return line.linting[0][1]

    def run(self, app, editor):
        """Run the linting command."""
        pass

    def mainloop(self, event):
        """Run the linting command."""
        file = self.app.get_file()
        editor = file.get_editor()
        cursor = editor.get_cursor()
        if len(editor.cursors) > 1:
            return False
        line_no = cursor.y + 1
        msg = self.get_msgs_on_line(editor, cursor.y)
        if msg:
            self.app.set_status("Line " + str(line_no) + ": " + msg)

    def get_output(self, cmd):
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        out, err = process.communicate()
        return out

    def get_file_linting(self, path):
        """Do linting check for given file path."""
        output = self.get_output(["flake8", path]).decode("utf-8")
        # Remove file paths from output
        output = output.replace(path+":", "")
        lines = output.split("\n")
        linting = {}
        for line in lines:
            if not line:
                continue
            parts = line.split(":")
            line_no = int(parts[0])
            char_no = int(parts[1])
            message = ":".join(parts[2:]).strip()
            if not line_no in linting.keys():
                linting[line_no] = []
            linting[line_no].append((char_no, message))
        return linting

module = {
    "class": Linter,
    "name": "linter",
}
