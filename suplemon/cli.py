#!/usr/bin/env python3
# -*- encoding: utf-8
"""
Start a Suplemon instance in the current window
"""

import argparse

from .main import App, __version__


def main():
    """Handle CLI invocation"""
    # Parse our CLI arguments
    parser = argparse.ArgumentParser(description="Console text editor with multi cursor support")
    parser.add_argument("filenames", metavar="filename", type=str, nargs="*", help="Files to load into Suplemon")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--config", type=str, help="Configuration file path.")
    parser.add_argument("--debug", help="Enable logging of debug messages to console.", action="store_true")
    args = parser.parse_args()
    filenames = args.filenames
    config_file = args.config
    debug = args.debug

    # Generate and start our application
    app = App(filenames=filenames, config_file=config_file, debug=debug)
    if app.init():
        app.run()
    else:
        app.logger.error("FATAL: App failed to initialize.")
        app.handle_logs()


if __name__ == "__main__":
    main()
