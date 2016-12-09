import random
import copy
import os
import time
import json
import csv
import sys
import matplotlib.pyplot as plt
import util
from naiveAgents import *

# Constants
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

def proportion_grid(size, action_table, passDist, isNaive, walls):
	proportion_table = passDist
	pos = [[' ',' '] for i in range(size*size*3)]
	hash_function = {}
	grid = ''

	i = 0
	for y in range(size):
		for x in range(size):
			hash_function[(x,y)] = i
			i += 1

	if  isNaive:
		for key in hash_function.keys():
			i = hash_function[key]
			pos[i][0] = float("{0:.2f}".format(proportion_table[key]))
			pos[i][1] = ' '
	else:
		for key in action_table:
			index = hash_function[key]
			pos[index][0] = float("{0:.2f}".format(proportion_table[key]))
			pos[index][1] = action_table[key]

	for i in range(size * 6 + size + 1):
		grid += "_"
		sys.stdout.write("_")
	grid += "\n"
	sys.stdout.write("\n")

	for y in range(size):
		grid += "|"
		sys.stdout.write("|")
		for x in range(size):
			grid += str(pos[hash_function[(x, size - y - 1)]])
			sys.stdout.write(str(pos[hash_function[(x, size - y - 1)]]))
			if ((x, size - y - 1),(x + 1, size - y - 1)) in walls:
				grid += ' ||'
				sys.stdout.write(' ||')
			else:
				grid += ' |'
				sys.stdout.write(' |')
		grid += "\n"
		sys.stdout.write("\n")
		for i in range(size * 6 + size + 1):
			grid += "_"
			sys.stdout.write("_")
		grid+="\n"
		sys.stdout.write("\n")
	return grid

def print_grid(size, taxiloc, destination, hasPassenger, walls):
	"""
	Print the grid of boxes.
	"""
	pos = [[' ',' ',' ',' ',' '] for i in range(size*size*3)]
	hash_function = {}

	i = 0
	for y in range(size):
		for x in range(size):
			hash_function[(x,y)] = i
			i += 1
	
	if taxiloc:
		pos[hash_function[taxiloc]][0] = 'T'
	if taxiloc and destination:
		pos[hash_function[taxiloc]][0] = 'T*'
	if destination:
		pos[hash_function[destination]][4] = 'D'
	if hasPassenger:
		pos[hash_function[taxiloc]][2] = 'P'

	for i in range(size * 6 + size + 1):
		sys.stdout.write("_")
	sys.stdout.write("\n")

	for y in range(size):
		sys.stdout.write("|")
		for x in range(size):
			sys.stdout.write("".join(pos[hash_function[(x, size - y - 1)]]))
			if ((x, size - y - 1),(x + 1, size - y - 1)) in walls:
				sys.stdout.write(' ||')
			else:
				sys.stdout.write(' |')
		sys.stdout.write("\n")
		for i in range(size * 6 + size + 1):
			sys.stdout.write("_")
		sys.stdout.write("\n")


class Passenger:
	def __init__(self, start, dest):
		self.startLocation = start
		self.destination = dest

class State:
	def __init__(self, ssize=4, prev=None, passDist=None, walls=None):
		self.ssize = ssize
		self.taxiLocation = randomLocation(self.ssize)
		self.taxiPassenger = None
		self.freePassenger = None
		self.passengerDistribution = passDist
		self.destination = None
		self.hasPassenger = False
		self.walls = walls

		if prev:
			self.taxiLocation = prev.taxiLocation
			self.taxiPassenger = prev.taxiPassenger
			self.passengerDistribution = prev.passengerDistribution
			self.freePassenger = prev.freePassenger
			self.destination = prev.destination
			self.hasPassenger = prev.hasPassenger
			self.walls = prev.walls
			self.ssize = prev.ssize

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
				if x + dx < self.ssize and x + dx >= 0 and y + dy < self.ssize and y + dy >= 0:
					if not self.walls or (self.walls and not ((x,y),(x+dx,y+dy)) in self.walls and not ((x+dx,y+dy),(x,y)) in self.walls):
						legalList.append(action)
		return legalList

	def generateSuccessor(self, action):
		state = State(prev=self)
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
			passenger = Passenger((x,y), randomDestination(x,y, self.ssize))
			return passenger
		else:
			return None

