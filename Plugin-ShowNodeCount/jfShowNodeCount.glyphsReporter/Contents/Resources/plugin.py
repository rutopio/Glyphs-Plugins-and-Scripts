# encoding: utf-8

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

from math import tan, radians

class jfShowNodeCount(ReporterPlugin):

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'jf Node Count',
			'zh': 'jf Node Count',
			})

	@objc.python_method
	def drawNodeCount( self, Layer ):
		FontMaster = Layer.associatedFontMaster()
		glyph = Layer.parent
		xHeight = FontMaster.xHeight
		angle = FontMaster.italicAngle

		# rotation point is half of x-height:
		offset = tan(radians(angle)) * xHeight/2

		layerCount = []
		customLayerName = Glyphs.font.customParameters["jf Layer for Count"]
		fontSetting = Glyphs.font.customParameters["jf Layer for Count Setting"]

		try:
			fontDisplaySize = int(fontSetting.split(";")[0].strip())
			sepDisplay = str(fontSetting.split(";")[1]).strip()
			applyCheck = fontSetting.split(";")[2].strip()
			yesEmoji = fontSetting.split(";")[3].strip()
			noEmoji = fontSetting.split(";")[4].strip()
		except:
			fontDisplaySize = 20
			sepDisplay = "/"
			applyCheck = "True"
			yesEmoji = "✅"
			noEmoji = "❌"

		# print(fontDisplaySize, sepDisplay, applyCheck, yesEmoji, noEmoji)

		if customLayerName:
			if ";" in customLayerName:
				parsedParameter = customLayerName.split(";")

		if parsedParameter:
			for name in parsedParameter:
				name = name.strip()
				nodeCount = 0
				try:
					if "::" in name: #when nested layer
						parentLayerName, childLayerName = name.split("::")
						for m in Glyphs.font.masters:
							if m.name == parentLayerName:
								associatedMasterId = m.id
						for layer in glyph.layers:
							if layer.name == childLayerName:
								if layer.associatedMasterId == associatedMasterId:
									layerID = layer.layerId
									name = layerID
				except:
					pass

				try:
					sublayer = glyph.layers[name]
					for thisPath in sublayer.paths:
						nodeCount += len(thisPath.nodes)
				except:
					pass	
				layerCount.append(str(nodeCount))
	
		y_coord = max(1000, Layer.bounds.origin.y+Layer.bounds.size.height + 50.0)
		x_coord = max(Layer.width, Layer.bounds.origin.x + Layer.bounds.size.width - 50.0)
		currentZoom = self.getScale()

		if applyCheck == "True":
			if len(set(layerCount)) == 1:
				displayString = yesEmoji+"："
			else:
				displayString = noEmoji+"："
		else:
			displayString = ""

		displayString += f" {sepDisplay} ".join(layerCount)
		
		self.drawTextAtPoint( displayString, NSPoint(x_coord,y_coord), align='right', fontSize=fontDisplaySize)

	@objc.python_method
	def background(self, layer):
		if self.getScale() >= 0.2:
			self.drawNodeCount( layer )
	
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__


