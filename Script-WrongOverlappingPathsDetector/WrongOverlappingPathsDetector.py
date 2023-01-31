
#MenuTitle: Wrong Overlapping Paths Detector
#Created by ChingRu
# -*- coding: utf-8 -*-
__doc__="""
A Glyphs.app script to find the wrong direction of overlapping paths.
"""

MacroTab.title = "Wrong Overlapping Paths Detector"
Glyphs.clearLog()

results = []
intersectionsLayer = GSLayer()
singlePathLayer = GSLayer()

for idx, glyph in enumerate(Glyphs.font.glyphs):
	layer = glyph.layers[0]
	
	try:
		glyphName = ("\\u"+layer.parent.name[3:]).encode("utf-8").decode("unicode_escape")
	except:
		glyphName = layer.parent.name
		
	print(f"{idx}/{len(Glyphs.font.glyphs)} {glyphName}")
	
	clockwisePath = []
	for idx, path in enumerate(layer.paths):
		if path.direction == 1:
			clockwisePath.append(path)

	intersectionsLayer.shapes = clockwisePath	
	allIntersectionsCount = intersectionsLayer.intersections().count()
	
	if allIntersectionsCount > 0 and allIntersectionsCount % 2 == 0:
	# if a shape has intersection with another one, it will have even intersection.
		for candidatePath in clockwisePath:
			# avoid self open corner
			singlePathLayer.shapes = [candidatePath]
			allIntersectionsCount -= singlePathLayer.intersections().count()
			singlePathLayer.clear()
	
		if allIntersectionsCount > 0 and allIntersectionsCount % 2 == 0:
			results.append(glyphName)
	
	intersectionsLayer.clear()

print("-"*20)
print("".join(res))

del intersectionsLayer
del singlePathLayer