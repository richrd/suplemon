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
    args = parser.parse_args()
    filenames = args.filenames
    config_file = args.config

    # Generate and start our application
    app = App(filenames=filenames, config_file=config_file)
    if app.init():
        app.run()
    else:
        app.logger.debug("app.init() returned False, not proceeding to run.")


if __name__ == "__main__":
    main()
