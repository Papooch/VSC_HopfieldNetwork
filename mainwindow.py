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
        self.lblDrawErase.hide()

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

    def deleteWorkspaceAll(self):
        for _ in range(len(self.main.workspacePatterns)):
            self.main.deleteWorkspacePattern()

    def figureWorkspaceDrawCallback(self, event):
        if event.xdata == None:
            return
        value = 0
        if event.button == 1:
            value = 0
        elif event.button == 3:
            value = 1
        else:
            return
        self.main.figWorkspace.drawPixel(int(event.xdata + .5), int(event.ydata + .5), value)
        self.updateCanvasWorkspace()

    def setupCallbacks(self):
        #menu Workspace
        self.actionWorkspaceLoadText.triggered.connect(self.loadPatternsText)
        self.actionWorkspaceNew.triggered.connect(self.main.newWorkspacePattern)
        self.actionWorkspaceDelete.triggered.connect(self.main.deleteWorkspacePattern)
        self.actionWorkspaceDeleteAll.triggered.connect(self.deleteWorkspaceAll)

        #menu Network

        #buttons Workspace
        self.btnNewPattern.clicked.connect(self.main.newWorkspacePattern)
        self.btnDeletePattern.clicked.connect(self.main.deleteWorkspacePattern)
        #self.btnClearPattern.clicked
        #self.btnSetAsInput.clicked
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

        #figure Callbacks
        self.canvasWorkspace.mpl_connect('motion_notify_event', self.figureWorkspaceDrawCallback)
        self.canvasWorkspace.mpl_connect('button_press_event', self.figureWorkspaceDrawCallback)
        
        