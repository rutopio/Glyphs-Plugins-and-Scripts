
targetWidth = 1024

for idx, layer in enumerate(Glyphs.font.selectedLayers):
	layer.width = targetWidth	
	
	thisLayerWidth = layer.width
	if abs(thisLayerWidth - 1024) < abs(thisLayerWidth - 512):
		print(f"{idx}/{len(Glyphs.font.selectedLayers)} {layer.parent.name} {thisLayerWidth} -> 1024 ")
		layer.width = 1024
	else:
		print(f"{idx}/{len(Glyphs.font.selectedLayers)} {layer.parent.name} {thisLayerWidth} -> 512")
		layer.width = 512

