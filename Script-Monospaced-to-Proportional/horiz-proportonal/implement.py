#MenuTitle: Horizontal Proportional - Implement Widths
#Created by ChingRu
# -*- coding: utf-8 -*-
__doc__="""
After analyze, implement the new width data of selected glyphs for creating horizontal proportional font.
"""


import math
import pickle

# PARAMETERS #
EXP_DECAY_ALL_WIDTHS_FACTOR = 1 #smaller, less kern
EXP_DACAY_PROP_FACTOR = 0.1

BASE_KERN = 200
MIN_WIDTH = 750 # floor of width
MAX_WIDTH = 1024 # ceiling of width


# Unpickling
with open("./widths-data", "rb") as fp:   
	widths = pickle.load(fp)

uniq_widths = sorted(list(set(widths)))

err = []

for idx, layer in enumerate(Glyphs.font.selectedLayers):
	try:
		print(f"{idx}/{len(Glyphs.font.selectedLayers)} layer.parent.name")
		thisWidth = layer.bounds.size.width
		performance_rating_in_all_widths = uniq_widths.index(thisWidth)/len(uniq_widths)
#		print("Percentile-Rank", performance_rating_in_all_widths*100)
		exp_decay_all_widths = math.exp(-performance_rating_in_all_widths/EXP_DECAY_ALL_WIDTHS_FACTOR)
		
		# calculate centroid of x （Geometric mean）
		x = 0
		ct = 0
		for thisShape in layer.shapes:
			for node in thisShape.nodes:
				x += node.x
				ct += 1
				
		centroid = x/ct

		rightX = layer.bounds.origin.x + layer.bounds.size.width
		leftX = layer.bounds.origin.x

		# calculate the proportion of glyph width for the rightmost to x centroid
		distance_centroid_to_right = abs(centroid-rightX)
		propRight = distance_centroid_to_right/thisWidth # 0<propRight<1

		# calculate the proportion of glyph width for the leftmost to x centroid
		distance_centroid_to_left = abs(centroid-leftX)
		propLeft = distance_centroid_to_left/thisWidth # 0<propLeft<1
		
#		print("y = e^(-x*factor) *vkern")
		
		rsb_kern = math.exp(-propRight * EXP_DACAY_PROP_FACTOR) * BASE_KERN * exp_decay_all_widths
		lsb_kern = math.exp(-propLeft * EXP_DACAY_PROP_FACTOR) * BASE_KERN * exp_decay_all_widths
		
		# print(rsb_kern, lsb_kern, thisWidth)
		# print(rsb_kern + lsb_kern + thisWidth)
		final_adjust_width = rsb_kern + lsb_kern + thisWidth

		if final_adjust_width < MIN_WIDTH:
			fix_kern = abs(MIN_WIDTH - final_adjust_width)/2
			rsb_kern += fix_kern
			lsb_kern += fix_kern
			print("too narrow, fix")
		
		if final_adjust_width > MAX_WIDTH:
			fix_kern = abs(MAX_WIDTH - final_adjust_width)/2
			rsb_kern -= fix_kern
			lsb_kern -= fix_kern
			print("too wide, fix")

		layer.RSB = rsb_kern
		layer.LSB = lsb_kern
	except:
		err.append(layer)
		pass

if err:
    print("Error:")
    print(err)