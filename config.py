

class Config:
    def __init__(self):
        self.filename = "config.txt"
        self.config = {
            "files":{}
        }
        
    def load(self):
        try:
            f = open(self.filename)
            data = f.read()
            f.close()
            self.config = eval(data)
        except:
            pass
        
    def store(self):
        data = str(self.config)
        f = open(self.filename)
        f.write(data)
        f.close()


