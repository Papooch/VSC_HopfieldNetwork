import numpy as np
import iofunc

class Hopfield():

    def __init__(self, dim = [1, 1]):
        self._gridDimensions = dim
        self._patterns = []
        self._weightMatrix = np.zeros([dim[0] * dim[1], dim[0] * dim[1]])
        #self._patternMatrices = []
        self._pixels = np.zeros(dim[0] * dim[1], dtype=int)

    def learnPattern(self, pattern):
        # W is the weight matrix of the new pattern
        pattern = np.array(pattern).reshape([1, len(pattern) * len(pattern[0])])[0]
        N = len(pattern)
        W = np.zeros(self._weightMatrix.shape)

        for j in range(len(self._weightMatrix)):
            
            for i in range(j):
                #print(i, ", ", j)
                #print(pattern[i])
                Hij = sum(self._weightMatrix[i, :] * pattern)
                Hji = sum(self._weightMatrix[j, :] * pattern)
                W[j, i] = W[i, j] = self._weightMatrix[i, j] + 1/N*(
                    pattern[i]*pattern[j] - pattern[i]*Hji - pattern[j]*Hij
                )
        self._weightMatrix += W
        pass
    
    def unlearnPattern(self, index):
        pass

    def unlearnAll(self):
        pass

    def setInitialState(self, pattern):
        self._pixels = np.array(pattern).reshape([1, len(pattern) * len(pattern[0])])[0]

    def getWeightMatrix(self):
        return self._weightMatrix


if __name__ == "__main__":
    #testPattern = np.array([[1, 0, 1], [0, 1, 1]])
    #testPattern2 = np.array([[1, 0, 1], [1, 1, 0]])
    #hopfield = Hopfield([2, 3])

    mats = iofunc.readMatrixText("input/in1.txt")
    hopfield = Hopfield([5, 4])

    for pattern in mats:
        hopfield.learnPattern(pattern)

    
    print(hopfield.getWeightMatrix())
    print(hopfield.getWeightMatrix().shape)