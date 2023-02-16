#MenuTitle: Horizontal Proportional - Analysis Widths
#Created by ChingRu
# -*- coding: utf-8 -*-
__doc__="""
A Glyphs.app script to analyze the height data of selected glyphs for creating horizontal proportional font.
"""

import pickle

widths = []

for layer in Glyphs.font.selectedLayers:
	width = layer.bounds.size.width
	widths.append(width)

print(f"Number of selected glyphs: {len(widths)}")

#Pickling
with open("./widths-data", "wb") as fp:   #Pickling
	pickle.dump(widths, fp)


