from learningAgents import *
from world import *

class NaiveAgent(Agent):
	def getAction(self, state):
		legalActions = state.getLegalActions()
		if state.taxiPassenger:
			if state.taxiLocation == state.destination:
				return 'Drop'
			else:
				opt_action = None
				value = float("inf")
				for action in legalActions:
					distance = world.manhattanDistance(state.generateSuccessor(action).taxiLocation, state.destination)
					if distance < value:
						value = distance
						opt_action = action
				return opt_action
		else:
			return random.choice(legalActions)