import random

# Constants
WIDTH = 3
HEIGHT = 3
PRICE = 1
COST = -1

class Action:
	NORTH = 'North'
	SOUTH = 'South'
	EAST = 'East'
	WEST = 'West'
	PICK = 'Pick'
	DROP = 'Drop'

	actions = {NORTH: (0, 1),
               SOUTH: (0, -1),
               EAST:  (1, 0),
               WEST:  (-1, 0),
               STAY:  (0,0),
               PICK:  (0, 0),
               DROP:  (0, 0)}

    actions_as_list = actions.items()

    def actionToVector(action):
        dx, dy =  Action.actions[action]
        return (dx, dy)

class Passenger:
	def __init__(self, start, dest):
		self.startLocation = start
		self.destination = dest


class WorldStateData:
	def __init__(self, prev = None):
		self.taxiLocation = None

		self.score = 0

		if not prev = None

class State:
	def __init__(self, prev=None, passDist=None):
		self.taxiLocation = None
		self.passenger = None
		self.passengerDistribution = passDist
		self.dropoffCount = 0

		if prev:
			self.taxiLocation = prev.taxiLocation
			self.passenger = prev.passenger
			self.passengerDistribution = prev.passengerDistribution
			self.dropoffCount = prev.dropoffCount

	def getLegalActions(self)
		legalList = []
		for action in Action.actions_as_list:
			dx, dy = Action.actionToVector(action)
			x , y = self.taxiLocation
			if x + dx < WIDTH and x - dx >= 0 and y + dy < HEIGHT and y - dy >= 0:
				legalList.append(action)
		return legalList

	def getSuccessorState(self, action):
		state = State(self)
		x, y = state.taxiLocation
		dx, dy = Action.actionToVector(action)
		state.taxiLocation = (x + dx, y + dy)

		if action == Action.PICK 
			state.passenger = state.passengerAtLocation(state.taxiLocation)

		if action == Action.DROP and state.passenger and state.taxiLocation == state.passenger.destination:
			state.passenger = None
			state.dropoffCount += 1

		return state

	def passangerAtLocation(self, x, y):
		rand = random.random()
		if rand < self.passengerDistribution[(x,y)]:
			passenger = Passenger((x,y), randomDestination(x,y))
			return passenger
		else:
			return None

	def getReward(self, action):
		if action == Action.DROP and state.passenger and state.taxiLocation == state.passenger.destination:
			return PRICE * manhattanDistance(state.passenger.startLocation, state.passenger.destination)
		else:
			return COST

class World:
	def __init__(self, agent):
		self.moveHistory = []
		self.state = State(passDist=generatePassDist())
		self.agent = agent

	def run(self):
		self.numMoves = 0
		while self.state.dropoffCount < 2:
			action = self.agent.getAction(self.state)
			self.moveHistory.append(action)
			nextstate = self.state.generateSuccessor(action)
			self.agent.observetransition(self.state, action, nextstate, self.state.getReward(action))
			self.state = nextstate


def generatePassDist():
	# passDist = {}
	# for x in range(WIDTH):
	# 	for y in range(HEIGHT):
	# 		passDist[(x,y)] = random.random()
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
	rand_x = random.randint(0,WIDTH)
	while rand_x == x:
		rand_x = random.randint(0,WIDTH)

	rand_y = random.randint(0,HEIGHT)
	while rand_y == y:
		rand_y = random.randint(0,HEIGHT)

	return (x,y)

def manhattanDistance( xy1, xy2 ):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )