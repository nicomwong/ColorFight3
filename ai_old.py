from colorfight import Colorfight
import time
import random
import math
from colorfight.constants import BLD_GOLD_MINE, BLD_ENERGY_WELL

g = Colorfight()
g.connect(room = 'nicoderek')

#returns position of (top-left corner) of closest affinity area
def affinityArea():
	#alterable constants
	areaLen = 5
	avgMin = 5 #desired minimum avg resource total of the cells in the area	

	suffAvgAffinity = [] 

	for X in range(0, g.width() - areaLen):
		for Y in range(0, g.height() - areaLen):
			resourceSum = 0

			#find avg affinity for area
			for x in range(X, X + areaLen - 1):
				for y in range(Y, Y + areaLen - 1):
					resourceSum += x.gold + x.energy
			avgAffinity = resourceSum / (areaLen * areaLen)

			#if suffices minimum, add to sufficient list
			if avgAffinity > avgMin:
				suffAvgAffinity.append(Position(X, Y))
		
	#find closest position out of sufficient list
	minDist = 900
	closestPos = Position(0, 0)
	for i in suffAvgAffinity:
		closest = myClosest(i.x, i.y)
		dist = abs(i.x - closest.x) + abs(i.y - closest.y)
		
		if dist < minDist:
			minDist = dist
			closestPos = i
	
	return closestPos
#end

def pathIsClear(x, y):
	myClosestCellPos = myClosest(x, y)
	
	for X in range(myClosestCellPos.x, x):
		for Y in range(myClosestCellPos.y, y):
			if
#end

if game.register(username = 'nico_ai', password = 'derekwu'):
	status = "attack(x, y)"
	while True:
		cmd_list = []
		my_attack_list = []
		g.update_turn()
		if g.me == None
			continue
		me = g.me
		game_map = g.game_map
		
		#start code
		#early game
		for cell in me.cells.values():
			#get home cell
			if (cell.is_home()):
				if (cell.is_empty()):
					cmd_list.append(g.attack(cell.position.directional_offset(Direction.North)))
					cmd_list.append(g.attack(cell.position.directional_offset(Direction.East)))
					cmd_list.append(g.attack(cell.position.directional_offset(Direction.West)))
					cmd_list.append(g.attack(cell.position.directional_offset(Direction.South)))

		if (status = "attack(x, y"):


		result = game.send_cmd(cmd_list)
					print(result)
