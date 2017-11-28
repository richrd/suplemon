# -*- encoding: utf-8

from suplemon.suplemon_module import Module


class BulkDelete(Module):
    """
    Bulk delete lines and characters.
    Asks what direction to delete in by default.

    Add 'up' to delete lines above highest cursor.
    Add 'down' to delete lines below lowest cursor.
    Add 'left' to delete characters to the left of all cursors.
    Add 'right' to delete characters to the right of all cursors.
    """

    def init(self):
        self.directions = ["up", "down", "left", "right"]

    def handler(self, prompt, event):
        # Get arrow keys from prompt
        if event.key_name in self.directions:
            prompt.set_data(event.key_name)
            prompt.on_ready()
        return True  # Disable normal key handling

    def run(self, app, editor, args):
        direction = args.lower()
        if not direction:
            direction = app.ui.query_filtered("Press arrow key in direction to delete:", handler=self.handler)

        if direction not in self.directions:
            app.set_status("Invalid direction.")
            return False

        # Delete entire lines
        if direction == "up":
            pos = editor.get_first_cursor()
            length = len(editor.lines)
            editor.lines = editor.lines[pos.y:]
            delta = length - len(editor.lines)
            # If lines were removed, move the cursors up the same amount
            if delta:
                editor.move_cursors((0, -delta))

        elif direction == "down":
            pos = editor.get_last_cursor()
            editor.lines = editor.lines[:pos.y+1]

        # Delete from start or end of lines
        else:
            # Select min/max function based on direction
            func = min if direction == "left" else max
            # Get all lines with cursors
            line_indices = editor.get_lines_with_cursors()
            for line_no in line_indices:
                # Get all cursors for the line
                line_cursors = editor.get_cursors_on_line(line_no)
                # Get the leftmost of rightmost x coordinate
                x = func(line_cursors, key=lambda c: c.x).x

                # Delete correct part of the line
                line = editor.lines[line_no]
                if direction == "left":
                    line.data = line.data[x:]
                    # Also move cursors appropriately when deleting left side
                    [c.move_left(x) for c in line_cursors]
                else:
                    line.data = line.data[:x]


module = {
    "class": BulkDelete,
    "name": "bulk_delete",
}
