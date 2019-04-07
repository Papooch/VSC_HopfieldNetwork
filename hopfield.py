import numpy as np
import iofunc

class Hopfield():

    def __init__(self, dim = [1, 1]):
        self.method = 0
        self._dimensions = dim
        self._length = dim[0]*dim[1]
        self._patterns = []
        self._weightMatrix = np.zeros([dim[0] * dim[1], dim[0] * dim[1]])
        self._energy = 0.0
        #self._patternMatrices = []
        self._pixels = np.zeros(dim[0] * dim[1], dtype=int)

    def learnPattern(self, pattern):
        if self.method == 0:
            self._learnPatternHebbian(pattern)
        else:
            self._learnPatternStrokey(pattern)

    def _learnPatternStrokey(self, pattern):
        # W is the weight matrix of the new pattern
        pattern = np.array(pattern).reshape([1, self._length])[0]
        pattern = np.where(pattern==0, -1, pattern)
        N = len(pattern)
        W = np.zeros(self._weightMatrix.shape)

        for j in range(len(self._weightMatrix)):           
            for i in range(j):
                #print(i, ", ", j)
                #print(pattern[i])
                Hij = sum([self._weightMatrix[i, k] * pattern[k] for k in range(N) if k not in [i, j]])
                Hji = sum([self._weightMatrix[j, k] * pattern[k] for k in range(N) if k not in [i, j]])
                W[j, i] = W[i, j] = self._weightMatrix[i, j] + 1/N*(
                    pattern[i]*pattern[j] - pattern[i]*Hji - pattern[j]*Hij
                )
                #W[j, i] = W[i, j] = (2*pattern[i]-1)*(2*pattern[j]-1)
        self._weightMatrix -= W
        self._patterns.append(pattern)


    def _learnPatternHebbian(self, pattern):
        pattern = np.array(pattern, dtype=float).reshape([1, self._length])
        # W is the weight matrix of the new pattern
        W = (2*pattern[:].T-1) @ (2*pattern[:]-1)  
        # Explanation: 
        # W = np.zeros(self._weightMatrix.shape)
        # for j in range(len(self._weightMatrix)):           
        #    for i in range(j):
        #        W[j, i] = W[i, j] = (2*pattern[i]-1)*(2*pattern[j]-1)
        
        # Subtract self-weights on the diagonal
        W *= (1-np.eye(*self._weightMatrix.shape, dtype=float))
        self._weightMatrix += W
        self._patterns.append(pattern)
    
    def unlearnPattern(self, index):
        pattern = self._patterns[index]
        W = (2*pattern[:].T-1) @ (2*pattern[:]-1)
        W *= (1-np.eye(*self._weightMatrix.shape, dtype=float))
        self._weightMatrix -= W
        del self._patterns[index]

    def unlearnAll(self):
        # TODO:
        pass

    def setInitialState(self, pattern):
        self._pixels = np.array(pattern).reshape([1, self._length])[0]
        self._energy = 0.0
        S = self._pixels
        W = self._weightMatrix
        self._energy = -1/2*( S @ W @ S.T)
        

    def getWeightMatrix(self):
        return self._weightMatrix
    
    def getEnergy(self):
        return self._energy

    def updatePixel(self, id):
        deltaE = self._weightMatrix[id, :] @ self._pixels
        #print(self._weightMatrix[id, :], ".", self._pixels, "=",deltaE)
        lastPixel = self._pixels[id]        
        if deltaE >= 0:
            self._pixels[id] = 1
        else:
            self._pixels[id] = 0
        #print(self._pixels)
        if lastPixel != self._pixels[id]:

            return True
        else:
            return False
    
    def getPattern(self, id):
        return self._patterns[id].copy().reshape(self._dimensions)

    def getCurrentState(self):
        return self._pixels.copy().reshape(self._dimensions)


if __name__ == "__main__":

    mats = iofunc.readMatrixText("input/in3.txt")
    initMat = iofunc.readMatrixText("input/in3.txt")[0]
    #initMat = np.random.randint(0, 2, [len(mats[0]),len(mats[0][0])], dtype = int)
    #initMat = np.array([[1,1,1,0,1]])
    hopfield = Hopfield([len(initMat),len(initMat[0])])
    hopfield.method = 0

    for pattern in mats:
        hopfield.learnPattern(pattern)

    #print(hopfield._pixels)

    hopfield.setInitialState(initMat)
    print(hopfield._pixels)

    print(hopfield._weightMatrix)

    print("Start: \n", hopfield.getCurrentState())
    print(hopfield.getPattern(0))
    from random import shuffle
    order = [i for i in range(len(initMat)*len(initMat[0]))]
    for i in range(6):
        for o in order:
            shuffle(order)
            #print(hopfield.updatePixel(o))
            #print(hopfield.getCurrentState())
    print(hopfield.getCurrentState())