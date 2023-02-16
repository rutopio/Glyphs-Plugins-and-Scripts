
#MenuTitle: Find Over Box 
#Created by ChingRu
# -*- coding: utf-8 -*-
__doc__="""
A Glyphs.app script to find the overbox glyphs (too wide or too tall)
"""

res = []	
for idx, layer in enumerate(Glyphs.font.selectedLayers):
    try:
		glyphname = ("\\u"+layer.parent.name[3:]).encode("utf-8").decode("unicode_escape")
	except:
		glyphname = layer.parent.name
		
	layerWidth = layer.bounds.size.width
	layerHeight = layer.bounds.size.height
	layerCoordX = layer.bounds.origin.x
	layerCoordY = layer.bounds.origin.y

	if layerCoordX < 0: # check left
		flag = 1
	elif layerCoordX + layerWidth > layer.width: # check right
		flag = 1
	elif layerCoordY < layer.descender: # heck bottom
		flag = 1
	elif layerCoordY + layerHeight > layer.ascender: # # check top
		flag = 1
	else:
		flag = 0
		
	if flag > 0:
		res.append(glyphname)
		print(f"❗️{idx}/{len(Glyphs.font.selectedLayers)} {glyphname}")
	else:
		print(f"✅{idx}/{len(Glyphs.font.selectedLayers)} {glyphname}")
		
print(" ".join(res))
	