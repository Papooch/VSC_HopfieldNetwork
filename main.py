import numpy as np

import iofunc
from figures import Figures
from hopfield import Hopfield
from common import clamp

import mainwindow
from mainwindow import QtWidgets

class Settings():
    def __init__(self):
        self.ySize = 5
        self.xSize = 5
        self.distortion = 10
        self.animationSpeed = 5

class Main():
    def __init__(self, ):
        self.settings = Settings()
        self.hopfield = None
        self.setupFigures([self.settings.xSize, self.settings.ySize])
        self.workspacePatterns = []
        self.learnedPatterns = []
        self.resetEveryting()

    def resetEveryting(self):
        self.noOfWorkspace = 0
        self.noOfLearned = 0
        self.currentWorkspace = 0
        self.currentLearned = 0
        self.workspacePatterns.clear()
        self.learnedPatterns.clear()
        self.hopfield.unlearnAll()
    
    def setupFigures(self, dim):
        self.figWorkspace = Figures(dim)
        self.figLearned = Figures(dim)
        self.figIO = Figures(dim)
        self.hopfield = Hopfield(dim)

    def applyDimensions(self, dim):
        self.resetEveryting()
        self.settings.xSize, self.settings.ySize = dim
        #self.setupFigures(dim)

    def loadPatterns(self, filename):
        loadedPatterns = iofunc.readMatrixTextMultipleFiles(filename)

        #if the imported image is of different dimensions than loaded, reset all
        arr = self.figWorkspace.image.get_array()        
        if  (len(arr) != len(loadedPatterns[0])) or (len(arr[0]) != len(loadedPatterns[0][0])):
            self.applyDimensions([len(loadedPatterns[0]), len(loadedPatterns[0][0])])
            self.figLearned.clear()
            mainWindow.updateCanvasLearned()

        self.hopfield = Hopfield([self.settings.xSize, self.settings.ySize])

        self.workspacePatterns.extend(loadedPatterns)

        self.figWorkspace.showPattern(self.workspacePatterns[-1])
        self.noOfWorkspace = len(self.workspacePatterns)
        self.currentWorkspace = len(self.workspacePatterns)-1
        self.updateCountLabels()
        mainWindow.updateCanvasWorkspace()

    def updateCountLabels(self):
        if not self.learnedPatterns:
            mainWindow.lblLearned.setText("0/0")
        else:
            mainWindow.lblLearned.setText("%d/%d" % (self.currentLearned+1, self.noOfLearned))
        mainWindow.lblWorkspace.setText("%d/%d" % (self.currentWorkspace+1, self.noOfWorkspace))
    
    #workspace
    def showNextWorkspace(self):
        if not self.workspacePatterns:
            return
        self.currentWorkspace = rollover(0, self.noOfWorkspace-1, self.currentWorkspace+1)
        self.showWorkspaceNumber(self.currentWorkspace)

    def showPreviousWorkspace(self):
        if not self.workspacePatterns:
            return
        self.currentWorkspace = rollover(0, self.noOfWorkspace-1, self.currentWorkspace-1)
        self.showWorkspaceNumber(self.currentWorkspace)

    def showWorkspaceNumber(self, number):
        if not self.workspacePatterns:
            return
        self.figWorkspace.showPattern(self.workspacePatterns[number])
        self.updateCountLabels()
        mainWindow.updateCanvasWorkspace()

    #learned
    def showNextLearned(self):
        if not self.learnedPatterns:
            return
        self.currentLearned = rollover(0, self.noOfLearned-1, self.currentLearned+1)
        self.showLearnedNumber(self.currentLearned)

    def showPreviousLearned(self):
        if not self.learnedPatterns:
            return
        self.currentLearned = rollover(0, self.noOfLearned-1, self.currentLearned-1)
        self.showLearnedNumber(self.currentLearned)

    def showLearnedNumber(self, number):
        if not self.learnedPatterns:
            self.figLearned.clear()
            mainWindow.updateCanvasLearned()
            return
        self.figLearned.showPattern(self.learnedPatterns[number])
        self.updateCountLabels()
        mainWindow.updateCanvasLearned()
    
    #---
    def learnPattern(self):
        pattern = self.workspacePatterns[self.currentWorkspace]
        self.hopfield.learnPattern(pattern)
        self.learnedPatterns.append(pattern)
        self.noOfLearned = len(self.learnedPatterns)
        self.currentLearned = self.noOfLearned-1
        self.showLearnedNumber(self.currentLearned)
        mainWindow.updateCanvasLearned()

    def unlearnPattern(self):
        if not self.learnedPatterns:
            return
        self.hopfield.unlearnPattern(self.currentLearned)
        del self.learnedPatterns[self.currentLearned]
        if not self.learnedPatterns:
            self.figLearned.clear()
            mainWindow.updateCanvasLearned()
        self.noOfLearned = len(self.learnedPatterns)
        self.updateCountLabels()
        self.showNextLearned()



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    
    main = Main()
    
    mainWindow = mainwindow.MainWindow(main)
    mainWindow.setupCallbacks()
    mainWindow.addCanvases(main.figWorkspace.figure, main.figLearned.figure, main.figIO.figure)
    #main.loadPatterns("input/in1.txt")
    mainWindow.show()

    
    sys.exit(app.exec_())