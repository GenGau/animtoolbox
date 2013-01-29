from pymel.core import *

#if the window exists, delete it and create a new one.
if uitypes.Window.exists("mirrorBlendShape"):
    deleteUI('mirrorBlendShape')
win = window('mirrorBlendShape',title="Mirror Blend Shape")

##############################
# UI SETUP
##############################

layout = autoLayout()
howToUseBtn = button(label="How to use this tool")
loadDrivenBtn = button(label="Load Driven Mesh", parent=layout)
drivenTxt = textField(ed=False)
setupMirrorBtn = button(label="Setup Mirroring")
mirrorBlendShapeBtn = button(label="Mirror Blend Shape", parent=layout)
layout.redistribute()

def howToUse(*args):
    confirmDialog(title="Create Wrap",
                message="Select the driven mesh, then click \"Load Driven Mesh\".\n"+
                        " Click the blend shape to be mirrored and click \"Setup Mirroring\".\n"+
                        " You have to make your own wrap deformer, so do so, then click \"Mirror Blend Shape\"",b="OK")


#Set the text of the driven shape textbox to the selected transform node. 
def loadDriven(*args):
    try:
        driven = ls(sl=True)[0]
    except:
        confirmDialog(title="Error",message="Select the driven mesh")
    drivenTxt.setText(driven)

def setupMirror(*args):
    try:
        blend_shape = ls(sl=True)[0]
    except:
        confirmDialog(title="Error",message="Select the blend shape to be mirrored.")
    
    driven = PyNode(drivenTxt.getText())
    
    if(driven == ""):
        confirmDialog(title="Error",message="Load the driven mesh")
        return

    new_posn = getAttr(blend_shape.t)[:]

    driven.duplicate(n="%s_scale" % driven.name())
    driven_scale = PyNode("%s_scale" % driven.name())
    setAttr(driven_scale.t,new_posn)

    driven_scale.duplicate(n="%s_wrap" % driven.name())
    driven_wrap = PyNode("%s_wrap" % driven.name())
    sx = -1 * getAttr(driven_scale.sx)
    setAttr(driven_scale.sx,sx)

    select(blend_shape)
    select(driven_scale, add=True)
    blendShape(n="mirror")

    select(cl=True)
    select(driven_wrap)
    select(driven_scale, add=True)

    
def mirrorBlendShape(*args):
    blendShape( 'mirror', edit=True, w=[(0, 1.0)] )

    driven = PyNode(drivenTxt.getText())

    driven_scale = PyNode("%s_scale" % driven.name())

    driven_wrap = PyNode("%s_wrap" % driven.name())

    select(driven_wrap)
    duplicate(n="%s_mirror" % driven.name())

    delete(driven_wrap)
    delete(driven_scale)

howToUseBtn.setCommand(howToUse)
loadDrivenBtn.setCommand(loadDriven)
setupMirrorBtn.setCommand(setupMirror)
mirrorBlendShapeBtn.setCommand(mirrorBlendShape)

win.show()
