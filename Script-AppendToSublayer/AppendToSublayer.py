#MenuTitle: Append To SubLayer
#Created by ChingRu
# -*- coding: utf-8 -*-
__doc__="""
A Glyphs.app script to copy a layer/master to another master, making the former as a the latter's sublayer.
"""

MacroTab.title = "Append To SubLayer"
Glyphs.clearLog()

attachLayerId = ATTACH_LAYER_ID
toBeSublayerId = TO_BE_SUBLAYER_LAYER_ID
newSublayerName = NEW_SUBLAYER_NAME

import copy

for idx, layer in enumerate(Glyphs.font.selectedLayers):
	glyph = layer.parent
	print(glyph)
	
	newLayer = GSLayer()
	newLayer.name = newSublayerName
	newLayer.associatedMasterId = attachLayerId # attach to last master
	newLayer.width = glyph.layers[toBeSublayerId].width
	newLayer.shapes = copy.copy(glyph.layers[toBeSublayerId].shapes)
	glyph.layers.append(newLayer)
