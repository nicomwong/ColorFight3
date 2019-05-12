from colorfight import Colorfight
import time
import random
from colorfight.constants import BLD_GOLD_MINE, BLD_ENERGY_WELL, BLD_FORTRESS

g = Colorfight()
g.connect(room = 'public1')

if g.register(username = 'larry_wheels' + str(random.randrange(0, 100)), password = '123'):
	
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

		if g.me == None: #execution keeps going into this
			continue
		
		#shorthands
		me = g.me
		game_map = g.game_map
		
		#constants
		#additional energy to put into attacking to bypass perimeter defense
		modifier = int(len(me.cells.values()) / 50) + 1
		per = int(len(me.cells.values()) / 25) + 1
		
		#early game constants
		early_game_energy_well_chance = 0.05
		early_game_size_upper_limit = 35
		limit = 40

		#if home dead
		homeExists = False
		for c in me.cells.values():
			if c.building.is_home:
				homeExists = True
		if not homeExists:
			homePos = me.cells.values()[len(me.cells.values()) / 2].position
			#build home
			cmd_list.append(g.build(homePos, BLD_HOME))
			#upgrade to lvl 3 again
			cmd_list.append(g.upgrade(homePos))
			cmd_list.append(g.upgrade(homePos))	

		#save energy for home once hit turn limit and home is not level 2/3
		if g.turn > limit and me.tech_level < 2:
			#upgrade home
			for c in me.cells.values():
				if c.building.can_upgrade \
						and c.building.is_home \
						and c.building.upgrade_gold < me.gold \
						and c.building.upgrade_energy < me.energy:
					cmd_list.append(g.upgrade(c.position))
					print("Upgraded HOME ({}, {})".format(c.position.x, c.position.y))
					me.gold -= c.building.upgrade_gold
					me.energy -= c.building.upgrade_energy

		#START OF ENERGY ACTIONS
		else:
			#update adj list and perim list
			for c in me.cells.values():
				for pos in c.position.get_surrounding_cardinals():	
					c = game_map[pos]	
					if c.owner != g.uid and c.position not in my_adj_list:
						my_adj_list.append(c.position)
					elif c.owner == g.uid:
						my_perimeter_list.append(c.position)
		
			#shuffle so that no direction is favored
			random.shuffle(my_adj_list)

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

			#if before 100 turns
			#move empty adj to front
			#ERRONEOUS
			if g.turn < 100:
				for i in range(0, len(my_adj_list) - 2):
					#next cell in list
					tmp = game_map[my_adj_list[i + 1]]
					#this cell in list
					this = game_map[my_adj_list[i]]
					
					#if this is not empty but next is empty, switch
					if tmp.is_empty and not this.is_empty:
						my_adj_list[i + 1] = my_adj_list[i]
						my_adj_list[i] = tmp.position
		
			#once at 40 size, focus adjacent enemy home
			if(len(me.cells.values()) > 40):
				for pos in my_adj_list:
					c = game_map[pos]
					if c.owner != g.uid and not c.is_empty:
						tmp = my_adj_list[0]
						my_adj_list[0] = pos
						my_adj_list.append(tmp)

			#attack adj list
			for pos in my_adj_list:
				c = game_map[pos]	

				#energy to expend to attack
				attack_expend = c.attack_cost + modifier

				if attack_expend <= me.energy \
						and pos not in my_attack_list:

					print("Attacking ({}, {}) with {} energy".format(pos.x, pos.y, attack_expend))
					me.energy -= attack_expend
					my_attack_list.append(pos)	
					cmd_list.append(g.attack(pos, attack_expend))

			#attack "defend" perimeter cells
			#**Problematic: should only do this when touching enemy cells
			for pos in my_perimeter_list:
				c = game_map[pos]
				if c.position not in my_attack_list:
					my_attack_list.append(pos)	
					#attacks with modifier
					cmd_list.append(g.attack(pos, per))
					me.energy -= per
					print("Defending ({}, {}) with {} energy".format(pos.x, pos.y, per))
		#END OF ENERGY ACTIONS


		#START OF GOLD ACTIONS

		#randomly build fortifications on perimeters
		#**never executes
		if me.gold / len(me.cells.values()) > 75:
			for pos in my_perimeter_list:
				c = game_map[pos]
				if c.building.is_empty and me.gold >= 100:
					cmd_list.append(g.build(pos, [BLD_FORTRESS]))
					me.gold -= 100
		
		#upgrade mines and wells
		#either upgrades or builds throughout, never consistently both
		"""for c in me.cells.values():
			if c.building.can_upgrade \
					and c.building.upgrade_gold < me.gold:
				print("inside upgrade")
				if c.building.name == "energy_well":
					cmd_list.append(g.upgrade(c.position))
					print("Upgraded ({}, {})".format(c.position.x, c.position.y))
					me.gold -= c.building.upgrade_gold
				if len(me.cells.values()) > early_game_size_upper_limit \
						and c.building.name == "gold_mine":	
					cmd_list.append(g.upgrade(c.position))
					print("Upgraded ({}, {})".format(c.position.x, c.position.y))
					me.gold -= c.building.upgrade_gold
		"""

		#build wells/mines
		for c in me.cells.values():
			if c.owner == me.uid and c.building.is_empty and me.gold >= 100:
				building = random.choice([BLD_GOLD_MINE, BLD_ENERGY_WELL])
				#if small, focus on energy
				if len(me.cells.values()) < early_game_size_upper_limit:
					r = random.randrange(0, 100)
					if r <= early_game_energy_well_chance * 100:
						building = BLD_GOLD_MINE
					else:
						building = BLD_ENERGY_WELL
				cmd_list.append(g.build(c.position, building))
				print("Built {} on ({}, {})".format(building, c.position.x, c.position.y))
				me.gold -= 100


		result = g.send_cmd(cmd_list)
		print(result)
