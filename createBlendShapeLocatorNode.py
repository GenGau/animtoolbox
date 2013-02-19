from pymel.core import *
import time

#if the window exists, delete it and create a new one.
if uitypes.Window.exists("blendShapeLocators"):
    deleteUI('blendShapeLocators')
win = window('blendShapeLocators',title="Blend Shape Locators")

##############################
# UI SETUP
##############################

layout = autoLayout()
loadBothBtn = button(label="Load Blend Shape AND Mesh")
loadExpressiveBtn = button(label="Load Expressive Blend Shape", parent=layout)
expressiveTxt = textField(text="EXPRESSIVE",ed=False)
loadDrivenBtn = button(label="Load Driven Mesh", parent=layout)
drivenTxt = textField(text="DRIVEN",ed=False)
newBlendShapeLocatorBtn = button(label="New Blend Shape Locator")

newBlendShapeLocatorTxt = textField(text="")


def updateBSMTxt(*args):
    selected = blendShapeMaskList.getSelectItem()[0]
    newBlendShapeMaskTxt.setText(selected)    
    
blendShapeMaskList = textScrollList(selectCommand=updateBSMTxt)

layout.redistribute()

#Set the text of the driven shape textbox to the selected transform node. 
def loadDriven(*args):
    driven = ls(sl=True)[0]
    drivenTxt.setText(driven)

#Set the text of the expressive shape textbox to be the selected transform node.
#Also loads any previously created blend shape masks to the list by checking
# for user created attributes. Needs exception checking, possibly a prefix to
# help distinguish blend shape masks from other user defined attributes.
def loadExpressive(*args):
    expressive = ls(sl=True)[0]
    expressiveTxt.setText(expressive)
    expressiveShape = expressive.getShape()
    
    #list attributes on expressiveShape where the attributes have been defined
    # by the user.
    mappings = listAttr(expressiveShape,ud=True)
    blendShapeMaskList.removeAll()
    blendShapeMaskList.append(mappings)

#Load both driven and expressive mesh.    
def loadBoth(*args):
    selection = ls(sl=True)
    expressive = selection[0]
    
    expressiveShape = expressive.getShape()
    
    mappings = listAttr(expressiveShape,ud=True)
    blendShapeMaskList.removeAll()
    blendShapeMaskList.append(mappings)
    
    try:
        expressiveTxt.setText(selection[0])
        drivenTxt.setText(selection[1])
    except:
        warning("Select the blend shape expressives mesh THEN the driven mesh")

#Creates a new blend shape mask.
def newBlendShapeLocator(*args):
    
    node = createNode("blendShapeLocatorNode")
    currentBlendShapes = textScrollList(blendShapeMaskList,q=True,ai=True)
    name = newBlendShapeLocatorTxt.getText()
    expressiveName = expressiveTxt.getText()
    expressive = PyNode(expressiveName)
    driven = PyNode(drivenTxt.getText())
    select(expressive)
    select(driven,add=True)

    expressiveShape = expressive.getShape()
    drivenShape = driven.getShape()
   
    if len(name) <= 0:
        warning("No mask name specified")
        return
        

    locator = spaceLocator(n="%s_loc" % name)
    # print "Locator"
    # print locator
    # print "--------"

    blendshape = duplicate(driven,n=expressiveName + "_" + name,st=True)[0]

    # print "BlendShape"
    # print blendshape
    # print "--------"

    # print "expressiveShape"
    # print expressiveShape
    # print "--------"

    # print "Node"
    # print node
    # print "--------"

    connectAttr(locator.worldPosition,node.blndLoc)
    connectAttr(locator.scaleX,node.blendFalloff)
    connectAttr(drivenShape.outMesh,node.drvnMesh)
    connectAttr(drivenShape.worldMatrix,node.drvnPosn)
    connectAttr(expressiveShape.outMesh,node.exprMesh)
    connectAttr(expressiveShape.worldMatrix,node.exprPosn)
    connectAttr(blendshape.outMesh,node.blendMeshIn)
    connectAttr(blendshape.worldMatrix,node.blendPosn)
    connectAttr(node.blndMeshOut,blendshape.inMesh)
    

loadDrivenBtn.setCommand(loadDriven)
loadExpressiveBtn.setCommand(loadExpressive)
loadBothBtn.setCommand(loadBoth)
newBlendShapeLocatorBtn.setCommand(newBlendShapeLocator)
win.show()
