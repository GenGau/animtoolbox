# createNode("blendShapeLocatorNode")
# connectAttr(PyNode("locator1").worldPosition,PyNode("blendShapeLocatorNode1").blndLoc)
# connectAttr(PyNode("locator1").scaleX,PyNode("blendShapeLocatorNode1").falloff)
# connectAttr(PyNode("pCubeShape1").outMesh,PyNode("blendShapeLocatorNode1").drvnMesh)
# connectAttr(PyNode("pCubeShape1").worldMatrix,PyNode("blendShapeLocatorNode1").drvnPosn)
# connectAttr(PyNode("pCubeShape2").outMesh,PyNode("blendShapeLocatorNode1").exprMesh)
# connectAttr(PyNode("pCubeShape2").worldMatrix,PyNode("blendShapeLocatorNode1").exprPosn)
# connectAttr(PyNode("pCubeShape3").outMesh,PyNode("blendShapeLocatorNode1").blendMeshIn)
# connectAttr(PyNode("pCubeShape3").worldMatrix,PyNode("blendShapeLocatorNode1").blendPosn)
# connectAttr(PyNode("blendShapeLocatorNode1").blndMeshOut,PyNode("pCubeShape3").inMesh)

# createNode("blendShapeLocatorNode")
# connectAttr(PyNode("locator1").worldPosition,PyNode("blendShapeLocatorNode1").blndLoc)
# connectAttr(PyNode("locator1").scaleX,PyNode("blendShapeLocatorNode1").falloff)
# connectAttr(PyNode("MMM_NeutralShape").outMesh,PyNode("blendShapeLocatorNode1").drvnMesh)
# connectAttr(PyNode("smileShape").outMesh,PyNode("blendShapeLocatorNode1").exprMesh)
# connectAttr(PyNode("MMM_Neutral1Shape").outMesh,PyNode("blendShapeLocatorNode1").blendMeshIn)
# connectAttr(PyNode("blendShapeLocatorNode1").blndMeshOut,PyNode("MMM_Neutral1Shape").inMesh)

import sys
from pymel.core import *
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

kPluginNodeName = "blendShapeLocatorNode"
kPluginNodeId = OpenMaya.MTypeId(0x00000001)


class blendShapeLocatorNode(OpenMayaMPx.MPxNode):
  # drivenMesh = OpenMaya.MObject()
	# expressiveMesh = OpenMaya.MObject()
	# blendLocator = OpenMaya.MObject()
	# blendFalloff = OpenMaya.MObject()
	# blendMeshIn = OpenMaya.MObject()
	# blendMeshOut = OpenMaya.MObject()

	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)

	def compute(self, plug, data):
		if plug == blendShapeLocatorNode.blendMeshOut:

			drivenMeshHandle = data.inputValue(blendShapeLocatorNode.drivenMesh)
			drvnMesh = drivenMeshHandle.data()
			drivenPosnHandle = data.inputValue(blendShapeLocatorNode.drivenPosn)
			matrix = drivenPosnHandle.asMatrix()
			drvnPosn = [matrix(3,0),matrix(3,1),matrix(3,2)]

			expressiveMeshHandle = data.inputValue(blendShapeLocatorNode.expressiveMesh)
			exprMesh = expressiveMeshHandle.data()
			expressivePosnHandle = data.inputValue(blendShapeLocatorNode.expressivePosn)
			matrix = expressivePosnHandle.asMatrix()
			exprPosn = [matrix(3,0),matrix(3,1),matrix(3,2)]


			blendLocator = data.inputValue(blendShapeLocatorNode.blendLocator)
			blndLoc = blendLocator.asDouble3()
			blendFalloff = data.inputValue(blendShapeLocatorNode.blendFalloff)
			falloff = blendFalloff.asDouble()

			blendMeshHandle = data.inputValue(blendShapeLocatorNode.blendMeshIn)
			blndMesh = blendMeshHandle.data()
			blendPosnHandle = data.inputValue(blendShapeLocatorNode.blendPosn)
			matrix = blendPosnHandle.asMatrix()
			blndPosn = [matrix(3,0),matrix(3,1),matrix(3,2)]


			drvnVertIter = OpenMaya.MItMeshVertex(drvnMesh)
			exprVertIter = OpenMaya.MItMeshVertex(exprMesh)
			blndVertIter = OpenMaya.MItMeshVertex(blndMesh)
			if not exprVertIter.count() == blndVertIter.count():
				print "Mesh vertex counts are not equivalent" 
				return

			while not exprVertIter.isDone():
				exprVertPos_world = exprVertIter.position()

				exprVertPos_world.x = exprVertPos_world.x + exprPosn[0]
				exprVertPos_world.y = exprVertPos_world.y + exprPosn[1]
				exprVertPos_world.z = exprVertPos_world.z + exprPosn[2]

				x = (exprVertPos_world.x-blndLoc[0])**2
				y = (exprVertPos_world.y-blndLoc[1])**2
				z = (exprVertPos_world.z-blndLoc[2])**2

				dist = (x+y+z)**0.5

				index = exprVertIter.index()

				if dist < falloff:
					exprVertPos_obj = exprVertIter.position()
					blndVertIter.setPosition(exprVertPos_obj)
				else:
					drvnVertPos_obj = drvnVertIter.position()
					blndVertIter.setPosition(drvnVertPos_obj)
				drvnVertIter.next()
				exprVertIter.next()
				blndVertIter.next()

			outputHandle = data.outputValue(blendShapeLocatorNode.blendMeshOut)
			outputHandle.setMObject(blndMesh)

			data.setClean(plug)
		else:
			return OpenMaya.kUnknownParameter
 
