# -*- encoding: utf-8
"""
Addon module loader.
"""
import os
import imp
import logging


class ModuleLoader:
    def __init__(self, app=None):
        self.app = app
        self.logger = logging.getLogger(__name__)
        # The app root directory
        self.curr_path = os.path.dirname(os.path.realpath(__file__))
        # The modules subdirectory
        self.module_path = os.path.join(self.curr_path, "modules" + os.sep)
        # Module instances
        self.modules = {}

    def load(self):
        """Find and load available modules."""
        self.logger.debug("Loading modules...")
        names = self.get_module_names()
        for name in names:
            module = self.load_single(name)
            if module:
                # Load and store the module instance
                inst = self.load_instance(module)
                if inst:
                    self.modules[module[0]] = inst

    def get_module_names(self):
        """Get names of loadable modules."""
        names = []
        dirlist = os.listdir(self.module_path)
        for item in dirlist:
            # Skip 'hidden' dot files and files beginning with and underscore
            if item.startswith((".", "_")):
                continue
            parts = item.split(".")
            if len(parts) < 2:
                # Can't find file extension
                continue
            name = parts[0]
            ext = parts[-1]
            # only load .py modules
            if ext != "py":
                continue
            names.append(name)
        return names

    def load_instance(self, module):
        """Initialize a module."""
        try:
            inst = module[1]["class"](self.app, module[0], module[1])  # Store the module instance
            return inst
        except:
            self.logger.error("Initializing module failed: {0}".format(module[0]), exc_info=True)
        return False

    def load_single(self, name):
        """Load single module file."""
        path = os.path.join(self.module_path, name+".py")
        try:
            mod = imp.load_source(name, path)
        except:
            self.logger.error("Failed loading module: {0}".format(name), exc_info=True)
            return False
        if "module" not in dir(mod):
            return False
        if "status" not in mod.module.keys():
            mod.module["status"] = False
        return name, mod.module

    def extract_docs(self):
        """Get names and docs of runnable modules and print as markdown."""
        names = sorted(self.get_module_names())
        for name in names:
            name, module = self.load_single(name)
            # Skip modules that can't be run expicitly
            if module["class"].run.__module__ == "suplemon.suplemon_module":
                continue
            # Skip undocumented modules
            if not module["class"].__doc__:
                continue
            docstring = module["class"].__doc__
            docstring = "\n    " + docstring.strip()

            doc = " * {0}\n{1}\n".format(name, docstring)
            print(doc)


if __name__ == "__main__":
    ml = ModuleLoader()
    ml.extract_docs()
