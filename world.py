WIDTH = 3
HEIGHT = 3

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
               PICK:  (0, 0),
               DROP:  (0, 0)}

    def directionToVector(direction):
        dx, dy =  Action.actions[action]
        return (dx, dy)


class WorldStateData:
	def __init__(self, prev = None):
		self.taxiLocation = None

		self.score = 0

		if not prev = None

class State:
	def __init__(self):
		self.taxiLocation = None
		self.has_passenger = False
		self.destination = None

	#def passanger_at_location(x,y):


class World:
	self.passenger_distribution = {}