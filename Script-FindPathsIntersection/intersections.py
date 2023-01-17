res = []

# for idx, gly in enumerate(Glyphs.font.glyphs):
# 	layer = gly.layers["Regular"]
#   print(idx, gly)


for idx, layer in enumerate(Glyphs.font.selectedLayers[0]):
	print(idx, layer)
	if layer.intersections().count() > 1: # find intersection			
		print("Find intersection")
		try:
			glyphname = ("\\u"+layer.parent.name[3:]).encode("utf-8").decode("unicode_escape")
		except:
			glyphname = layer.parent.name
		res.append(glyphname)

print("="*20)		
print("".join(res))