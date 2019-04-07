import numpy as np
from matplotlib.figure import Figure
import warnings
warnings.filterwarnings("ignore", message="tight_layout : falling back to Agg renderer")

class Figures():
    def __init__(self, dim=[1,1]):
        self._lastX = 0
        self._lastY = 0

        self.arr = np.array(dim, dtype = 'int')
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
        self.figure.tight_layout(pad=0)
        self.showPattern([[0]])
        self.clear()

    def showPattern(self, pattern):
        self.ax.clear()
        self.arr = pattern
        self.image = self.ax.imshow(self.arr, cmap = 'gray', vmin=0, vmax=1)
        return self.figure

    def updatePattern(self, pattern):
        self.arr = pattern
        self.image.set_data(self.arr)
        return self.figure

    def clear(self):
        self.ax.clear()
        return self.figure

    def drawPixel(self, x, y, value):
        self.arr[y, x] = value
        self.image.set_data(self.arr)
        return self.figure

