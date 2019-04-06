from PyQt5.uic import loadUiType
from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from main import Main

Ui_MainWindow, QMainWindow = loadUiType('HopfieldUI.ui')

class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self, main):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.main = main

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

    def loadPatternsText(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Text Files (*.txt)")
        if not filename:
            return
        self.main.loadPatternsText(filename)

    def applySettings(self):
        self.main.applyDimensions([self.spnYSize.value(), self.spnXSize.value()])
        self.updateCanvasWorkspace()
        self.updateCanvasLearned()

    def setupCallbacks(self):
        #menu Workspace
        self.actionWorkspaceLoadText.triggered.connect(self.loadPatternsText)

        #menu Network

        #buttons Workspace
        self.btnWorkspaceLeft.clicked.connect(self.main.showPreviousWorkspace)
        self.btnWorkspaceRight.clicked.connect(self.main.showNextWorkspace)

        #buttons Network
        self.btnLearnedLeft.clicked.connect(self.main.showPreviousLearned)
        self.btnLearnedRight.clicked.connect(self.main.showNextLearned)
        self.btnUnlearn.clicked.connect(self.main.unlearnPattern)

        #buttons Learn
        self.btnLearn.clicked.connect(self.main.learnPattern)
        
        #buttons Settings
        self.btnApplySettings.clicked.connect(self.applySettings)
        