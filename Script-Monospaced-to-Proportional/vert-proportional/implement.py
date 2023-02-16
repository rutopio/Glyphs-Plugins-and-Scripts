#MenuTitle: Vertical Proportional - Implement Heights
#Created by ChingRu
# -*- coding: utf-8 -*-
__doc__="""
After analyze, implement the new height data of selected glyphs for creating vertical proportional font.
"""


import math
import pickle

# PARAMETERS #
EXP_DECAY_ALL_WIDTHS_FACTOR = 1 #smaller, less kern
EXP_DACAY_PROP_FACTOR = 0.1

BASE_KERN = 200
MIN_HEIGHT = 750 # min of height
MAX_HEIGHT = 1024 # ceiling of height


# Unpickling
with open("./heights-data", "rb") as fp:   
	heights = pickle.load(fp)

uniq_heights = sorted(list(set(heights)))

err = []

for idx, layer in enumerate(Glyphs.font.selectedLayers):
	try:
		print(f"{idx}/{len(Glyphs.font.selectedLayers)} {layer.parent.name}")
		thisHeight = layer.bounds.size.height
		percentile_rank_in_all_heights = uniq_heights.index(thisHeight)/len(uniq_heights)
#		print("Percentile-Rank", percentile_rank_in_all_heights*100)
		exp_decay_all_heights = math.exp(-percentile_rank_in_all_heights/EXP_DECAY_ALL_WIDTHS_FACTOR)
		
		# calculate centroid of y （Geometric mean）
		y = 0
		ct = 0
		for thisShape in layer.shapes:
			for node in thisShape.nodes:
				y += node.y
				ct += 1
				
		centroid = y/ct

		topY = layer.bounds.origin.y + layer.bounds.size.height
		bottomY = layer.bounds.origin.y

		# calculate the proportion of glyph width for the topmost to y centroid
		distance_centroid_to_top = abs(centroid-topY)
		propTop = distance_centroid_to_top/thisHeight # 0<propTop<1

		# calculate the proportion of glyph width for the bottommost to y centroid
		distance_centroid_to_bottom = abs(centroid-bottomY)
		propBottom = distance_centroid_to_bottom/thisHeight # 0<propBottom<1

#		print("y = e^(-x*factor) *vkern")
		
		tsb_kern = math.exp(-propTop * EXP_DACAY_PROP_FACTOR) * BASE_KERN * exp_decay_all_heights
		bsb_kern = math.exp(-propBottom * EXP_DACAY_PROP_FACTOR) * BASE_KERN * exp_decay_all_heights
		
		# print(tsb_kern, bsb_kern, thisHeight)
		# print(tsb_kern + bsb_kern + thisHeight)
		final_adjust_height = tsb_kern + bsb_kern + thisHeight

		if final_adjust_height < MIN_HEIGHT:
			fix_kern = abs(MIN_HEIGHT - final_adjust_height)/2
			tsb_kern += fix_kern
			bsb_kern += fix_kern
			print("too low, fix")
		
		if final_adjust_height > MAX_HEIGHT:
			fix_kern = abs(MAX_HEIGHT - final_adjust_height)/2
			tsb_kern -= fix_kern
			bsb_kern -= fix_kern
			print("too high, fix")

		layer.TSB = tsb_kern
		layer.BSB = bsb_kern
	except:
		err.append(layer)
		pass

if err:
    print("Error:")
    print(err)