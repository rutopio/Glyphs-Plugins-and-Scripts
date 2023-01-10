#MenuTitle: Suffix Renamer
#Created by ChingRu
# -*- coding: utf-8 -*-
__doc__="""
A Glyphs.app script to rename the suffix of glyph name.
"""


MacroTab.title = "Suffix Renamer"
font = Glyphs.font	
Glyphs.clearLog()

########## CONFIGS ##########
suffix_name = "ss"
fill_digit = 2
#############################

import datetime

for glyph in font.glyphs:
	if len(glyph.name) >= 5:
		if glyph.name[-4] == "." and glyph.name[-3:].isdigit():
			suffix = 1  # max = 20
			old_name = glyph.name
			new_name = glyph.name[:-4] + "."+ suffix_name + str(suffix).zfill(fill_digit)
			while(Glyphs.font.glyphs[new_name] is not None):
				suffix += 1
				new_name = glyph.name[:-4] + "."+ suffix_name + str(suffix).zfill(fill_digit)
				
			if suffix >= 20:
				print(f"Warning, the glyphs {old_name[:-4]} has more than 20 stylist sets.")
			dt = datetime.datetime.now().strftime("%H:%M:%S")
			glyph.name = new_name
			print(f"{dt} | Raname glyph: [{old_name}] -> [{new_name}]")

dt = datetime.datetime.now().strftime("%H:%M:%S")
print(f"{dt} | Done!")