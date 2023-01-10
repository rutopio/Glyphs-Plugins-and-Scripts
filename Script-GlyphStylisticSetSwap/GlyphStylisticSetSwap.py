#MenuTitle: Glyph Stylistic Set Swap
#Created by ChingRu
# -*- coding: utf-8 -*-
__doc__="""
A Glyphs.app script to swap the glyphs between the first stylistic set (*.ss01) and the default set (*).
"""


MacroTab.title = "Glyph Stylistic Set Swap"
font = Glyphs.font	
Glyphs.clearLog()

swap = list("PASTE_THE_GLYPHS_NAME_YOU_WANT_TO_SWAP")

swap_uni = []

for ch in swap:
    print(ch)
    unicode_name = font.glyphs[ch].name
    swap_uni.append(unicode_name)

swap_uni = list(set(swap_uni))

for idx, ch_uni in enumerate(swap_uni):
    font.glyphs[ch_uni].name = ch_uni+".tmp"
    font.glyphs[ch_uni+".ss01"].name = ch_uni
    font.glyphs[ch_uni+".tmp"].name = ch_uni+".ss01"
    print(f"swap ({idx}/{len(swap_uni)}): {ch_uni} ({swap[idx]}) ")