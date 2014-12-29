
class Logger:
    def __init__(self, filename="log.txt"):
        self.filename = "filename"
        self.lines = []

    def log(self, data):
        self.lines.append(str(data))

    def output(self):
        for line in self.lines:
            try:
                print(line)
            except:
                pass
            
