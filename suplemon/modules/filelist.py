# -*- encoding: utf-8

from suplemon.suplemon_module import Module
from suplemon.statusbar import StatusComponent, StatusComponentGenerator


class FileListGenerator(StatusComponentGenerator):
    def __init__(self, app):
        StatusComponentGenerator.__init__(self)
        self.app = app
        self._state = (None, None, None)
        self._components = list()

    def compute(self):
        f = self.app.get_file()
        state = (id(f), f.is_writable(), f.is_changed())
        if self._state != state:
            self._state = state
            # TODO: This does not regenerate on config changes
            self._components = list(self._generate())
            self._serial += 1
        return self._serial

    def get_components(self):
        return self._components

    def _generate(self):
        """
            Generate (maybe rotated) file list components beginning at current file.
            Current file has a priority of 2 and thus is unlikely to truncate.
            All other files have a priority of 0 and are thus below the default of 1
            and will be truncated if the space gets low.
        """

        use_unicode = self.app.config["app"]["use_unicode_symbols"]
        show_modified = self.app.config["display"]["show_file_modified_indicator"]

        config = self.app.config["modules"][__name__]
        no_write_symbol = config["no_write"][use_unicode]
        is_changed_symbol = config["is_changed"][use_unicode]
        rotate = config["rotate"]
        wrap_active = config["wrap_active"]
        wrap_active_align = config["wrap_active_align"]
        limit = config["limit"]
        style_other = self.app.ui.colors.get("filelist_other")
        style_active = self.app.ui.colors.get("filelist_active")

        files = self.app.get_files()
        curr_file_index = self.app.current_file_index()
        curr_file = files[curr_file_index]
        filecount = len(files)
        if 0 < limit < filecount:
            files = [
                files[curr_file_index - 1],
                files[curr_file_index],
                files[(curr_file_index + 1) % filecount]
            ]
        elif rotate:
            # TODO: allow rotate if hitting limit as well?
            files = files[curr_file_index:] + files[:curr_file_index]

        for f in files:
            name = f.name
            if not f.is_writable():
                name = no_write_symbol + name
            elif show_modified and f.is_changed():
                name += is_changed_symbol
            if f == curr_file:
                if wrap_active:
                    name = "[%s]" % name
                yield StatusComponent(name, style_active, 2)
            else:
                if wrap_active and wrap_active_align:
                    name = " %s " % name
                yield StatusComponent(name, style_other, 0)

        if 0 < limit < filecount:
            yield StatusComponent("(%i more)" % (filecount - limit), style_other)

class FileList(Module):
    """Show open tabs/files"""
    def get_components(self):
        return [
            ("filelist", FileListGenerator)
        ]

    def get_default_config(self):
        return {
            "rotate": False,
            "wrap_active": True,
            "wrap_active_align": False,
            "no_write": ["!", "\u2715"],
            "is_changed": ["*", "\u2732"],
            "limit": 0
        }


module = {
    "class": FileList,
    "name": "filelist"
}
