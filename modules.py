# -*- encoding: utf-8
"""
Addon module loader.
"""
import os
import imp

from helpers import *


class ModuleLoader:
    def __init__(self, app=None):
        self.app = app
        # The app root directory
        self.curr_path = os.path.dirname(os.path.realpath(__file__))
        # The modules subdirectory
        self.module_path = os.path.join(self.curr_path, "modules" + os.sep)
        # Module instances
        self.modules = {}

    def log(self, data, type=None):
        if self.app:
            self.app.log(data, type)
        else:
            print(data)

    def load(self):
        """Find and load available modules."""
        self.log("Loading modules...", LOG_INFO)
        dirlist = os.listdir(self.module_path)
        for item in dirlist:
            # Skip 'hidden' dot files
            if item[0] == ".":
                continue
            parts = item.split(".")
            if len(parts) < 2:
                continue
            name = parts[0]
            ext = parts[-1]

            # only load .py modules that don't begin with an underscore
            if ext == "py" and name[0] != "_":
                module = self.load_single(name)
                if module:
                    # Load and store the module instance
                    inst = self.load_instance(module)
                    if inst:
                        self.modules[module[0]] = inst

    def load_instance(self, module):
        """Initialize a module."""
        try:
            inst = module[1]["class"](self.app)  # Store the module instance
            inst.name = module[0]
            inst.options = module[1]
            return inst
        except:
            self.log("Initializing module failed: " + module[0])
            self.log(get_error_info())
        return False

    def load_single(self, name):
        """Load single module file."""
        path = os.path.join(self.module_path, name+".py")
        try:
            mod = imp.load_source(name, path)
        except:
            self.log("Failed loading module:"+str(name))
            self.log(traceback.format_exc())
            self.log(sys.exc_info()[0])
            return False
        if "module" not in dir(mod):
            return False
        if "status" not in mod.module.keys():
            mod.module["status"] = False
        return name, mod.module

if __name__ == "__main__":
    ml = ModuleLoader()
    ml.load()
