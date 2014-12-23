import json

class Config:
    def __init__(self):
        self.filename = "config.json"
        self.defaults = {
            "files":{},
            "tab_width":4,
            "display": {
                "show_top_bar": True,
                "show_bottom_bar": True,
                "show_line_nums": True,
                "show_highlighting": False,
            },
        }

        self.config = dict(self.defaults)

    def log(self, s):
        # FIXME: Pipe logging to app instance
        pass

    def load(self):
        try:
            f = open(self.filename)
            data = f.read()
            f.close()
            self.config = eval(data)
        except:
            self.log("Failed to load config file!")
            pass
        
    def store(self):
        data = str(self.config)
        f = open(self.filename)
        f.write(data)
        f.close()
 
    def __getitem__(self, i):
        return self.config[i]

    def __setitem__(self, i, v):
        self.config[i] = v

    def __str__(self):
        return str(self.config)

    def __len__(self):
        return len(self.config)

