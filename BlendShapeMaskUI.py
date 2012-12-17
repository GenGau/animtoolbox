from pymel.core import *

#if the window exists, delete it and create a new one.
if uitypes.Window.exists("blendShapeMasks"):
    deleteUI('blendShapeMasks')
win = window('blendShapeMasks',title="Blend Shape Masks")

##############################
# UI SETUP
##############################

layout = autoLayout()
loadBothBtn = button(label="Load Blend Shape AND Mesh")
loadExtremeBtn = button(label="Load Extreme Blend Shape", parent=layout)
extremeTxt = textField(text="EXTREME",ed=False)
loadDrivenBtn = button(label="Load Driven Mesh", parent=layout)
drivenTxt = textField(text="DRIVEN",ed=False)
makeBlendShapeBtn = button(label="New Blend Shape")
updateBlendShapeMasksBtn = button(label="Update Blend Shape Masks")
newBlendShapeMaskBtn = button(label="New Blend Shape Mask")
newBlendShapeMaskTxt = textField(text="")


def updateBSMTxt(*args):
    selected = blendShapeMaskList.getSelectItem()[0]
    print selected
    newBlendShapeMaskTxt.setText(selected)    
    
blendShapeMaskList = textScrollList(selectCommand=updateBSMTxt)


global blendShapeObj
layout.redistribute()

#Set the text of the driven shape textbox to the selected transform node. 
def loadDriven(*args):
    driven = ls(sl=True)[0]
    drivenTxt.setText(driven)

#Set the text of the extreme shape textbox to be the selected transform node.
#Also loads any previously created blend shape masks to the list by checking
# for user created attributes. Needs exception checking, possibly a prefix to
# help distinguish blend shape masks from other user defined attributes.
def loadExtreme(*args):
    extreme = ls(sl=True)[0]
    extremeTxt.setText(extreme)
    extremeShape = extreme.getShape()
    
    #list attributes on extremeShape where the attributes have been defined
    # by the user.
    mappings = listAttr(extremeShape,ud=True)
    blendShapeMaskList.removeAll()
    blendShapeMaskList.append(mappings)

#Load both driven and extreme mesh.    
def loadBoth(*args):
    selection = ls(sl=True)
    extreme = selection[0]
    
    extremeShape = extreme.getShape()
    
    mappings = listAttr(extremeShape,ud=True)
    blendShapeMaskList.removeAll()
    blendShapeMaskList.append(mappings)
    
    try:
        extremeTxt.setText(selection[0])
        drivenTxt.setText(selection[1])
    except:
        warning("Select the blend shape extremes mesh THEN the driven mesh")
       
#Create the initial blendshape from extreme to driven.        
def makeBlendShape(*args):
    extreme = select(extremeTxt.getText())
    driven = select(drivenTxt.getText(),add=True)
    blendShape(n="BSMask");
    
#Creates a new blend shape mask.
def newBlendShapeMask(*args):
    
    name = newBlendShapeMaskTxt.getText()
    extreme = select(extremeTxt.getText())
    driven = select(drivenTxt.getText(),add=True)
    
    
    selection = ls(sl=True)
    extreme = selection[0]
    driven = selection[1]
    extremeShape = extreme.getShape()
    drivenShape = driven.getShape()
   
    if len(name) <= 0:
        warning("No mask name specified")
        return
        
    mappings = listAttr(extremeShape,ud=True)
    
    #if the blend shape mask isn't already defined
    if not(name in mappings):
        

        drivenShapeInput = drivenShape.inputs()
        
        #Iterate through all of the driven shape's inputs
        # and look for an input with type blendShape.
        for i in range(len(drivenShapeInput)):
            input = drivenShapeInput[i]
            if input.type() == "blendShape":
                drivenShapeInput = input
                break
            elif i == (len(drivenShapeInput) - 1):
                warning("There's no blend shape on the driven mesh")
                return
        

        mappings.append(name)
        index = mappings.index(name)
        runtime.AddBlendShape(n="BSMask")
        
        drivenShapeBSNode = drivenShapeInput.inputTarget[0].inputTargetGroup
        drivenShapeWeights = drivenShapeBSNode[index].targetWeights
        
        select(extremeShape)
        addAttr(ln=name,dt="doubleArray")
        makePaintable("mesh",name)
        blendShapeAttr = extremeShape + "." + name
        setAttr(blendShapeAttr, [0.0])
         
        drivenWeights = getAttr(drivenShapeWeights)
        blendWeights = getAttr(blendShapeAttr) 
        
        lenDrivenWeights = len( drivenWeights )
        lenBlendWeights = len( blendWeights )
        lenVerts = len(driven.vtx)
        
        #Initially, blendShapeAttr isn't initialized to anything useful
        # so we create an array of 0.0 that is equal in length to the
        # number of vertices on the mesh.
        if lenVerts > lenBlendWeights:
            print "Padding"
            diff = lenVerts - lenBlendWeights
            diffArray = [0.0] * diff
            
            setAttr(blendShapeAttr,blendWeights + diffArray)
        
        for i in range(len(getAttr(blendShapeAttr))):
            setAttr(drivenShapeWeights[i],getAttr(blendShapeAttr)[i])
        
        blendShapeMaskList.append(name)
        newBlendShapeMaskTxt.setText("")

        #Set tool context to paint attributes for the newly created
        # blend shape mask.
        #if not(artAttrSkinPaintCtx('blendShapeMaskCtx').exists()):
        #    artAttrSkinPaintCtx('blendShapeMaskCtx')
        #setTool('blendShapeMaskCtx')
    else:
        warning("Blend Shape Mask already exists")
        return
        
#Transfers the weights that were painted to the 
# corresponding blend shape weights.
def updateBlendShapeMasks(*args):
    
    blendShapeMask = newBlendShapeMaskTxt.getText()
    
    select(d=True)
    extreme = select(extremeTxt.getText())
    driven = select(drivenTxt.getText(),add=True)
    selection = ls(sl=True)
    extreme = selection[0]
    driven = selection[1]
    print drivenTxt.getText()
    print driven
    
    extremeShape = extreme.getShape()
    drivenShape = driven.getShape()
    
    mappings = listAttr(extremeShape,ud=True)
    
    
    drivenShapeInput = drivenShape.inputs()
    print drivenShape.inputs()
    for i in range(len(drivenShapeInput)):
        input = drivenShapeInput[i]
        if input.type() == "blendShape":
            drivenShapeInput = input
            break
        elif i == (len(drivenShapeInput) - 1):
            warning("There's no blend shape on the driven mesh")
            return
            
    index = 0
    if blendShapeMask in mappings:
        index = mappings.index(blendShapeMask)
    else:
        warning("Blend Shape Mask doesn't exist")
        return
    
    drivenShapeBSNode = drivenShapeInput.inputTarget[0].inputTargetGroup
    drivenShapeWeights = drivenShapeBSNode[index].targetWeights
    
    mask = getAttr(extremeShape + "." + blendShapeMask)
    
    
    for i in range(len(mask)):
        setAttr(drivenShapeWeights[i],mask[i])
    


loadDrivenBtn.setCommand(loadDriven)
loadExtremeBtn.setCommand(loadExtreme)
loadBothBtn.setCommand(loadBoth)
newBlendShapeMaskBtn.setCommand(newBlendShapeMask)
makeBlendShapeBtn.setCommand(makeBlendShape)
updateBlendShapeMasksBtn.setCommand(updateBlendShapeMasks)
win.show()
