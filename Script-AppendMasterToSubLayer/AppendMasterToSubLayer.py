#MenuTitle: Append Master To SubLayer
#Created by ChingRu
# -*- coding: utf-8 -*-
__doc__="""
A Glyphs.app script to copy a layer/master to another master, making the former as a the latter's sublayer.
"""

MacroTab.title = "Append Master To SubLayer"
Glyphs.clearLog()

attach_layer_id = ATTACH_LAYER_ID
to_be_sublayer_id = TO_BE_SUBLAYER_LAYER_ID
new_sublayer_name = NEW_SUBLAYER_NAME

import copy

for idx, layer in enumerate(Glyphs.font.selectedLayers):
	glyph = layer.parent
	print(glyph)
	
	newLayer = GSLayer()
	newLayer.name = new_sublayer_name
	newLayer.associatedMasterId = attach_layer_id # attach to last master
	newLayer.width = glyph.layers[to_be_sublayer_id].width
	newLayer.shapes = copy.copy(glyph.layers[to_be_sublayer_id].shapes)
	glyph.layers.append(newLayer)
