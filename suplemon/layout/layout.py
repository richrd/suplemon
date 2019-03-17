
class Size(object):
    def __init__(self, width=0, height=0):
        self.width = width
        self.height = height

    def __len__(self):
        return 2

    def __getitem__(self, k):
        if k > 1:
            raise IndexError("Size indices must be 0 or 1 ({} was given)".format(k))
        return self.height if k else self.width

    def __setitem__(self, k, v):
        if k > 1:
            raise IndexError("Size indices must be 0 or 1")
        if k:
            self.height = v
        else:
            self.width = v

    def __repr__(self):
        return "Size(" + str(self.width) + ", " + str(self.height) + ")"


class Layout(object):
    # FIXME: Use or remove this class
    # TODO: This should probably keep track of all widgets
    pass

    def focus(self, target):
        # TODO: Focus a control
        pass

    def get_focusable(self):
        # TODO: Get focusable controls
        pass
