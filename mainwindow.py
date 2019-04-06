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

    def loadPatterns(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Text Files (*.txt)")
        if not filename:
            return
        self.main.loadPatterns(filename)

    def setupCallbacks(self):
        self.actionLoad_text.triggered.connect(self.loadPatterns)
        self.btnWorkspaceLeft.clicked.connect(self.main.showPreviousWorkspace)
        self.btnWorkspaceRight.clicked.connect(self.main.showNextWorkspace)
        self.btnLearnedLeft.clicked.connect(self.main.showPreviousLearned)
        self.btnLearnedRight.clicked.connect(self.main.showNextLearned)
        self.btnLearn.clicked.connect(self.main.learnPattern)
        self.btnUnlearn.clicked.connect(self.main.unlearnPattern)