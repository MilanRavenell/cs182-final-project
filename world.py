import random
import copy
import os
import time
import json
import csv

# Constants
WIDTH = 3
HEIGHT = 3
PRICE = 3
COST = -1

class Action:
	NORTH = 'North'
	SOUTH = 'South'
	EAST = 'East'
	WEST = 'West'
	STAY = 'Stay'
	PICK = 'Pick'
	DROP = 'Drop'

	actions = {NORTH: (0, 1),
			   SOUTH: (0, -1),
			   EAST:  (1, 0),
			   WEST:  (-1, 0),
			   STAY:  (0,0),
			   PICK:  (0, 0),
			   DROP:  (0, 0)}


actions_as_list = [Action.NORTH, Action.SOUTH, Action.EAST, Action.WEST, Action.STAY, Action.PICK, Action.DROP]

def actionToVector(action):
	dx, dy =  Action.actions[action]
	return (dx, dy)

def proportion_grid(action_table, isNaive):
	proportion_table = generatePassDist()
	pos = [' '] * 27
	hash_function = {}
	hash_function[(0,0)] = 0
	hash_function[(1,0)] = 1
	hash_function[(2,0)] = 2
	hash_function[(0,1)] = 3
	hash_function[(1,1)] = 4
	hash_function[(2,1)] = 5
	hash_function[(0,2)] = 6
	hash_function[(1,2)] = 7
	hash_function[(2,2)] = 8

	if  isNaive:
		for key in hash_function.keys():
			i = hash_function[key]
			pos[i] = proportion_table[key]
			pos[i + 9] = ' '
	else:
		for key in action_table:
			index = hash_function[key]
			pos[index] = proportion_table[key]
			pos[index + 9] = action_table[key]

	print "_________________________"
	print "|%s %s|%s %s|%s %s|" % (pos[6], pos[15], pos[7], pos[16], pos[8], pos[17])
	print "_________________________"
	print "|%s %s|%s %s|%s %s|" % (pos[3], pos[12], pos[4], pos[13], pos[5], pos[14])
	print "_________________________"
	print "|%s %s|%s %s|%s %s|" % (pos[0], pos[9], pos[1], pos[10], pos[2], pos[11])
	print "_________________________"

def print_grid(taxiloc, destination, hasPassenger):
	"""
	Print the grid of boxes.
	"""
	pos = [' '] * 27
	hash_function = {}
	hash_function[(0,0)] = 0
	hash_function[(1,0)] = 1
	hash_function[(2,0)] = 2
	hash_function[(0,1)] = 3
	hash_function[(1,1)] = 4
	hash_function[(2,1)] = 5
	hash_function[(0,2)] = 6
	hash_function[(1,2)] = 7
	hash_function[(2,2)] = 8

	
	if taxiloc:
		pos[hash_function[taxiloc]] = 'T'
	if taxiloc and destination:
		pos[hash_function[taxiloc]] = 'T*'
	if destination:
		pos[hash_function[destination] + 18] = 'D'
	if hasPassenger:
		pos[hash_function[taxiloc] + 9] = 'P'
	

	print "___________________"
	print "|%s %s %s|%s %s %s|%s %s %s|" % (pos[6], pos[15], pos[24], pos[7], pos[16], pos[25], pos[8], pos[17], pos[26])
	print "___________________"
	print "|%s %s %s|%s %s %s|%s %s %s|" % (pos[3], pos[12], pos[21], pos[4], pos[13], pos[22], pos[5], pos[14], pos[23])
	print "___________________"
	print "|%s %s %s|%s %s %s|%s %s %s|" % (pos[0], pos[9], pos[18], pos[1], pos[10], pos[19], pos[2], pos[11], pos[20])
	print "___________________"

class Passenger:
	def __init__(self, start, dest):
		self.startLocation = start
		self.destination = dest

class State:
	def __init__(self, prev=None, passDist=None):
		self.taxiLocation = randomLocation()
		self.taxiPassenger = None
		self.freePassenger = None
		self.passengerDistribution = passDist
		self.destination = None
		self.hasPassenger = False

		if prev:
			self.taxiLocation = prev.taxiLocation
			self.taxiPassenger = prev.taxiPassenger
			self.passengerDistribution = prev.passengerDistribution
			self.freePassenger = prev.freePassenger
			self.destination = prev.destination
			self.hasPassenger = prev.hasPassenger

	def getLegalActions(self):
		legalList = []
		# if passeger is at grid location, TaxiAgent's action should be PICK UP
		if self.freePassenger and not self.taxiPassenger:
			legalList.append(Action.PICK)
			return legalList

		# if taxi is at destination location, TaxiAgent's action should be DROP OFF
		if self.taxiPassenger and self.taxiLocation == self.taxiPassenger.destination:
			legalList.append(Action.DROP)
			return legalList

		for action in [Action.NORTH, Action.SOUTH, Action.EAST, Action.WEST, Action.STAY]:
				dx, dy = actionToVector(action)
				x , y = self.taxiLocation
				if x + dx < WIDTH and x + dx >= 0 and y + dy < HEIGHT and y + dy >= 0:
					legalList.append(action)
		return legalList

	def generateSuccessor(self, action):
		state = State(self)
		x, y = state.taxiLocation
		dx, dy = actionToVector(action)
		state.taxiLocation = (x + dx, y + dy)

		# if Taxi picks up free passenger, assign freePassenger to taxiPassenger
		if action == Action.PICK:
			state.taxiPassenger = copy.deepcopy(state.freePassenger)
			state.destination = state.taxiPassenger.destination
			state.freePassenger = None
			state.hasPassenger = False

		if action == Action.DROP and state.taxiPassenger and state.taxiLocation == state.taxiPassenger.destination:
			state.destination = None
			state.taxiPassenger = None

		state.freePassenger = state.passengerAtLocation(state.taxiLocation)
		if state.freePassenger:
			state.hasPassenger = True
		else:
			state.hasPassenger = False

		return state

	def getReward(self, action):
		if action == Action.DROP and self.taxiPassenger and self.taxiLocation == self.taxiPassenger.destination:
			return PRICE * manhattanDistance(self.taxiPassenger.startLocation, self.taxiPassenger.destination)
		elif self.taxiPassenger:
			return (1 / float(manhattanDistance(self.taxiLocation, self.taxiPassenger.destination)))
		else:
			return COST

	def passengerAtLocation(self, location):
		x, y = location
		rand = random.random()
		if rand < self.passengerDistribution[(x,y)]:
			passenger = Passenger((x,y), randomDestination(x,y))
			return passenger
		else:
			return None

