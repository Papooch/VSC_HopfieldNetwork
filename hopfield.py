import numpy as np

class Hopfield():

    def __init__(self, dim = [1, 1]):
        self._gridDimensions = dim
        self._patterns = []
        self._weightMatrix = np.zeros([dim[0]**2, dim[1]**2])
        self._pixels = np.zeros(dim[0] * dim[1], dtype=int)

    def learnPattern(self, pattern):
        pass
    
    def unlearnPattern(self, index):
        pass

    def unlearnAll(self):
        pass

    def setInitialState(self, pattern):
        self._pixels = pattern.reshape([1, len(pattern[0] + len(pattern[1]))])

    

if __name__ == "__main__":
    hopfield = Hopfield()
    