#!/usr/bin/python3
#-*- encoding: utf-8
"""
Start a Suplemon instance in the current window
"""

import argparse

from main import App, __version__


def main():
    """Handle CLI invocation"""
    # Parse our CLI arguments
    parser = argparse.ArgumentParser(description="Console text editor with multi cursor support")
    parser.add_argument("filenames", metavar="filename", type=str, nargs="*", help="Files to load into Suplemon")
    parser.add_argument("--version", action="version", version=__version__)
    args = parser.parse_args()

    # Generate and start our application
    app = App(filenames=args.filenames)
    app.init()

    # Output log info
    if app.config["app"]["debug"]:
        app.logger.output()


if __name__ == "__main__":
    main()
