"""
Addon module loader.
"""
import os
import imp

from helpers import *

class ModuleLoader:
    def __init__(self):
        self.curr_path = os.path.dirname(os.path.realpath(__file__))
        self.module_path = os.path.join(self.curr_path, "modules" + os.sep)
        self.modules = {}
    
    def load(self):
        dirlist = os.listdir(self.module_path)
        modules = {}
        for item in dirlist:
            if item[0] == ".":
                continue
            parts = item.split(".")
            if len(parts) < 2:
                return False
            name = parts[0]
            ext = parts[-1]
        
            # only load .py modules that don't begin with an underscore
            if ext == "py" and name[0] != "_":
                #module = self.load_single(item)
                module = self.load_single(name)
                if module:
                    #self.modules[module[0]] = module[1]["class"]() # Store the module instance
                    self.modules[module[0]] = self.load_instance(module) # Load and store the module instance

    def load_instance(self, module):
        inst = module[1]["class"]() # Store the module instance
        inst.name = module[0]
        inst.options = module[1]
        return inst
    
    def load_single(self, name):
        path = os.path.join(self.module_path, name+".py")
        try:
            mod = imp.load_source(name, path)
            if not "module" in dir(mod):
                return False
            if not "status" in mod.module.keys():
                mod.module["status"] = False
            return name, mod.module
        except:
            print("Failed loading:", name)
            print(traceback.format_exc())
            print(sys.exc_info()[0])
            return False

if __name__ == "__main__":
    ml = ModuleLoader()
    ml.load()
