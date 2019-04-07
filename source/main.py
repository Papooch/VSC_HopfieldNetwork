import numpy as np
import time

import iofunc
from figures import Figures
from hopfield import Hopfield
from common import rollover

import mainwindow
from PyQt5 import QtWidgets, QtCore

class Settings():
    def __init__(self):
        self.ySize = 5
        self.xSize = 5
        self.distortion = 10
        self.animation = True
        self.animationSpeed = 10
        self.animationRunningFlag = False
        self.animationPrescaler = 10
        self.IOEnable = False

class Main():
    def __init__(self, ):
        self.settings = Settings()
        self.hopfield = None
        self.setupFigures([self.settings.xSize, self.settings.ySize])
        self.workspacePatterns = []
        self.learnedPatterns = []

    def resetEveryting(self):
        self.noOfWorkspace = 0
        self.noOfLearned = 0
        self.currentWorkspace = 0
        self.currentLearned = 0
        self.workspacePatterns.clear()
        self.learnedPatterns.clear()
        self.hopfield.unlearnAll()
        self.figLearned.clear()
        self.figWorkspace.clear()
        self.figIO.clear()
        self.workspaceToolsEnable(False)
        self.learnedToolsEnable(False)
        self.ioToolsEnable(False)
    
    def setupFigures(self, dim):
        self.figWorkspace = Figures(dim)
        self.figLearned = Figures(dim)
        self.figIO = Figures(dim)
        self.hopfield = Hopfield(dim)

    def applyDimensions(self, dim):
        self.resetEveryting()
        self.settings.ySize, self.settings.xSize = dim
        self.updateCountLabels()
        self.hopfield = Hopfield([self.settings.ySize, self.settings.xSize])
        #self.setupFigures(dim)

    def loadPatternsText(self, filename):
        try:
            loadedPatterns = iofunc.readMatrixTextMultipleFiles(filename)
            self.loadPatterns(loadedPatterns)
        except:
            QtWidgets.QMessageBox.warning(mainWindow, 'File error', "Bad input file fromat, see help for more info.")

    def loadPatternImage(self, filenames):
        try:
            for filename in filenames:
                loadedPattern = iofunc.readMatrixImage(filename)
                self.loadPatterns([loadedPattern])
        except:
            QtWidgets.QMessageBox.warning(mainWindow, 'File error', "Bad input file fromat, see help for more info.")

    def loadPatterns(self, loadedPatterns):
        #if the imported image is of different dimensions than loaded, reset all
        arr = self.figWorkspace.image.get_array()
        if  len(loadedPatterns[0]) > 150 or len(loadedPatterns[0][0]) > 150:
            QtWidgets.QMessageBox.warning(mainWindow, 'Size error', "Only patterns up to 150 pixels in either dimension can be loaded.")
            return
        if  (len(arr) != len(loadedPatterns[0])) or (len(arr[0]) != len(loadedPatterns[0][0])):
            self.applyDimensions([len(loadedPatterns[0]), len(loadedPatterns[0][0])])
            mainWindow.spnXSize.setValue(self.settings.xSize)
            mainWindow.spnYSize.setValue(self.settings.ySize)
            mainWindow.updateCanvasLearned()

        self.workspacePatterns.extend(loadedPatterns)

        self.figWorkspace.showPattern(self.workspacePatterns[-1])
        self.noOfWorkspace = len(self.workspacePatterns)
        self.currentWorkspace = len(self.workspacePatterns)-1
        self.updateCountLabels()
        self.workspaceToolsEnable(True)
        mainWindow.lblDrawErase.show()
        mainWindow.updateCanvasWorkspace()

    def saveWorkspacePatternText(self, filename):
        iofunc.writeMatrixText(filename, [self.workspacePatterns[self.currentWorkspace]])

    def saveAllWorkspacePatternsText(self, filename):
        iofunc.writeMatrixText(filename, self.workspacePatterns)

    def saveOutputText(self, filename):
        iofunc.writeMatrixText(filename, [self.figIO.arr])

    def learnFromFileText(self):
        pass

    def updateCountLabels(self):
        if not self.learnedPatterns:
            mainWindow.lblLearned.setText("0/0")
        else:
            mainWindow.lblLearned.setText("%d/%d" % (self.currentLearned+1, self.noOfLearned))
        if not self.workspacePatterns:
            mainWindow.lblWorkspace.setText("0/0")
        else:
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
    def learnPattern(self, _=None, pattern=None):
        if pattern is None:
            pattern = self.workspacePatterns[self.currentWorkspace]
        self.hopfield.learnPattern(pattern.copy())
        self.learnedPatterns.append(pattern.copy())
        self.noOfLearned = len(self.learnedPatterns)
        self.currentLearned = self.noOfLearned-1
        self.showLearnedNumber(self.currentLearned)
        self.learnedToolsEnable(True)
        mainWindow.updateCanvasLearned()

    def learnAllPatterns(self):
        for pattern in self.workspacePatterns:
            self.learnPattern(pattern=pattern)

    def unlearnPattern(self):
        if not self.learnedPatterns:
            return
        self.hopfield.unlearnPattern(self.currentLearned)
        del self.learnedPatterns[self.currentLearned]
        if not self.learnedPatterns:
            self.figLearned.clear()
            self.learnedToolsEnable(False)
            mainWindow.updateCanvasLearned()
        self.noOfLearned = len(self.learnedPatterns)
        self.updateCountLabels()
        self.showPreviousLearned()

    def unlearnAllPatterns(self):
        for _ in range(len(self.learnedPatterns)):
            self.unlearnPattern()

    #workspace control
    def newWorkspacePattern(self, _=None, pattern=None):
        mainWindow.lblDrawErase.show()
        self.workspaceToolsEnable(True)
        if pattern is None:
            pattern = np.ones([self.settings.ySize, self.settings.xSize], dtype = np.int16)

        self.workspacePatterns.append(pattern)
        self.figWorkspace.showPattern(self.workspacePatterns[-1])
        self.noOfWorkspace = len(self.workspacePatterns)
        self.currentWorkspace = len(self.workspacePatterns)-1
        self.updateCountLabels()
        mainWindow.updateCanvasWorkspace()

    def deleteWorkspacePattern(self):
        if not self.workspacePatterns:
            return
        pass
        del self.workspacePatterns[self.currentWorkspace]
        if not self.workspacePatterns:
            self.figWorkspace.clear()
            mainWindow.updateCanvasWorkspace()
            self.workspaceToolsEnable(False)
            mainWindow.lblDrawErase.hide()
        self.noOfWorkspace = len(self.workspacePatterns)
        self.updateCountLabels()
        self.showPreviousWorkspace()

    def clearWorkspacePattern(self):
        if not self.workspacePatterns:
            return
        self.workspacePatterns[self.currentWorkspace].fill(1)
        self.figWorkspace.showPattern(self.workspacePatterns[self.currentWorkspace])
        mainWindow.updateCanvasWorkspace()

    def duplicateWorkspacePattern(self):
        self.newWorkspacePattern(pattern=self.workspacePatterns[self.currentWorkspace].copy())

    # IO control
    def setWorkspaceAsInput(self):
        if not self.workspacePatterns:
            return
        self.figIO.showPattern(self.workspacePatterns[self.currentWorkspace].copy())
        self.ioToolsEnable(True)
        mainWindow.updateCanvasIO()

    def saveOutputToWorkspace(self):
        self.newWorkspacePattern(pattern=self.figIO.arr.copy())

    def distort(self):
        if not self.learnedPatterns:
            return
        pattern = self.learnedPatterns[self.currentLearned].copy()
        for pixel in np.nditer(pattern, op_flags=['readwrite']):
            if np.random.rand()*100 < self.settings.distortion:
                pixel[...] = 1-pixel
        self.figIO.showPattern(pattern)
        self.ioToolsEnable(True)
        mainWindow.updateCanvasIO()

    def solveFinished(self):
        self.hopfieldThread.exit()
        self.settings.animationRunningFlag = False
        self.solvingInProgress(False)
        mainWindow.btnSolve.setText("Reconstruct!")
        mainWindow.btnSetAsInput.setEnabled(True)
        mainWindow.actionWorkspaceSetAsInput.setEnabled(True)

    def solve(self):
        if self.settings.animationRunningFlag:
            self.settings.animationRunningFlag = False
            return

        self.hopfield.setInitialState(self.figIO.arr.copy())
        self.hopfieldThread = HopfieldThread(self.hopfield, self.figIO, mainWindow.canvasIO, self.settings)
        self.hopfieldThread.finished.connect(self.solveFinished)
        self.settings.animationRunningFlag = True

        self.solvingInProgress(True)
        mainWindow.btnSolve.setText("Stop")
        mainWindow.btnSetAsInput.setDisabled(True)
        mainWindow.actionWorkspaceSetAsInput.setDisabled(True)

        self.hopfieldThread.start()

    def workspaceToolsEnable(self, enable = True):
        mainWindow.btnSetAsInput.setEnabled(enable)
        mainWindow.actionWorkspaceSetAsInput.setEnabled(enable)
        mainWindow.btnDeletePattern.setEnabled(enable)
        mainWindow.btnClearPattern.setEnabled(enable)
        mainWindow.actionWorkspaceDuplicate.setEnabled(enable)
        mainWindow.actionWorkspaceDelete.setEnabled(enable)
        mainWindow.actionWorkspaceDeleteAll.setEnabled(enable)
        mainWindow.actionWorkspaceClear.setEnabled(enable)
        mainWindow.btnLearn.setEnabled(enable)
        mainWindow.btnLearnAll.setEnabled(enable)
        mainWindow.actionNetworkLearnWorkspace.setEnabled(enable)
        mainWindow.actionNetworkLearnAllWorkspace.setEnabled(enable)
        mainWindow.actionWorkspaceSaveCurrent.setEnabled(enable)
        mainWindow.actionWorkspaceSave.setEnabled(enable)

    def learnedToolsEnable(self, enable = True):
        mainWindow.btnDistort.setEnabled(enable)
        mainWindow.actionNetworkDistort.setEnabled(enable)
        mainWindow.btnUnlearn.setEnabled(enable)
        mainWindow.actionNetworkUnlearn.setEnabled(enable)
        mainWindow.actionNetworkUnlearnAll.setEnabled(enable)
    
    def ioToolsEnable(self, enable = True):
        mainWindow.btnSolve.setEnabled(enable)
        mainWindow.actionSolve.setEnabled(enable)
        mainWindow.btnSaveToWorkspace.setEnabled(enable)
        mainWindow.actionNetworkSaveToWorkspace.setEnabled(enable)
        mainWindow.actionNetworkSaveToFile.setEnabled(enable)

    def solvingInProgress(self, enable = True):
        mainWindow.btnSetAsInput.setEnabled(not enable)
        mainWindow.btnDistort.setEnabled(not enable)
        mainWindow.btnUnlearn.setEnabled(not enable)
        mainWindow.actionNetworkUnlearn.setEnabled(not enable)
        mainWindow.actionNetworkUnlearnAll.setEnabled(not enable)
        mainWindow.btnLearn.setEnabled(not enable)
        mainWindow.btnLearnAll.setEnabled(not enable)
        mainWindow.actionNetworkSaveToFile.setEnabled(not enable)


