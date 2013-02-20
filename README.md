Animation Toolbox
===========

Blend Shape Locator Node:

The purpose of the Blend Shape Locator Node (BSLN) is to make the creation of facial blend shapes easier for the artist. Traditionally, an artist would create a facial blend shape by duplicating the base mesh and sculpting a specific part of an expression e.g. smile_left, smile_right, etc. This method of sculpting parts of an expression makes it hard to see the whole picture. This process also makes creating mirrored blend shapes a non-trivial problem. 

The BSLN allows the artist to sculpt the whole of an expression and separate out its different parts. So from a smiling face mesh, the artist gets smile_left, smile_right, squint_left, and squint_right. This also means that an artist can mirror sculpt geometry, eliminating the need to mirror blend shapes. 

To use the node:
	1. Download blendShapeLocatorNode.py and copy it into the plug-ins directory. 
		On Mac the directory is /Users/Shared/Autodesk/maya/plug-ins
		On Windows the directory is /My Documents/maya/plug-ins
	2. In Maya, open Window > Settings/Preferences > Plug-in Manager
	3. Click refresh and open the dropdown with path to the plug-ins; blendShapeLocatorNode.py should be in there.
	4. Check the "Loaded" and "Auto load" buttons next to blendShapeLocatorNode.py
	//TODO encapsulate createBlendShapeLocatorNode.py in blendShapeLocatorNode.py
	5. Download createBlendShapeLocators.py
	6. Open the script editor and source createBlendShapeLocatorNode.py. This will load the UI
	7. It would be useful to create a shelf button for it until its integrated into the blendShapeLocatorNode
	8. Shift select the expressive mesh then the driven mesh and click "Load Blend Shape AND Mesh"
	9. In the textbox at the bottom, type in the name of the new blendshape, and click "New Blend Shape Locator". The new blendshape mesh will be named <EXPRESSIVE_MESH_NAME>_<WHATEVER_YOU_TYPE_IN> and the locator will be named <WHATEVER_YOU_TYPE_IN>_loc
	10. Position the locator over the part of the expressive mesh that you want to be a blendshape, and scale to increase/decrease the falloff. 

