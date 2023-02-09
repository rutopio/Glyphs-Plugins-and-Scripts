
targetWidth = 512

for idx, layer in enumerate(Glyphs.font.selectedLayers):
	bound = layer.bounds
	thisWidth = bound.size.width

	layer.width = targetWidth
	nowX = bound.origin.x
	shouldX = targetWidth/2 - thisWidth/2
	shiftX = shouldX - nowX
	for sh in layer.shapes:
		sh.applyTransform((1, 0, 0, 1 ,shiftX ,0))
	print(f"{idx}/{len(Glyphs.font.selectedLayers)} {layer.parent.name} {layer.width} -> {targetWidth} (Delta: {shiftX})")
