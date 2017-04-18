from PySide import QtCore, QtGui
import mirroratorUI as customUI
import mirroratorCore as mirroratorCore
from shiboken import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
reload(customUI)

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtGui.QWidget)
 
class ControlMainWindow(QtGui.QDialog):
 
    def __init__(self, parent=None):
 
        super(ControlMainWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self._mapped = 0
        self.ui =  customUI.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tolleranceLine.setValidator(QtGui.QDoubleValidator())
        icon = QtGui.QIcon(":/navButtonConnected.png")
        self.ui.baseObjectButton.setIcon(icon)
        

        self.ui.mapVerticesButton.clicked.connect(self.mapVertices)
        self.ui.baseObjectButton.clicked.connect(self.getSelection)
        
        self.ui.checkSymmetryButton.clicked.connect(self.checkSymmetry)
        self.ui.symmetricalMeshButton.clicked.connect(self.createSymmetricalMesh)

        self.ui.flipSelectionButton.clicked.connect(self.flipSelection)
        self.ui.mirrorSelectionLRButton.clicked.connect(self.mirrorSelectionLtoR)
        self.ui.mirrorSelectionRLButton.clicked.connect(self.mirrorSelectionRtoL)

        self.ui.revertToBaseButton.clicked.connect(self.revertToBase)
        self.ui.flipMeshButton.clicked.connect(self.flipMesh)
        self.ui.mirrorMeshLRButton.clicked.connect(self.mirrorMeshLtoR)
        self.ui.mirrorMeshRLButton.clicked.connect(self.mirrorMeshRtoL)

 
    def mapVertices(self):
        base = self.ui.baseObjectText.text();
        axis = str(self.ui.axisBox.currentText()).lower()
        space = str(self.ui.spaceBox.currentText()).lower()
        tolerance = float(self.ui.tolleranceLine.text())

        self._mirrorator = mirroratorCore.rig_mirrorator(base, space, axis, tolerance)
        self._mirrorator.buildSymmetryMap()
        self._mapped = 1

    def getSelection(self):
        selection = cmds.ls(sl=True)
        if selection:
            self.ui.baseObjectText.setText(selection[0])


    def checkSymmetry(self):

        selection = cmds.ls(sl=True)
        if self._mapped == 1:
            if selection:
                if len(selection) >= 1:
                    selection = selection[0]
                self._mirrorator.checkSymmetry(selection)
        else: 
            raise RuntimeError("Please build the symmetry map first.")


    def createSymmetricalMesh(self):

        cmds.undoInfo(openChunk=True)
        selection = cmds.ls(sl=True)
        if self._mapped == 1:
            if selection:
                if len(selection) >= 1:
                    selection = selection[0]
                self._mirrorator.createSymmetricalMesh(selection)
        else: 
            raise RuntimeError("Please build the symmetry map first.")
        cmds.undoInfo(closeChunk=True)


    def flipSelection(self):

        cmds.undoInfo(openChunk=True)
        selection = cmds.ls(sl=True, fl=True)
        if self._mapped == 1:
            if selection:
                self._mirrorator.flipSelection(selection)
        else: 
            raise RuntimeError("Please build the symmetry map first.")
        cmds.undoInfo(closeChunk=True)

    def mirrorSelectionLtoR(self):

        cmds.undoInfo(openChunk=True)
        selection = cmds.ls(sl=True, fl=True)
        if self._mapped == 1:
            if selection:
                self._mirrorator.mirrorSelectionLtoR(selection)
        else: 
            raise RuntimeError("Please build the symmetry map first.")
        cmds.undoInfo(closeChunk=True)

    def mirrorSelectionRtoL(self):

        cmds.undoInfo(openChunk=True)
        selection = cmds.ls(sl=True, fl=True)
        if self._mapped == 1:
            if selection:
                self._mirrorator.mirrorSelectionRtoL(selection)
        else: 
            raise RuntimeError("Please build the symmetry map first.")
        cmds.undoInfo(closeChunk=True)


    def revertToBase(self):

        cmds.undoInfo(openChunk=True)
        selection = cmds.ls(sl=True)
        if self._mapped == 1:
            if selection:
                if len(selection) >= 1:
                    selection = selection[0]
                self._mirrorator.revertToBase(selection)
        else: 
            raise RuntimeError("Please build the symmetry map first.")
        cmds.undoInfo(closeChunk=True)

    def mirrorMeshLtoR(self):

        cmds.undoInfo(openChunk=True)
        selection = cmds.ls(sl=True)
        if self._mapped == 1:
            if selection:
                if len(selection) >= 1:
                    selection = selection[0]
                self._mirrorator.mirrorLtoR(selection)
        else: 
            raise RuntimeError("Please build the symmetry map first.")
        cmds.undoInfo(closeChunk=True)

    def mirrorMeshRtoL(self):

        cmds.undoInfo(openChunk=True)
        selection = cmds.ls(sl=True)
        if self._mapped == 1:
            if selection:
                if len(selection) >= 1:
                    selection = selection[0]
                self._mirrorator.mirrorRtoL(selection)
        else: 
            raise RuntimeError("Please build the symmetry map first.")
        cmds.undoInfo(closeChunk=True)

    def flipMesh(self):

        cmds.undoInfo(openChunk=True)
        selection = cmds.ls(sl=True)
        if self._mapped == 1:
            if selection:
                if len(selection) >= 1:
                    selection = selection[0]
                self._mirrorator.flipTarget(selection)
        else: 
            raise RuntimeError("Please build the symmetry map first.")
        cmds.undoInfo(closeChunk=True)

try:
    myWin.deleteLater()
except NameError as e:
    pass
    
myWin = ControlMainWindow(parent=maya_main_window())
myWin.show()
