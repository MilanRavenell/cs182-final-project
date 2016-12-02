import random
import copy

# Constants
WIDTH = 3
HEIGHT = 3
PRICE = 100
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

		for action in [Action.NORTH, Action.SOUTH, Action.EAST, Action.WEST]:
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
	def __init__(self, agent):
		self.agent = agent
		self.state = State(passDist=generatePassDist())

	def run(self):
		self.moveHistory = []
		self.state = State(passDist=generatePassDist())
		self.numMoves = 0
		self.favoredCount = 0
		self.dropoffCount = 0
		
		while self.dropoffCount < 10000:
			action = self.agent.getAction(self.state)
			if action == Action.DROP:
				self.dropoffCount += 1
			if self.state.taxiLocation == (2,0):
				self.favoredCount += 1
			self.numMoves += 1
			self.moveHistory.append(action)
			nextstate = self.state.generateSuccessor(action)
			self.agent.observeTransition(self.state, action, nextstate, self.state.getReward(action))
			self.state = nextstate

	def getFavoredProportion(self):
		return float(self.favoredCount) / float(self.numMoves)


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

