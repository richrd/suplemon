# -*- encoding: utf-8

import socket

from suplemon.suplemon_module import Module


class Hostname(Module):
    """Shows the machine hostname in the bottom status bar."""

    def init(self):
        self.hostname = ""
        hostinfo = None
        try:
            hostinfo = socket.gethostbyaddr(socket.gethostname())
        except:
            self.logger.debug("Failed to get hostname.")
        if hostinfo:
            self.hostname = hostinfo[0]
            # Use shorter hostname if available
            if hostinfo[1]:
                self.hostname = hostinfo[1][0]

    def get_status(self):
        if self.hostname:
            return "host:{0}".format(self.hostname)
        return ""


module = {
    "class": Hostname,
    "name": "hostname",
    "status": "bottom",
}
