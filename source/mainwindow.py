from PyQt5.uic import loadUiType
from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from main import Main

import os
dirname = os.path.dirname(__file__)

Ui_MainWindow, QMainWindow = loadUiType(os.path.join(dirname, 'HopfieldUI.ui'))

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
        filename, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", dirname,"Text Files (*.txt);;All Files (*)")
        if not filename:
            return
        self.main.loadPatternsText(filename)

    def loadPatternImage(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", dirname,"Image Files (*.jpg *.png *.bmp);;All Files (*)")
        if not filename:
            return
        self.main.loadPatternImage(filename)

    def savePatternText(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', "pattern.txt", 'Text Files (*.txt);;All Files (*)')
        if not filename:
            return
        self.main.saveWorkspacePatternText(filename)

    def saveAllWorkspacePattternsText(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', os.path.join(dirname, "patterns.txt"), 'Text Files (*.txt);;All Files (*)')
        if not filename:
            return
        self.main.saveAllWorkspacePatternsText(filename)

    def saveOutputText(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', os.path.join(dirname, "patterns.txt"), 'Text Files (*.txt);;All Files (*)')
        if not filename:
            return
        self.main.saveOutputText(filename)

    def applySettings(self):
        self.main.applyDimensions([self.spnYSize.value(), self.spnXSize.value()])
        self.updateCanvasWorkspace()
        self.updateCanvasLearned()

    def deleteWorkspaceAll(self):
        for _ in range(len(self.main.workspacePatterns)):
            self.main.deleteWorkspacePattern()

    def setDistortion(self): 
        self.main.settings.distortion = self.spnDistortion.value()

    def setAnimaiton(self):
        self.main.settings.animation = self.chkAnimation.isChecked()

    def setAnimationSpeed(self):
        self.main.settings.animationSpeed = self.sldAnimationSpeed.value()

    def setAnimationPrescaler(self):
        self.main.settings.animationPrescaler = self.spnAnimationPrescaler.value()

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
        self.actionWorkspaceLoadImage.triggered.connect(self.loadPatternImage)
        self.actionWorkspaceNew.triggered.connect(self.main.newWorkspacePattern)
        self.actionWorkspaceDelete.triggered.connect(self.main.deleteWorkspacePattern)
        self.actionWorkspaceDeleteAll.triggered.connect(self.deleteWorkspaceAll)
        self.actionWorkspaceClear.triggered.connect(self.main.clearWorkspacePattern)
        self.actionWorkspaceDuplicate.triggered.connect(self.main.duplicateWorkspacePattern)
        self.actionWorkspaceSetAsInput.triggered.connect(self.main.setWorkspaceAsInput)
        self.actionWorkspaceSaveCurrent.triggered.connect(self.savePatternText)
        self.actionWorkspaceSave.triggered.connect(self.saveAllWorkspacePattternsText)

        #menu Network
        self.actionNetworkDistort.triggered.connect(self.main.distort)
        self.actionNetworkUnlearn.triggered.connect(self.main.unlearnPattern)
        self.actionNetworkSaveToWorkspace.triggered.connect(self.main.saveOutputToWorkspace)
        self.actionNetworkSaveToFile.triggered.connect(self.saveOutputText)
        self.actionNetworkUnlearnAll.triggered.connect(self.main.unlearnAllPatterns)
        self.actionNetworkLearnWorkspace.triggered.connect(self.main.learnPattern)
        self.actionNetworkLearnAllWorkspace.triggered.connect(self.main.learnAllPatterns)

        #buttons Workspace
        self.btnNewPattern.clicked.connect(self.main.newWorkspacePattern)
        self.btnDeletePattern.clicked.connect(self.main.deleteWorkspacePattern)
        self.btnClearPattern.clicked.connect(self.main.clearWorkspacePattern)
        self.btnSetAsInput.clicked.connect(self.main.setWorkspaceAsInput)
        self.btnWorkspaceLeft.clicked.connect(self.main.showPreviousWorkspace)
        self.btnWorkspaceRight.clicked.connect(self.main.showNextWorkspace)

        #buttons Network
        self.btnLearnedLeft.clicked.connect(self.main.showPreviousLearned)
        self.btnLearnedRight.clicked.connect(self.main.showNextLearned)
        self.btnUnlearn.clicked.connect(self.main.unlearnPattern)
        self.btnDistort.clicked.connect(self.main.distort)
        self.btnSaveToWorkspace.clicked.connect(self.main.saveOutputToWorkspace)
        self.btnSolve.clicked.connect(self.main.solve)

        #buttons Learn
        self.btnLearn.clicked.connect(self.main.learnPattern)
        self.btnLearnAll.clicked.connect(self.main.learnAllPatterns)
        
        #buttons Settings
        self.btnApplySettings.clicked.connect(self.applySettings)
        self.spnDistortion.valueChanged.connect(self.setDistortion)
        self.chkAnimation.toggled.connect(self.setAnimaiton)
        self.sldAnimationSpeed.valueChanged.connect(self.setAnimationSpeed)
        self.spnAnimationPrescaler.valueChanged.connect(self.setAnimationPrescaler)

        #figure Callbacks
        self.canvasWorkspace.mpl_connect('motion_notify_event', self.figureWorkspaceDrawCallback)
        self.canvasWorkspace.mpl_connect('button_press_event', self.figureWorkspaceDrawCallback)
        
        