#!/usr/bin/env python3
# -*- encoding: utf-8
"""
Start a Suplemon instance in the current window
"""

import sys

try:
    import argparse
except:
    # Python < 2.7
    argparse = False

from main import App, __version__


def main():
    """Handle CLI invocation"""
    # Parse our CLI arguments
    if argparse:
        parser = argparse.ArgumentParser(description="Console text editor with multi cursor support")
        parser.add_argument("filenames", metavar="filename", type=str, nargs="*", help="Files to load into Suplemon")
        parser.add_argument("--version", action="version", version=__version__)
        args = parser.parse_args()
        filenames = args.filenames
    else:
        # Python < 2.7 fallback
        filenames = sys.argv[1:]

    # Generate and start our application
    app = App(filenames=filenames)
    app.init()

    # Output log info
    if app.config["app"]["debug"]:
        app.logger_handler.output()

if __name__ == "__main__":
    main()
