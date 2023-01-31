#MenuTitle: Glyph Compatibility Reporter en
#Created by ChingRu
# -*- coding: utf-8 -*-
__doc__="""
A Glyphs.app script to check the compatibility for interpolating between two master, and print the report of problem glyphs.
"""

MacroTab.title = "Glyph Compatibility Reporter en"
Glyphs.clearLog()
font = Glyphs.font

import math
import datetime
global POSITION_TOLERATE
global ANGLE_TOLERATE
global masterNameFormer
global masterNameLatter

##### SETTINGS ####W

POSITION_TOLERATE = 100
ANGLE_TOLERATE = 45

masterNameFormer = font.masters[0].name
masterNameLatter = font.masters[1].name

# flag = 1: open problem glyphs in the newtab after running the script
flagOfOpenWindow = True

################W

class Reports():
	def __init__(self):
		self.numOfShapeNotEqual = []
		self.shapeHasSingularNode = []
		self.shapeHasTwinNodes = []
		self.wrongPosition = []
		self.wrongInitNode = []
		self.wrongTypeOfNodes = []
		self.wrongDirections = []
	def printLogs(self, flag = 0):
		print("＊The number of paths is not equal. (glyph name / former master / latter master):")
		if self.numOfShapeNotEqual:
			print(", ".join([f"{gly[0]}({gly[1]}/{gly[2]})"  for gly in self.numOfShapeNotEqual]))
		else:
			print("Not Found.")
		print("-"*20)
		print("＊Layer contains an isolated single node. It's a node, not a shape. (glyph name / master / No. Path): ")
		if self.shapeHasSingularNode:
			print(", ".join([f"{gly[0]}({gly[1]}/{gly[2]})"  for gly in self.shapeHasSingularNode]))
		else:
			print("Not Found.")
		print("-"*20)
		print("＊Layer contains a path composed of two nodes. It's a line, not a shape. (glyph name / master / No. Path): ")
		if self.shapeHasTwinNodes:
			print(", ".join([f"{gly[0]}({gly[1]})"  for gly in self.shapeHasTwinNodes]))
		else:
			print("Not Found.")
		print("-"*20)
		print("＊The position of shape between two masters is too far. The path order might be wrong. (glyph name / No. Path): ")
		if self.wrongPosition:
			print(", ".join([f"{gly[0]}({gly[1]})"  for gly in self.wrongPosition]))
		else:
			print("Not Found.")
		print("-"*20)
		print("＊The initial node of shape between two masters might be wrong. (glyph name / No. Path): ")
		if self.wrongInitNode:
			print(", ".join([f"{gly[0]}({gly[1]})"  for gly in self.wrongInitNode]))
		else:
			print("Not Found.")
		print("-"*20)
		print("＊The type of node between two masters might be wrong. (glyph name / No. Path):")
		if self.wrongTypeOfNodes:
			print(", ".join([f"{gly[0]}({gly[1]})"  for gly in self.wrongTypeOfNodes]))
		else:
			print("Not Found.")
		print("-"*20)
		print("＊The direction of shape between two masters might be wrong. (glyph name / No. Path):")
		if self.wrongDirections:
			print(", ".join([f"{gly[0]}({gly[1]})"  for gly in self.wrongDirections]))
		else:
			print("Not Found.")
		if flag == 1:
			lttr = ""
			lttr += "".join([gly[0] for gly in self.numOfShapeNotEqual]) + "\n"
			lttr += "".join([gly[0] for gly in self.shapeHasSingularNode]) + "\n"
			lttr += "".join([gly[0] for gly in self.wrongPosition])+ "\n"
			lttr += "".join([gly[0] for gly in self.wrongInitNode])+ "\n"
			lttr += "".join([gly[0] for gly in self.wrongTypeOfNodes])+ "\n"
			lttr += "".join([gly[0] for gly in self.wrongDirections])+ "\n"
			try:
				if len(lttr) > 6:
					font.newTab( lttr )
			except:
				print( lttr )
		
reports = Reports()

def get_shape_attr(thisShape): 
	nodeXs    = [thisShape.nodes[i].x    for i in range(len(thisShape.nodes))]
	nodeYs    = [thisShape.nodes[i].y    for i in range(len(thisShape.nodes))]
	nodeTypes = [thisShape.nodes[i].type for i in range(len(thisShape.nodes))]
	return nodeXs, nodeYs, nodeTypes	

def check_compatibility(layerFormer, layerLatter, name):	
	nodeTypesFormer 	= layerFormer.compareString()[:-1].split("_")
	nodeTypesLatter 	= layerLatter.compareString()[:-1].split("_")
	numberOfShapeFormer = len(layerFormer.shapes)
	numberOfShapeLatter = len(layerFormer.shapes)
	
	if numberOfShapeFormer != numberOfShapeLatter: #int compare
		reports.numOfShapeNotEqual.append( (name, numberOfShapeFormer, numberOfShapeLatter) )
		numberOfShape = numberOfShapeFormer
