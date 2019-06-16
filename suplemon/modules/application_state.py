# -*- encoding: utf-8


import hashlib

from suplemon.suplemon_module import Module


class ApplicationState(Module):
    """
    Stores the state of open files when exiting the editor and restores when files are reopened.

    Cursor positions and scroll position are stored and restored.
    """

    def init(self):
        self.init_logging(__name__)
        self.bind_event_after("app_loaded", self.on_load)
        self.bind_event_before("app_exit", self.on_exit)

    def on_load(self, event):
        """Runs when suplemon is fully loaded."""
        self.restore_states()

    def on_exit(self, event):
        """Runs before suplemon is exits."""
        self.store_states()

    def get_file_states(self):
        """Get the state of currently opened files. Returns a dict with the file path as key and file state as value."""
        states = {}
        for file in self.app.get_files():
            states[file.get_path()] = self.get_file_state(file)
        return states

    def get_file_state(self, file):
        """Get the state of a single file."""
        editor = file.get_editor()
        state = {
            "cursors": [cursor.tuple() for cursor in editor.cursors],
            "scroll_pos": editor.scroll_pos,
            "hash": self.get_hash(editor),
        }
        return state

    def get_hash(self, editor):
        # We don't need cryptographic security so we just use md5
        h = hashlib.md5()
        for line in editor.lines:
            h.update(line.get_data().encode("utf-8"))
        return h.hexdigest()

    def set_file_state(self, file, state):
        """Set the state of a file."""
        cursor = file.editor.get_cursor()
        # Don't set the cursor pos if it's not the default 0,0
        if cursor.x or cursor.y:
            return
        file.editor.set_cursors(state["cursors"])
        file.editor.scroll_pos = state["scroll_pos"]

    def store_states(self):
        """Store the states of opened files."""
        states = self.get_file_states()
        for path in states.keys():
            self.storage[path] = states[path]
        self.storage.store()

    def restore_states(self):
        """Restore the states of files that are currently open."""
        for file in self.app.get_files():
            path = file.get_path()
            if path in self.storage.get_data().keys():
                state = self.storage[path]
                if "hash" not in state:
                    self.set_file_state(file, state)
                elif state["hash"] == self.get_hash(file.get_editor()):
                    self.set_file_state(file, state)


module = {
    "class": ApplicationState,
    "name": "application_state",
}