class World:
	def __init__(self, agent, agent_type, size=4, directory=''):
		self.agent = agent
		self.wsize = int(size) 
		self.state = State(ssize=self.wsize, passDist=randomPassDist(self.wsize), walls=randWalls(self.wsize))
		self.dir = directory
		self.agent_type = agent_type
		self.cruise_time_list = []
		self.proportion_grid_list = []
		self.avg_dropoff_list = []
		self.x_axis = []
		self.begin_train = 0
		self.end_train = 0
		self.score = 0
		self.score_list = []
		self.cruiseTime = 0
		self.numMoves = 0
		self.move_to_higher_location = 0
		self.num_no_passenger_moves = 0
		self.dropoffCount = 0
		self.convergeTime = 0
		self.action_table = {}
		self.f=open(self.dir + 'results.txt', 'w')

	def run(self):
		self.pick_up_count = 0
		self.total_drop_offs = 0
		self.drop_off_steps = 0
		self.move_to_higher_location_trained = 0
		self.num_no_passenger_moves_trained = 0
		self.cruise_time_trained = 0
		self.numMovesConverged = 0

		qvalues = util.Counter()
		for key, val in csv.reader(open(self.dir + "output.csv")):
			qvalues[key] = float(val)
		self.agent.qvalues = copy.deepcopy(qvalues)
		
		while True:
			if self.numMovesConverged >= 10000:
				proportion_grid(self.wsize, self.action_table, self.state.passengerDistribution, False, self.state.walls)
				print_grid(self.wsize, self.state.taxiLocation, self.state.destination, self.state.hasPassenger, self.state.walls)
				time.sleep(1.5)
				os.system('clear')

			# Save the results 
			if self.numMovesConverged == 10000:
				plt.axvline(self.convergeTime/1000, color='r', linestyle='--')
				plt.plot(self.cruise_time_list, color='b', linestyle='-')
				plt.ylabel('Average Cruise Time')
				plt.savefig(self.dir + 'cruise_time.png')
				plt.show()
				plt.close()

				plt.plot(self.proportion_grid_list, color='b', linestyle='-')
				plt.ylabel('Average Move-to-Higher Proportion')
				plt.axvline(self.convergeTime/1000, color='r', linestyle='--')
				plt.savefig(self.dir + 'Move-to-higher.png')
				plt.show()
				plt.close()

				plt.plot(self.score_list, color='b', linestyle='-')
				plt.ylabel('Score')
				plt.axvline(self.convergeTime, color='r', linestyle='--')
				plt.savefig(self.dir + 'Score.png')
				plt.show()
				plt.close()

				self.f.write("\n_______FINAL_______\n\n")
				self.f.write(proportion_grid(self.wsize, self.action_table, self.state.passengerDistribution, False, self.state.walls))
				self.f.write("time: " + str(self.end_train - self.begin_train) + "\n")
				self.f.write("convergence dropoff: "+ str(self.dropoffCount) + "\n")
				self.f.write("convergence steps: " + str(self.numMoves) + "\n")
				self.f.close()

				self.runNaive()
				return

			action = self.agent.getAction(self.state)

			self.numMovesConverged += 1
			self.numMoves += 1

			if action == Action.DROP:
				self.dropoffCount += 1

			self.metrics(action)

			nextstate = self.state.generateSuccessor(action)
			self.agent.observeTransition(self.state, action, nextstate, self.state.getReward(action))
			self.state = nextstate

			if self.numMoves % 1000 == 0:
			 	print self.dropoffCount
			 	self.f.write("\n" + proportion_grid(self.wsize, self.action_table, self.state.passengerDistribution, False, self.state.walls))


	def train(self):
		self.begin_train = time.time()

		if os.path.isfile(self.dir + "output.csv"):
			os.remove(self.dir + "output.csv") # delete output file 

		while True:
			if self.agent.isConverged:
				self.convergeTime = self.numMoves
				self.end_train = time.time()
				print self.end_train - self.begin_train

				self.f.write("\n" + proportion_grid(self.wsize, self.action_table, self.state.passengerDistribution, False, self.state.walls))
				
				if self.agent_type == 'Taxi':
					w = csv.writer(open(self.dir + "output.csv", "w"))
					w.writerow(['size', self.wsize]) # saves size to output file 
					for key, val in self.agent.qvalues.items():
						w.writerow([key, val])
					self.agent.in_training = False
					return
				
			action = self.agent.getAction(self.state)

			self.numMoves += 1

			self.metrics(action)
						
			# successor function 
			nextstate = self.state.generateSuccessor(action)
			if self.agent_type == 'Taxi':
				self.agent.observeTransition(self.state, action, nextstate, self.state.getReward(action))
			self.state = nextstate

			if self.numMoves % 1000 == 0:
				print self.numMoves

	def runNaive(self):
		numMovesNaive = 0
		agent = NaiveAgent()

		self.cruise_time_list = []
		self.proportion_grid_list = []
		self.avg_dropoff_list = []
		self.x_axis = []
		self.begin_train = 0
		self.score_list = []
		self.cruiseTime = 0
		self.move_to_higher_location = 0
		self.num_no_passenger_moves = 0
		self.numMoves = 0

		while self.numMoves < 18740:
			action = agent.getAction(self.state)
			self.metrics(action)
			nextstate = self.state.generateSuccessor(action)
			self.state = nextstate
			self.numMoves += 1
			if self.numMoves % 1000 == 0:
				print self.numMoves

		print self.cruise_time_list
		plt.axvline(8, color='r', linestyle='--')
		plt.plot(self.cruise_time_list, color='b', linestyle='-')
		plt.ylabel('Average Naive Cruise Time')
		plt.savefig(self.dir + 'naive_cruise_time.png')
		plt.show()
		plt.close()

		plt.plot(self.proportion_grid_list, color='b', linestyle='-')
		plt.ylabel('Average Naive Move-to-Higher Proportion')
		plt.axvline(8, color='r', linestyle='--')
		plt.savefig(self.dir + 'naive_move-to-higher.png')
		plt.show()
		plt.close()

		plt.plot(self.score_list, color='b', linestyle='-')
		plt.ylabel('Naive Score')
		plt.axvline(self.convergeTime, color='r', linestyle='--')
		plt.savefig(self.dir + 'naive_Score.png')
		plt.show()
		plt.close()


	def metrics(self, action):
		self.score += self.state.getReward(action)
		self.score_list.append(self.score)

		if not self.state.taxiPassenger: 
			self.cruiseTime += 1
			self.num_no_passenger_moves += 1
			if moved_to_higher(self.state.taxiLocation, action, self.state.passengerDistribution):
				self.move_to_higher_location += 1
		
		if self.numMoves % 1000 == 0:
			self.cruise_time_list.append(float(self.cruiseTime) / float(1000))
			if self.num_no_passenger_moves:
				self.proportion_grid_list.append(float(self.move_to_higher_location) / float(self.num_no_passenger_moves))
			self.x_axis.append(self.numMoves)
			self.move_to_higher_location = 0
			self.cruiseTime = 0
			self.num_no_passenger_moves = 0

		policies = self.agent.findPolicies(self.wsize)
		for i in policies.keys():
			a, b, c = i
			if b == None and c == False:
				self.action_table[a] = policies[i]

