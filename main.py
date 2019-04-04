from PyQt5.uic import loadUiType
from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.figure import Figure

from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

import numpy as np
from matplotlib import pyplot

import iofunc
from hopfield import Hopfield


Ui_MainWindow, QMainWindow = loadUiType('HopfieldUI.ui')

def clamp(minv, maxv, value):
    return min(max(minv, value), maxv)

class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self, ):
        super(MainWindow, self).__init__()
        self.setupUi(self)

    def addCanvases(self, fWorkspace, fLearned, fIO):
        self.canvasWorkspace = FigureCanvas(fWorkspace)
        self.canvasLearned = FigureCanvas(fLearned)
        self.canvasIO = FigureCanvas(fIO)
        self.mplWorkspaceLayout.addWidget(self.canvasWorkspace)
        self.mplLearnedLayout.addWidget(self.canvasLearned)
        self.mplIOLayout.addWidget(self.canvasIO)
        self.canvasWorkspace.draw()
        self.canvasWorkspace.draw()
        self.canvasWorkspace.draw()
        self.canvasList = [self.canvasWorkspace, self.canvasLearned, self.canvasIO]
        self.mplLayoutList = [self.mplWorkspaceLayout, self.mplLearnedLayout, self.mplIOLayout]

    def removeFigures(self):
        for i in range(3):
            self.mplLayoutList[i].removeWidget(self.canvasList[i])
            self.canvasList[i].close()

    def updateCanvasWorkspace(self):
        self.canvasWorkspace.draw()

    def updateCanvasLearned(self):
        self.canvasLearned.draw()

    def updateCanvasIO(self):
        self.canvasIO.draw()

    def loadPatterns(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Text Files (*.txt)")
        if not filename:
            return
        main.loadPatterns(filename)

    def setupCallbacks(self):
        self.actionLoad_text.triggered.connect(self.loadPatterns)
        self.btnWorkspaceLeft.clicked.connect(main.showPreviousWorkspace)
        self.btnWorkspaceRight.clicked.connect(main.showNextWorkspace)
        self.btnLearnedLeft.clicked.connect(main.showPreviousLearned)
        self.btnLearnedRight.clicked.connect(main.showNextLearned)
        self.btnLearn.clicked.connect(main.learnPattern)

class Settings():
    def __init__(self):
        self.ySize = 5
        self.xSize = 5
        self.distortion = 10
        self.animationSpeed = 5


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
        self.showPattern([[1]])

    def showPattern(self, pattern):
        self.ax.clear()
        self.arr = pattern
        self.image = self.ax.imshow(self.arr, cmap = 'gray')
        return self.figure

    def updatePattern(self, pattern):
        self.arr = pattern
        self.image.set_data(self.arr)
        return self.figure


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
        self.currentWorkspace = clamp(0, self.noOfWorkspace-1, self.currentWorkspace+1)
        self.showWorkspaceNumber(self.currentWorkspace)

    def showPreviousWorkspace(self):
        self.currentWorkspace = clamp(0, self.noOfWorkspace-1, self.currentWorkspace-1)
        self.showWorkspaceNumber(self.currentWorkspace)

    def showWorkspaceNumber(self, number):
        if not self.workspacePatterns:
            return
        self.figWorkspace.showPattern(self.workspacePatterns[number])
        self.updateCountLabels()
        mainWindow.updateCanvasWorkspace()

    #learned
    def showNextLearned(self):
        self.currentLearned = clamp(0, self.noOfLearned-1, self.currentLearned+1)
        self.showLearnedNumber(self.currentLearned)

    def showPreviousLearned(self):
        self.currentLearned = clamp(0, self.noOfLearned-1, self.currentLearned-1)
        self.showLearnedNumber(self.currentLearned)

    def showLearnedNumber(self, number):
        if not self.learnedPatterns:
            return
        self.figLearned.showPattern(self.learnedPatterns[number])
        self.updateCountLabels()
        mainWindow.updateCanvasLearned()

    def learnPattern(self):
        pattern = self.workspacePatterns[self.currentWorkspace]
        self.hopfield.learnPattern(pattern)
        self.learnedPatterns.append(pattern)
        self.noOfLearned = len(self.learnedPatterns)
        self.currentLearned = self.noOfLearned-1
        self.showLearnedNumber(self.currentLearned)
        mainWindow.updateCanvasLearned()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    
    main = Main()
    
    mainWindow = MainWindow()
    mainWindow.setupCallbacks()
    mainWindow.addCanvases(main.figWorkspace.figure, main.figLearned.figure, main.figIO.figure)
    #main.loadPatterns("input/in1.txt")
    mainWindow.show()

    
    sys.exit(app.exec_())