class HopfieldThread(QtCore.QThread):
    
    signal = QtCore.pyqtSignal(int)
    
    def __init__(self, hopfield, figure, canvas, settings):
        QtCore.QThread.__init__(self)
        self.hopfield = hopfield
        self.fig = figure
        self.canvas = canvas
        self.settings = settings
        self.iterationNo = 0

    def run(self):
        order = [i for i in range(len(self.fig.arr)*len(self.fig.arr[0]))]
        pixelChanged = True
        while pixelChanged:
            pixelChanged = False
            np.random.shuffle(order)
            for o in order:
                self.iterationNo += 1
                if not self.settings.animationRunningFlag:
                    return
                if self.hopfield.updatePixel(o):
                    pixelChanged = True
                if self.settings.animation and self.iterationNo >= self.settings.animationPrescaler:
                    time.sleep(0.2-(self.settings.animationSpeed/200))
                    self.fig.updatePattern(self.hopfield.getCurrentState())
                    self.canvas.draw()
                    self.iterationNo = 0

        self.fig.updatePattern(self.hopfield.getCurrentState())
        self.canvas.draw()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    
    main = Main()
    mainWindow = mainwindow.MainWindow(main)
    main.resetEveryting()
    mainWindow.addCanvases(main.figWorkspace.figure, main.figLearned.figure, main.figIO.figure)
    mainWindow.setupCallbacks()
    #main.loadPatterns("input/in1.txt")
    mainWindow.show()

    
    sys.exit(app.exec_())