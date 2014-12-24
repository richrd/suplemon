import json

class Config:
    def __init__(self, parent):
        self.parent = parent
        self.filename = "config.json"
        self.defaults = {
            "files": {},
            "editor": {
                "tab_width": 4,
                "cursor": "reverse",
            },
            "display": {
                "show_top_bar": True,
                "show_bottom_bar": True,
                "show_line_nums": True,
                "show_highlighting": False,
                "show_clock": True
            },
        }

        self.config = dict(self.defaults)

    def log(self, s):
        self.parent.logger.log(s)
        # FIXME: Pipe logging to app instance
        pass

    def load(self):
        #try:
            f = open(self.filename)
            data = f.read()
            f.close()
            self.config = json.loads(data)
        #except:
        #    self.log("Failed to load config file!")
        #    pass
        
    def store(self):
        data = json.dumps(self.config)
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

