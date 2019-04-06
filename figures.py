import numpy as np
from matplotlib.figure import Figure

class Figures():
    def __init__(self, dim=[1,1]):
        self.arr = np.array(dim, dtype = int)
        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        self.ax.tick_params(
            axis='both',
            which='both',
            bottom = False,
            left = False,
            labelbottom = False,
            labelleft = False
        )
        self.figure.tight_layout()
        self.showPattern([[0]])
        self.clear()

    def showPattern(self, pattern):
        self.ax.clear()
        self.arr = pattern
        self.image = self.ax.imshow(self.arr, cmap = 'gray')
        return self.figure

    def updatePattern(self, pattern):
        self.arr = pattern
        self.image.set_data(self.arr)
        return self.figure

    def clear(self):
        self.ax.clear()
        return self.figure