def nodeCreator():
	return OpenMayaMPx.asMPxPtr( blendShapeLocatorNode() )
 
def nodeInitializer():
	typedAttr = OpenMaya.MFnTypedAttribute()
	numericAttr  = OpenMaya.MFnNumericAttribute()
	matrixAttr = OpenMaya.MFnMatrixAttribute()
 
	blendShapeLocatorNode.expressiveMesh = typedAttr.create("expressiveMesh", "exprMesh", OpenMaya.MFnData.kMesh)
	blendShapeLocatorNode.expressivePosn = matrixAttr.create("expressivePosn", "exprPosn")
	blendShapeLocatorNode.drivenMesh = typedAttr.create("drivenMesh", "drvnMesh", OpenMaya.MFnData.kMesh)
	blendShapeLocatorNode.drivenPosn = matrixAttr.create("drivenPosn", "drvnPosn")
	blendShapeLocatorNode.blendLocator = numericAttr.create("blendLocator", "blndLoc", OpenMaya.MFnNumericData.k3Double)
	blendShapeLocatorNode.blendFalloff = numericAttr.create("blendFalloff", "falloff", OpenMaya.MFnNumericData.kDouble)
	blendShapeLocatorNode.blendMeshIn = typedAttr.create("blendMeshIn", "blndMeshIn", OpenMaya.MFnData.kMesh)
	blendShapeLocatorNode.blendPosn = matrixAttr.create("blendPosn", "blndPosn")
	blendShapeLocatorNode.blendMeshOut = typedAttr.create("blendMeshOut", "blndMeshOut", OpenMaya.MFnData.kMesh)

	blendShapeLocatorNode.addAttribute(blendShapeLocatorNode.expressiveMesh)
	blendShapeLocatorNode.addAttribute(blendShapeLocatorNode.expressivePosn)
	blendShapeLocatorNode.addAttribute(blendShapeLocatorNode.drivenMesh)
	blendShapeLocatorNode.addAttribute(blendShapeLocatorNode.drivenPosn)
	blendShapeLocatorNode.addAttribute(blendShapeLocatorNode.blendLocator)
	blendShapeLocatorNode.addAttribute(blendShapeLocatorNode.blendFalloff)
	blendShapeLocatorNode.addAttribute(blendShapeLocatorNode.blendMeshIn)
	blendShapeLocatorNode.addAttribute(blendShapeLocatorNode.blendPosn)
	blendShapeLocatorNode.addAttribute(blendShapeLocatorNode.blendMeshOut)
 
 	blendShapeLocatorNode.attributeAffects(blendShapeLocatorNode.expressiveMesh, blendShapeLocatorNode.blendMeshOut)
 	blendShapeLocatorNode.attributeAffects(blendShapeLocatorNode.expressivePosn, blendShapeLocatorNode.blendMeshOut)
 	blendShapeLocatorNode.attributeAffects(blendShapeLocatorNode.drivenPosn, blendShapeLocatorNode.blendMeshOut)
 	blendShapeLocatorNode.attributeAffects(blendShapeLocatorNode.blendPosn, blendShapeLocatorNode.blendMeshOut)
	blendShapeLocatorNode.attributeAffects(blendShapeLocatorNode.blendLocator, blendShapeLocatorNode.blendMeshOut)
 
 
# initialize the script plug-in
def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.registerNode( kPluginNodeName, kPluginNodeId, nodeCreator, nodeInitializer)
	except:
		sys.stderr.write( "Failed to register node: %s" % kPluginNodeName )
		raise
 
# uninitialize the script plug-in
def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( kPluginNodeId )
	except:
		sys.stderr.write( "Failed to deregister node: %s" % kPluginNodeName )
		raise
