# -*- encoding:utf-8
import subprocess

from suplemon_module import Module


class Linter(Module):
    def init(self):
        self.init_logging(__name__)
        if not self.has_flake8_support():
            self.logger.warning("Flake8 not available. Can't show linting.")
            return False

        # Lint all files after app is loaded
        self.bind_event_after("app_loaded", self.lint_all_files)
        # Show linting messages in status bar
        self.bind_event_after("mainloop", self.mainloop)
        # Re-lint current file when appropriate
        self.bind_event_after("save_file", self.lint_current_file)
        self.bind_event_after("save_file_as", self.lint_current_file)
        self.bind_event_after("reload_file", self.lint_current_file)
        self.bind_event_after("open_file", self.lint_current_file)

    def has_flake8_support(self):
        return self.get_output(["flake8"])

    def lint_current_file(self, event):
        self.lint_file(self.app.get_file())

    def lint_all_files(self, event):
        """Do linting check for all open files and store results."""
        for file in self.app.files:
            self.lint_file(file)
        return False

    def lint_file(self, file):
        path = file.get_path()
        if not path:  # Unsaved file
            return False
        if file.get_extension().lower() != "py":  # Only lint Python files
            return False
        linting = self.get_file_linting(path)
        if not linting:  # Linting failed
            return False
        editor = file.get_editor()
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

    def get_msg_count(self, editor):
        count = 0
        for line in editor.lines:
            if hasattr(line, "linting"):
                if line.linting:
                    count += 1
        return count

    def run(self, app, editor):
        """Run the linting command."""
        editor = self.app.get_file().get_editor()
        count = self.get_msg_count(editor)
        status = str(count) + " lines with linting errors in this file."
        self.app.set_status(status)

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
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        except EnvironmentError:
            # cant use FileNotFoundError in Python 2
            return False
        out, err = process.communicate()
        return out

    def get_file_linting(self, path):
        """Do linting check for given file path."""
        output = self.get_output(["flake8", path])
        if not output:
            return False
        output = output.decode("utf-8")
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
            if line_no not in linting.keys():
                linting[line_no] = []
            linting[line_no].append((char_no, message))
        return linting

module = {
    "class": Linter,
    "name": "linter",
}
