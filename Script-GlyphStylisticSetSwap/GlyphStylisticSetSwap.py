#MenuTitle: Glyph Stylistic Set Swap
#Created by ChingRu
# -*- coding: utf-8 -*-
__doc__="""
A Glyphs.app script to swapGlyphs the glyphs between the first stylistic set (*.ss01) and the default set (*).
"""


MacroTab.title = "Glyph Stylistic Set Swap"
font = Glyphs.font	
Glyphs.clearLog()

swapGlyphs = list("PASTE_THE_GLYPHS_NAME_YOU_WANT_TO_SWAP")

swapGlyphsSet = []

for ch in swapGlyphs:
    print(ch)
    unicode_name = font.glyphs[ch].name
    swapGlyphsSet.append(unicode_name)

swapGlyphsSet = list(set(swapGlyphsSet))

for idx, glyph in enumerate(swapGlyphsSet):
    font.glyphs[glyph].name = glyph + ".tmp"
    font.glyphs[glyph+".ss01"].name = glyph
    font.glyphs[glyph+".tmp"].name = glyph + ".ss01"
    print(f"swapGlyphs ({idx}/{len(swapGlyphsSet)}): {glyph} ({swapGlyphs[idx]}) ")