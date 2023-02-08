
#MenuTitle: Wrong Overlapping Paths Detector
#Created by ChingRu
# -*- coding: utf-8 -*-
__doc__="""
A Glyphs.app script to find the wrong direction of overlapping paths.
"""

MacroTab.title = "Wrong Overlapping Paths Detector"
Glyphs.clearLog()

results = []
tmpLayer = GSLayer()
intersectionsLayer = GSLayer()
singlePathLayer = GSLayer()

for idx, layer in enumerate(Glyphs.font.selectedLayers):

	try:
		if layer.parent.name.startswith("uni"):
			glyphName = ("\\u"+layer.parent.name[3:]).encode("utf-8").decode("unicode_escape")
		else: 
			glyphName = layer.parent.name
	except:
		glyphName = layer.parent.name
		
	print(f"{idx+1}/{len(Glyphs.font.selectedLayers)} {glyphName}")
	
	allIntersectionsCount = 0
	for i in range(len(layer.paths)):
		if layer.paths[i].direction == 1:
			for j in range(len(layer.paths)):
				if i == j:
					continue
				tmpLayer.shapes = [layer.paths[i], layer.paths[j]]
				allIntersectionsCount += tmpLayer.intersections().count()
				tmpLayer.clear()

				singlePathLayer.shapes = [layer.paths[i]]
				allIntersectionsCount -= singlePathLayer.intersections().count()
				singlePathLayer.shapes = [layer.paths[j]]
				allIntersectionsCount -= singlePathLayer.intersections().count()
				singlePathLayer.clear()
	
	clockwisePath = []
	for idx, path in enumerate(layer.paths):
		if path.direction == 1:
			clockwisePath.append(path)

	intersectionsLayer.shapes = clockwisePath	
	allIntersectionsCount += intersectionsLayer.intersections().count()	
	
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
print(" ".join(results))

del intersectionsLayer
del singlePathLayer
del tmpLayer