"""
=======================================
MIRRORATOR - Developed by Daniele Dolci  2017
=======================================
"""

import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

class rig_mirrorator(object):
    """
    """
    def __init__(self, baseObject, pivot, axis, tolerance):
        """
        baseObject = symmetrical base mesh
        pivot = origin of axis or bounding box pivot
        axis = x, y, z
        """
        self._baseObject = baseObject
        self._tolerance = tolerance

        self._translationMirror = []
        self._index = None
        self._pivot = pivot
        self._space = True
        self.setMirror(axis)
        self.setPivot(pivot)
    
    def setPivot(self, value):
        """
        world or local
        """
        if value == "world":
            self._space = True
        elif value == "local":
            self._space = False

    def setMirror(self, value):
        """
        """
        if value == "x":
            self._translationMirror = [-1, 1, 1]
            self._index = 0
        if value == "y":
            self._translationMirror = [1, -1, 1]
            self._index = 1
        if value == "z":
            self._translationMirror = [1, 1, -1]
            self._index = 2


    def buildSymmetryMap(self):
        """
        """
        vtxs = [] 

        
        if cmds.objExists(self._baseObject):
            #vtxs = cmds.ls("{0}.vtx[*]".format(self._baseObject), fl=True)
            mPoint = OpenMaya.MPointArray()
            mSpace = None

            if self._pivot == 'local':
                mSpace = OpenMaya.MSpace.kObject
            elif self._pivot == 'world': 
                mSpace = OpenMaya.MSpace.kWorld

            selectionList = OpenMaya.MSelectionList()
            try:
                selectionList.add(self._baseObject)
            except:
                return None

            dagPath = OpenMaya.MDagPath()
            selectionList.getDagPath( 0, dagPath )
            

            mFnSet = OpenMaya.MFnMesh(dagPath)
            mFnSet.getPoints(mPoint, mSpace)

            for x in range(0, mPoint.length()):
                vtxs.append([mPoint[x][0], mPoint[x][1], mPoint[x][2]])
                    

        else:
            raise RuntimeError  

        LeftSideVtx = []
        LeftSidePos = []
        MiddleVtx = []
        RightSideVtx = []
        TempSideVtx = []
        TempSidePos = []

        
        for i in range(len(vtxs)):
            vtxPos = vtxs[i][self._index]
            if  vtxPos > self._tolerance :      
                LeftSideVtx.append("{0}.vtx[{1}]".format(self._baseObject, i))
                LeftSidePos.append(vtxs[i])

            elif (vtxPos <= self._tolerance and vtxPos >= 0) or (vtxPos >= self._tolerance*-1 and vtxPos <= 0):
                MiddleVtx.append("{0}.vtx[{1}]".format(self._baseObject, i))
            else:
                TempSideVtx.append("{0}.vtx[{1}]".format(self._baseObject, i))
                TempSidePos.append(vtxs[i])


        toRemoveFromLeftSide = []
        for e, lVtxPos in enumerate(LeftSidePos): 
            lastRightSideVtx = None
            if len(RightSideVtx) >= 1:      
                lastRightSideVtx = RightSideVtx[-1]
            for i in range(len(TempSidePos)):
                vtxPos = TempSidePos[i]
                vtx = TempSideVtx[i]                       
                check = 0
                for x, pos in enumerate(vtxPos):
                    if x == self._index:
                        pos = pos*self._translationMirror[self._index]
                    delta = lVtxPos[x] - pos
                    if delta < 0:
                        delta = delta*-1
                    if delta <= self._tolerance:
                        check += 1
                    else:
                        break
                if check == 3:  
                    RightSideVtx.append(vtx)
                    break
            if len(RightSideVtx) >= 1:  
                newLastRightSideVtx = RightSideVtx[-1]
                if lastRightSideVtx == newLastRightSideVtx:
                    toRemoveFromLeftSide.append(LeftSideVtx[e])
            else:
                toRemoveFromLeftSide.append(LeftSideVtx[e])

        
        for v in toRemoveFromLeftSide:
            if v in LeftSideVtx:
                LeftSideVtx.remove(v)
        
        
        asymmetricalVertices = cmds.ls("{0}.vtx[*]".format(self._baseObject), fl=True) 
        if len(asymmetricalVertices) != len(LeftSideVtx+RightSideVtx+MiddleVtx):
            for v in LeftSideVtx+RightSideVtx+MiddleVtx:
                if v in asymmetricalVertices:
                    asymmetricalVertices.remove(v)      
        else:
            asymmetricalVertices = []
        
        cmds.select(asymmetricalVertices)
        self._LeftSideVtx = LeftSideVtx
        self._MiddleVtx = MiddleVtx
        self._RightSideVtx = RightSideVtx 
        self._vtxs = vtxs

    def getSelectedObject(self, value):
        """
        """

        selectedObject = value.split(".")[0]
        if selectedObject != self._baseObject:
            return selectedObject

        return self._baseObject
        
    def mirrorSelectionLtoR(self, value):
        """
        value = [vertices]
        """
        cmds.select(clear=True)
        toSelect = []
        for v in value:
            selectedObject = self.getSelectedObject(v)
            if selectedObject != self._baseObject:
                v = v.replace(selectedObject, self._baseObject)
            if v in self._LeftSideVtx:
                toSelect.append(v.replace(self._baseObject, selectedObject))
                toSelect.append(self._RightSideVtx[self._LeftSideVtx.index(v)].replace(self._baseObject, selectedObject))
            elif v in self._MiddleVtx:
                toSelect.append(v.replace(self._baseObject, selectedObject))

        cmds.select(toSelect)

    def mirrorSelectionRtoL(self, value):
        """
        value = [vertices]
        """
        cmds.select(clear=True)
        toSelect = []
        for v in value:
            selectedObject = self.getSelectedObject(v)
            if selectedObject != self._baseObject:
                v = v.replace(selectedObject, self._baseObject)
            if v in self._RightSideVtx:
                toSelect.append(v.replace(self._baseObject, selectedObject))
                toSelect.append(self._LeftSideVtx[self._RightSideVtx.index(v)].replace(self._baseObject, selectedObject))
            elif v in self._MiddleVtx:
                toSelect.append(v.replace(self._baseObject, selectedObject))

        cmds.select(toSelect)

    def flipSelection(self, value):
        """
        """
        cmds.select(clear=True)

        toSelect = []
        for v in value:
            selectedObject = self.getSelectedObject(v)
            if selectedObject != self._baseObject:
                v = v.replace(selectedObject, self._baseObject)
            if v in self._LeftSideVtx:
                toSelect.append(self._RightSideVtx[self._LeftSideVtx.index(v)].replace(self._baseObject, selectedObject))
            elif v in self._RightSideVtx:
                toSelect.append(self._LeftSideVtx[self._RightSideVtx.index(v)].replace(self._baseObject, selectedObject))
            else:
                toSelect.append(v.replace(self._baseObject, selectedObject))

        cmds.select(toSelect)       

    def createSymmetricalMesh(self, value):
        """
        average of asymmetrical vertices
        """
        asymmetricalVertices = self.checkSymmetry(value)
        leftAsymV = asymmetricalVertices[0]
        rightAsymV = asymmetricalVertices[1]

        for v, u in zip(leftAsymV, rightAsymV):
            vPos = cmds.xform(v, q=True, ws=self._space, t=True)
            uPos = cmds.xform(u, q=True, ws=self._space, t=True)
            uPosReverted = [uPos[0]*self._translationMirror[0], uPos[1]*self._translationMirror[1], uPos[2]*self._translationMirror[2]]
            newPos = [(vPos[0]+uPosReverted[0])/2, (vPos[1]+uPosReverted[1])/2, (vPos[2]+uPosReverted[2])/2]
            cmds.xform(v, ws=self._space, t=[newPos[0], newPos[1], newPos[2]])
            cmds.xform(u, ws=self._space, t=[newPos[0]*self._translationMirror[0], newPos[1]*self._translationMirror[1], newPos[2]*self._translationMirror[2]])

    def revertToBase(self, value):
        """
        revert target to base
        """
        if cmds.objExists(value):
            for baseV in self._LeftSideVtx+self._MiddleVtx+self._RightSideVtx:
                targetV = baseV.replace(self._baseObject, value)
                basePos = cmds.xform(baseV, q=True, ws=False, t=True)
                targetPos = cmds.xform(targetV, q=True, ws=False, t=True)
                if basePos != targetPos:
                    cmds.xform(targetV, ws=False, t=basePos)

    def mirrorLtoR(self, value):
        """
        mirror object from left to right LOCALLY
        """
        if cmds.objExists(value):
            asymmetricalVertices = self.checkSymmetry(value)
            leftAsymV = asymmetricalVertices[0]
            rightAsymV = asymmetricalVertices[1]
            for leftV, rightV in zip(leftAsymV, rightAsymV):
                leftPos = cmds.xform(leftV, q=True, ws=False, t=True)
                rightPos = cmds.xform(rightV, q=True, ws=False, t=True)      
                leftPos[self._index] = leftPos[self._index]*-1
                if leftPos != rightPos:
                    cmds.xform(rightV, ws=False, t=leftPos)

    def mirrorRtoL(self, value):
        """
        mirror object from right to left LOCALLY
        """
        if cmds.objExists(value):
            asymmetricalVertices = self.checkSymmetry(value)
            leftAsymV = asymmetricalVertices[0]
            rightAsymV = asymmetricalVertices[1]
            for leftV, rightV in zip(leftAsymV, rightAsymV):
                leftPos = cmds.xform(leftV, q=True, ws=False, t=True)
                rightPos = cmds.xform(rightV, q=True, ws=False, t=True)      
                rightPos[self._index] = rightPos[self._index]*-1
                if rightPos != leftPos:
                    cmds.xform(leftV, ws=False, t=rightPos)

    def flipTarget(self, value):
        """
        flip the object LOCALLY
        """
        if cmds.objExists(value):
            asymmetricalVertices = self.checkSymmetry(value)
            leftAsymV = asymmetricalVertices[0]
            rightAsymV = asymmetricalVertices[1]
            for leftV, rightV in zip(leftAsymV, rightAsymV):
                leftPos = cmds.xform(leftV, q=True, ws=False, t=True)
                rightPos = cmds.xform(rightV, q=True, ws=False, t=True)      
                rightPos[self._index] = rightPos[self._index]*-1
                if rightPos != leftPos:
                    cmds.xform(leftV, ws=False, t=rightPos)
                    leftPos[self._index] = leftPos[self._index]*-1
                    cmds.xform(rightV, ws=False, t=leftPos)

    def checkSymmetry(self, value):
        """
        """
        
        leftV = []
        rightV = []
        midV = []
        leftAsymVtx =[]
        rightAsymVtx =[]

        if cmds.objExists(value):
            if value != self._baseObject:
                for v in self._LeftSideVtx:
                    leftV.append(v.replace(self._baseObject, value))
                for v in self._RightSideVtx:
                    rightV.append(v.replace(self._baseObject, value))
                for v in self._MiddleVtx:
                    rightV.append(v.replace(self._baseObject, value))
            else:
                leftV = self._LeftSideVtx
                rightV = self._RightSideVtx
                midV = self._MiddleVtx


        for v, u in zip(leftV, rightV):
            vPos = cmds.xform(v, q=True, ws=self._space, t=True)
            uPos = cmds.xform(u, q=True, ws=self._space, t=True)    
            deltaPos = [vPos[0]-(uPos[0]*self._translationMirror[0]), vPos[1]-(uPos[1]*self._translationMirror[1]), vPos[2]-(uPos[2]*self._translationMirror[2])]
            check = 0
            for x, pos in enumerate(uPos):
                if x == self._index:
                    pos = pos*self._translationMirror[self._index]
                delta = vPos[x] - pos
                if delta < 0:
                    delta = delta*-1
                if delta <= self._tolerance:
                    check += 1
                else:
                    break
            if check != 3:  
                leftAsymVtx.append(v)
                rightAsymVtx.append(u)
                
        asymmetricalVertices = [leftAsymVtx, rightAsymVtx]
        cmds.select(leftAsymVtx+rightAsymVtx)
        return asymmetricalVertices