#		{glyph.name}: The {masterNameFormer} master has {numberOfShapeFormer} shapes, while the {masterNameLatter} master has {numberOfShapeLatter} shapes.
	else:
		numberOfShape = numberOfShapeFormer
		
	nodeXsFormer, nodeYsFormer, nodeXsLatter, nodeYsLatter, directionsFormer, directionsLatter = [], [], [] ,[], [], []
		
	for shape in layerFormer.shapes:	
		nodeXs, nodeYs, _ = get_shape_attr(shape)
		nodeXsFormer.append(nodeXs)
		nodeYsFormer.append(nodeYs)
		directionsFormer.append(shape.direction)
		
	for shape in layerLatter.shapes:
		nodeXs, nodeYs, _ = get_shape_attr(shape)	
		nodeXsLatter.append(nodeXs)
		nodeYsLatter.append(nodeYs)
		directionsLatter.append(shape.direction)
	
	# check whether the direciton of each shape is the same
	for idx, (first, second) in enumerate(zip(directionsFormer, directionsLatter)):
		if first != second:
			reports.wrongDirections.append( (name, idx+1) )
			
	# check whether there has a shape formed by single/twin node(s).
	for idx in range(numberOfShape):
		if len(nodeTypesFormer[idx]) < 3: 
			if nodeTypesFormer[idx].endswith("|"): 
				reports.shapeHasSingularNode.append( (name, masterNameFormer, idx+1) )
				# {glyph.name} No. {idx} shape in {masterNameFormer} only has one node.
			else:
				reports.shapeHasTwinNodes.append( (name, masterNameFormer, idx+1) )
				# {glyph.name} No. {idx} shape in {masterNameFormer} only has two node.
		if len(nodeTypesLatter[idx]) < 3:
			if nodeTypesFormer[idx].endswith("|"):
				reports.shapeHasSingularNode.append( (name, masterNameLatter, idx+1) )
				# {glyph.name} No. {idx} shape in {masterNameLatter} only has one node.
			else:
				reports.shapeHasTwinNodes.append( (name, masterNameLatter,  idx+1) )
#				{glyph.name} No. {idx} shape in {masterNameLatter} only has two node.

		# check the type of each node for compatibility 
		if nodeTypesFormer[idx] != nodeTypesLatter[idx]:
			reports.wrongTypeOfNodes.append( (name, idx+1) )
#			{glyph.name} No. {idx} shape has compatibility problem via two master.

	#	# check the position of shape is nearby (via centroid)
		centXFormer = sum(nodeXsFormer[idx])/len(nodeXsFormer[idx])
		centYFormer = sum(nodeYsFormer[idx])/len(nodeYsFormer[idx])
		centXLatter = sum(nodeXsLatter[idx])/len(nodeXsLatter[idx])
		centYLatter = sum(nodeYsLatter[idx])/len(nodeYsLatter[idx])
		if abs(centXFormer - centXLatter)>POSITION_TOLERATE or abs(centYFormer - centYLatter)>POSITION_TOLERATE:
			reports.wrongPosition.append( (name, idx+1) )
#			print(idx+1)
#			print(abs(centXFormer - centXLatter))
#			print(abs(centYFormer - centYLatter))
#			{glyph.name} No. {idx} shape might has compatibility problem due to the worng position.
	
	# check the direction and order of initial point
		endFormer = layerFormer.shapes[idx].nodes[-1]
		startFormer = layerFormer.shapes[idx].nodes[0]
		radFormer = math.atan2(endFormer.y-startFormer.y, endFormer.x-startFormer.x)
		angleFormer = radFormer/math.pi*180
		if angleFormer < 0:
			angleFormer += 360
		
		endLatter = layerLatter.shapes[idx].nodes[-1]
		startLatter = layerLatter.shapes[idx].nodes[0]
		radLatter = math.atan2(endLatter.y-startLatter.y, endLatter.x-startLatter.x)
		angleLatter = radLatter/math.pi*180
		if angleLatter < 0:
			angleLatter += 360
		
		if 350 > max(angleLatter, angleFormer) - min(angleLatter, angleFormer) > ANGLE_TOLERATE:
			reports.wrongInitNode.append( (name, idx+1) )
			print(f"{name}({idx+1}) {abs(angleLatter - angleFormer)}")
			#{glyph.name} No. {idx} shape should check the direction of initial point

def main():
	err = []
	for idx, layer in enumerate(Glyphs.font.selectedLayers):
		glyph = layer.parent
		uniCode = glyph.name
		try:
			glyphName = ("\\u"+uniCode[3:]).encode("utf-8").decode("unicode_escape")
		except:
			glyphName = uniCode
			
		layerFormer = (font.glyphs[uniCode].layers[masterNameFormer])
		layerLatter = (font.glyphs[uniCode].layers[masterNameLatter])
		
		if len(layerFormer.paths)>0:
			try:
				check_compatibility(layerFormer, layerLatter, glyphName)
				print(f"{idx+1}/{len(Glyphs.font.selectedLayers)} {uniCode} {glyphName}")
			except:
				print("Error!", glyphName)
				err.append(glyphName)
							
	if (err):
		print("-"*20)
		print("Error in:")
		print(err)
		print("-"*20)
	print("-"*30, "REPORTS", "-"*30 )
	reports.printLogs(flag = flagOfOpenWindow)

if __name__ == "__main__":
	font.disableUpdateInterface()
	startTime = datetime.datetime.now()
	main()
	endTime = datetime.datetime.now()
	print("-"*20)
	print("Time cost:", endTime - startTime)
	font.enableUpdateInterface()