class World:
	def __init__(self, agent, agent_type):
		self.agent = agent
		self.state = State(passDist=generatePassDist())
		self.agent_type = agent_type

	def run(self):
		self.pick_up_count = 0
		self.total_drop_offs = 0
		self.drop_off_steps = 0
		self.move_to_higher_location = 0
		self.num_no_passenger_moves = 0
		self.numMovesAfter10000 = 0
		self.action_table = {}
		self.cruiseTime = 0

		qvalues = {}
		for key, val in csv.reader(open("output.csv")):
			qvalues[key] = val
		print self.agent.qvalues
		self.agent.qvalues = copy.deepcopy(qvalues)

		policies = self.agent.findPolicies()
		for i in policies.keys():
			a, b, c = i
			if b == None and c == False:
				self.action_table[a] = policies[i]
		
		while True:
			proportion_grid(self.action_table, False)
			print_grid(self.state.taxiLocation, self.state.destination, self.state.hasPassenger)
			time.sleep(1.5)
			os.system('clear')

			if self.numMovesAfter10000 >= 1:
				print "cruise time: " + str(float(self.cruiseTime) / float(self.numMovesAfter10000))
			if self.pick_up_count >= 1:
				print "avg_drop_off_time:" + str(float(self.total_drop_offs) / float(self.pick_up_count))
			if self.num_no_passenger_moves >= 1:
				print "propotion move to higher:" + str(float(self.move_to_higher_location) / float(self.num_no_passenger_moves))

			action = self.agent.getAction(self.state)
			
			# calculating proportion of time agent moves to a higher state when taxi doesn't have passenger 
			# = self.move_to_higher_location / self.num_no_passenger_moves 
			# also calculating proportion of time cruising i.e time spent without passenger 
			# = self.cruiseTime / self.numMoves10000
			self.numMovesAfter10000 += 1
			if not self.state.taxiPassenger: 
				self.cruiseTime += 1
				self.num_no_passenger_moves += 1
				if moved_to_higher(self.state.taxiLocation, action):
					self.move_to_higher_location += 1

				# calculating avg drop_off time 
				# = self.total_drop_offs / self.pick_up_count 
				self.drop_off_steps += 1
				if action == Action.PICK:
					self.drop_off_steps = 0
					self.pick_up_count += 1
				if action == Action.DROP:
					self.total_drop_offs += self.drop_off_steps
					self.drop_off_steps = 0

			nextstate = self.state.generateSuccessor(action)
			self.state = nextstate


	def train(self):
		self.numMoves = 0
		self.dropoffCount = 0

		while True:
			if (self.dropoffCount > 10000):
				if self.agent_type == 'Taxi':
					w = csv.writer(open("output.csv", "w"))
					for key, val in self.agent.qvalues.items():
						w.writerow([key, val])
					self.agent.in_training = False
					return
				
			action = self.agent.getAction(self.state)
			self.numMoves += 1
			
			if action == Action.DROP:
				self.dropoffCount += 1
						
			# successor function 
			nextstate = self.state.generateSuccessor(action)
			if self.agent_type == 'Taxi':
				self.agent.observeTransition(self.state, action, nextstate, self.state.getReward(action))
			self.state = nextstate

def moved_to_higher(loc, action):
	passenger_dist = generatePassDist()
	curr_val = passenger_dist[loc]
	dx, dy = actionToVector(action)	
	new_val = passenger_dist[(loc[0] + dx, loc[1] + dy)]
	if new_val >= curr_val:
		return True
	else: 
		return False 

def generatePassDist():
	passDist = {(0,0): 0.1,
				(0,1): 0.3,
				(0,2): 0.5,
				(1,0): 0.1,
				(1,1): 0.3,
				(1,2): 0.4,
				(2,0): 0.7,
				(2,1): 0.1,
				(2,2): 0.2}
	return passDist

def randomDestination(x,y):
	rand_x = random.randint(0,WIDTH-1)
	while rand_x == x:
		rand_x = random.randint(0,WIDTH-1)

	rand_y = random.randint(0,HEIGHT-1)
	while rand_y == y:
		rand_y = random.randint(0,HEIGHT-1)

	return (rand_x,rand_y)

def manhattanDistance( xy1, xy2 ):
	"Returns the Manhattan distance between points xy1 and xy2"
	return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )

def randomLocation():
	rand_x = random.randint(0,WIDTH-1)
	rand_y = random.randint(0,HEIGHT-1)
	return (rand_x,rand_y)