def moved_to_higher(loc, action, passDist):
	passenger_dist = passDist
	curr_val = passenger_dist[loc]
	dx, dy = actionToVector(action)	
	new_val = passenger_dist[(loc[0] + dx, loc[1] + dy)]
	if new_val >= curr_val:
		return True
	else: 
		return False 

def randomLocation(size):
	rand_x = random.randint(0,size-1)
	rand_y = random.randint(0,size-1)
	return (rand_x,rand_y)

def randomPassDist(size):
	passDist = {}
	for x in range(size):
		for y in range(size):
			passDist[(x,y)] = random.uniform(0,0.5)
	return passDist

def randomDestination(x,y,size):
	rand_x = random.randint(0,size-1)
	while rand_x == x:
		rand_x = random.randint(0,size-1)

	rand_y = random.randint(0,size-1)
	while rand_y == y:
		rand_y = random.randint(0,size-1)

	return (rand_x,rand_y)

def randWalls(size):
	numWalls = random.randint(0,0)
	possible = []
	for x in range(size):
		for y in range(size):
			if x + 1 < size:
				possible.append(((x,y),(x+1,y)))
	walls = []
	for i in range(numWalls):
		walls.append(random.choice(possible))
	return walls

def manhattanDistance( xy1, xy2 ):
	"Returns the Manhattan distance between points xy1 and xy2"
	return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )





