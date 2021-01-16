# -*- encoding: utf-8

import time

from suplemon.suplemon_module import Module


class Date(Module):
    """Shows the current date without year in the top status bar."""

    def get_status(self):
        s = time.strftime("%Y-%m-%d")
        if self.app.config["app"]["use_unicode_symbols"]:
            return "" + s
        return s


module = {
    "class": Date,
    "name": "date",
    "status": "top",
}
