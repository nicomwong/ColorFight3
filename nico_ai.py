from colorfight import Colorfight
import time
import random
from colorfight.constants import BLD_GOLD_MINE, BLD_ENERGY_WELL, BLD_FORTRESS

g = Colorfight()
g.connect(room = 'nico')

if g.register(username = 'nicoAI', password = '123', join_key = 'asdf'):
	
	while True:
		cmd_list = []
		
		#offense
		my_attack_list = []
		my_adj_list = []
		
		#defense
		my_perimeter_list = []

		#collection
		my_upgrade_list = []

		#update game
		g.update_turn()
		
		#constants
		modifier = 0 #additional energy to put into attacking to bypass perimeter defense
		if (len(me.cells.values()) > 100)):
			modifier = len(me.cells.values()) / 100

		if g.me == None: #execution keeps going into this
			continue
		
		#shorthands
		me = g.me
		game_map = g.game_map

		#update adj list
		for c in me.cells.values():
			for pos in c.position.get_surrounding_cardinals():	
				c = game_map[pos]	
				if c.owner != g.uid and c.position not in my_adj_list:
					my_adj_list.append(c.position)
		
		#order adj list descending order
		for i in range(0, len(my_adj_list) - 1):
		
			#ratios: resource / cost
			#next cell in list
			tmp = game_map[my_adj_list[i + 1]]
			nextRatio = (tmp.natural_energy + tmp.natural_gold) / tmp.attack_cost
			#this cell in list
			this = game_map[my_adj_list[i]]
			thisRatio = (this.natural_energy + this.natural_gold) / this.attack_cost
			
			#if ascending order, swap
			if thisRatio < nextRatio:
				my_adj_list[i + 1] = my_adj_list[i]
				my_adj_list[i] = tmp.position

		#attack adj list
		for pos in my_adj_list:
			c = game_map[pos]	

			#energy to expend to attack
			attack_expend = c.attack_cost + modifier

			if attack_expend <= me.energy \
					and pos not in my_attack_list:

				print("We are attacking ({}, {}) with {} energy".format(pos.x, pos.y, attack_expend))
				me.energy -= attack_expend
				my_attack_list.append(pos)	
				cmd_list.append(g.attack(pos, attack_expend))


		#if gold is bottlenecked by space, then only upgrade home and wells
		if me.gold / len(me.cells.values()) > 80:
			#upgrade home
			for c in me.cells.values():
				if c.building.can_upgrade \
						and c.building.name == "home" \
						and c.building.upgrade_gold < me.gold \
						and c.building.upgrade_energy < me.energy:
					cmd_list.append(g.upgrade(c.position))
					print("We upgraded ({}, {})".format(c.position.x, c.position.y))
					me.gold -= c.building.upgrade_gold
					me.energy -= c.building.upgrade_energy

			#upgrade wells
			for c in me.cells.values():
				if c.building.can_upgrade \
						and c.building.name == "energy_well" \
						and c.building.upgrade_gold < me.gold \
						and c.building.upgrade_energy < me.energy:
					cmd_list.append(g.upgrade(c.position))
					print("We upgraded ({}, {})".format(c.position.x, c.position.y))
					me.gold -= c.building.upgrade_gold
					me.energy -= c.building.upgrade_energy

		else:
			#upgrade wells, mines
			for c in me.cells.values():
				if c.building.can_upgrade \
						and c.building.name == "energy_well" or c.building.name == "gold_mine" \
						and c.building.level < me.tech_level \
						and c.building.upgrade_gold < me.gold \
						and c.building.upgrade_energy < me.energy:
					cmd_list.append(g.upgrade(c.position))
					print("We upgraded ({}, {})".format(c.position.x, c.position.y))
					me.gold -= c.building.upgrade_gold
					me.energy -= c.building.upgrade_energy

		#build wells/mines
		for c in me.cells.values():
			if c.owner == me.uid and c.building.is_empty and me.gold >= 100:
				building = random.choice([BLD_GOLD_MINE, BLD_ENERGY_WELL])
				cmd_list.append(g.build(c.position, building))
				print("We built {} on ({}, {})".format(building, c.position.x, c.position.y))
				me.gold -= 100

		


		result = g.send_cmd(cmd_list)
		print(result)
