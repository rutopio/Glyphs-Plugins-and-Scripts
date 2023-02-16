#MenuTitle: Vertical Proportional - Analysis Heights
#Created by ChingRu
# -*- coding: utf-8 -*-
__doc__="""
A Glyphs.app script to analyze the height data of selected glyphs for creating vertical proportional font.
"""

import pickle

heights = []

for layer in Glyphs.font.selectedLayers:
	height = layer.bounds.size.height
	heights.append(height)

print(f"Number of selected glyphs: {len(heights)}")

#Pickling
with open("./heights-data", "wb") as fp:  
	pickle.dump(heights, fp)

