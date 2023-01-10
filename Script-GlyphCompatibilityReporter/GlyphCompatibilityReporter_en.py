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
global former_master_name
global latter_master_name

##### SETTINGS ####W

POSITION_TOLERATE = 100
ANGLE_TOLERATE = 45

former_master_name = font.masters[0].name
latter_master_name = font.masters[1].name

# flag = 1: open problem glyphs in the newtab after running the script
open_flag = True

################W

class Reports():
	def __init__(self):
		self.numOfShapeNotEqual = []
		self.shapeHasSingularNode = []
		self.shapeHasTwinNode = []
		self.wrongPosition = []
		self.wrongInitNode = []
		self.wrongTypeOfNode = []
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
		if self.shapeHasTwinNode:
			print(", ".join([f"{gly[0]}({gly[1]})"  for gly in self.shapeHasTwinNode]))
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
		if self.wrongTypeOfNode:
			print(", ".join([f"{gly[0]}({gly[1]})"  for gly in self.wrongTypeOfNode]))
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
			lttr += "".join([gly[0] for gly in self.wrongTypeOfNode])+ "\n"
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

def check_compatibility(layer_former, layer_latter, name):	
	nodeTypes_former 	= layer_former.compareString()[:-1].split("_")
	nodeTypes_latter 	= layer_latter.compareString()[:-1].split("_")
	numberOfshape_former = len(layer_former.shapes)
	numberOfshape_latter = len(layer_former.shapes)
	
	if numberOfshape_former != numberOfshape_latter: #int compare
		reports.numOfShapeNotEqual.append( (name, numberOfshape_former, numberOfshape_latter) )
		numberOfshape = numberOfshape_former
#		{glyph.name}: The {former_master_name} master has {numberOfshape_former} shapes, while the {latter_master_name} master has {numberOfshape_latter} shapes.
	else:
		numberOfshape = numberOfshape_former
		
	nodeXs_former, nodeYs_former, nodeXs_latter, nodeYs_latter, directions_former, directions_latter = [], [], [] ,[], [], []
		
	for shape in layer_former.shapes:	
		nodeXs, nodeYs, _ = get_shape_attr(shape)
		nodeXs_former.append(nodeXs)
		nodeYs_former.append(nodeYs)
		directions_former.append(shape.direction)
		
	for shape in layer_latter.shapes:
		nodeXs, nodeYs, _ = get_shape_attr(shape)	
		nodeXs_latter.append(nodeXs)
		nodeYs_latter.append(nodeYs)
		directions_latter.append(shape.direction)
	
	# check whether the direciton of each shape is the same
	for idx, (first, second) in enumerate(zip(directions_former, directions_latter)):
		if first != second:
			reports.wrongDirections.append( (name, idx+1) )
			
	# check whether there has a shape formed by single/twin node(s).
	for idx in range(numberOfshape):
		if len(nodeTypes_former[idx]) < 3: 
			if nodeTypes_former[idx].endswith("|"): 
				reports.shapeHasSingularNode.append( (name, former_master_name, idx+1) )
				# {glyph.name} No. {idx} shape in {former_master_name} only has one node.
			else:
				reports.shapeHasTwinNode.append( (name, former_master_name, idx+1) )
				# {glyph.name} No. {idx} shape in {former_master_name} only has two node.
		if len(nodeTypes_latter[idx]) < 3:
			if nodeTypes_former[idx].endswith("|"):
				reports.shapeHasSingularNode.append( (name, latter_master_name, idx+1) )
				# {glyph.name} No. {idx} shape in {latter_master_name} only has one node.
			else:
				reports.shapeHasTwinNode.append( (name, latter_master_name,  idx+1) )
#				{glyph.name} No. {idx} shape in {latter_master_name} only has two node.

		# check the type of each node for compatibility 
		if nodeTypes_former[idx] != nodeTypes_latter[idx]:
			reports.wrongTypeOfNode.append( (name, idx+1) )
#			{glyph.name} No. {idx} shape has compatibility problem via two master.

	#	# check the position of shape is nearby (via centroid)
		centX_former = sum(nodeXs_former[idx])/len(nodeXs_former[idx])
		centY_former = sum(nodeYs_former[idx])/len(nodeYs_former[idx])
		centX_latter = sum(nodeXs_latter[idx])/len(nodeXs_latter[idx])
		centY_latter = sum(nodeYs_latter[idx])/len(nodeYs_latter[idx])
		if abs(centX_former - centX_latter)>POSITION_TOLERATE or abs(centY_former - centY_latter)>POSITION_TOLERATE:
			reports.wrongPosition.append( (name, idx+1) )
#			print(idx+1)
#			print(abs(centX_former - centX_latter))
#			print(abs(centY_former - centY_latter))
#			{glyph.name} No. {idx} shape might has compatibility problem due to the worng position.
	
	# check the direction and order of initial point
		end_former = layer_former.shapes[idx].nodes[-1]
		start_former = layer_former.shapes[idx].nodes[0]
		rad_former = math.atan2(end_former.y-start_former.y, end_former.x-start_former.x)
		angle_former = rad_former/math.pi*180
		if angle_former < 0:
			angle_former += 360
		
		end_latter = layer_latter.shapes[idx].nodes[-1]
		start_latter = layer_latter.shapes[idx].nodes[0]
		rad_latter = math.atan2(end_latter.y-start_latter.y, end_latter.x-start_latter.x)
		angle_latter = rad_latter/math.pi*180
		if angle_latter < 0:
			angle_latter += 360
		
		if 350 > max(angle_latter, angle_former) - min(angle_latter, angle_former) > ANGLE_TOLERATE:
			reports.wrongInitNode.append( (name, idx+1) )
			print(f"{name}({idx+1}) {abs(angle_latter - angle_former)}")
			#{glyph.name} No. {idx} shape should check the direction of initial point

def main():
	err = []
	for idx, layer in enumerate(Glyphs.font.selectedLayers):
		glyph = layer.parent
		uniCode = glyph.name
		try:
			glyphname = ("\\u"+uniCode[3:]).encode("utf-8").decode("unicode_escape")
		except:
			glyphname = uniCode
			
		layer_former = (font.glyphs[uniCode].layers[former_master_name])
		layer_latter = (font.glyphs[uniCode].layers[latter_master_name])
		
		if len(layer_former.paths)>0:
			try:
				check_compatibility(layer_former, layer_latter, glyphname)
				print(f"{idx+1}/{len(Glyphs.font.selectedLayers)} {uniCode} {glyphname}")
			except:
				print("Error!", glyphname)
				err.append(glyphname)
							
	if (err):
		print("-"*20)
		print("Error in:")
		print(err)
		print("-"*20)
	print("-"*30, "REPORTS", "-"*30 )
	reports.printLogs(flag = open_flag)

if __name__ == '__main__':
	font.disableUpdateInterface()
	start_time = datetime.datetime.now()
	main()
	end_time = datetime.datetime.now()
	print("-"*20)
	print("Time cost:", end_time - start_time)
	font.enableUpdateInterface()