#MenuTitle: Suffix Renamer
#Created by ChingRu
# -*- coding: utf-8 -*-
__doc__="""
A Glyphs.app script to rename the suffixOrder of glyph name.
"""


MacroTab.title = "Suffix Renamer"
font = Glyphs.font	
Glyphs.clearLog()

########## CONFIGS ##########
suffixName = "ss"
fillDigits = 2
#############################

import datetime

for glyph in font.glyphs:
	if len(glyph.name) >= 5:
		if glyph.name[-4] == "." and glyph.name[-3:].isdigit():
			suffixOrder = 1  # max = 20
			oldGlyphName = glyph.name
			newGlyphName = glyph.name[:-4] + "."+ suffixName + str(suffixOrder).zfill(fillDigits)
			while(Glyphs.font.glyphs[newGlyphName] is not None):
				suffixOrder += 1
				newGlyphName = glyph.name[:-4] + "."+ suffixName + str(suffixOrder).zfill(fillDigits)
				
			if suffixOrder >= 20:
				print(f"Warning, the glyphs {oldGlyphName[:-4]} has more than 20 stylist sets.")
			dt = datetime.datetime.now().strftime("%H:%M:%S")
			glyph.name = newGlyphName
			print(f"{dt} | Raname glyph: [{oldGlyphName}] -> [{newGlyphName}]")

dt = datetime.datetime.now().strftime("%H:%M:%S")
print(f"{dt} | Done!")