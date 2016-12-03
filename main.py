from world import World, Action
from qlearningAgents import TaxiAgent 
from graphicsGridWorld import GraphicsGridworldDisplay, GridWorld

def runEpisode(agent, environment, display):
    dropoffCount = 0
    favoredCount = 0
    numMoves = 0
    moveHistory = []

    while dropoffCount < 100:

        # DISPLAY CURRENT STATE
        state = environment.state
        display(state)

        # GET ACTION (USUALLY FROM AGENT)
        action = agent.getAction(state)
        if action == None:
            raise 'Error: Agent returned None action'

        # EXECUTE ACTION
        if action == Action.DROP:
        	dropoffCount += 1
        if state.taxiLocation == (2,0):
        	favoredCount += 1
        numMoves += 1
        moveHistory.append(action)
        nextstate = state.generateSuccessor(action)
        agent.observeTransition(state, action, nextstate, state.getReward(action))
        environment.state = nextstate

def main():
	taxi = TaxiAgent()
	world = World(taxi)
	for i in range(10):
		world.run()
		#print world.getFavoredProportion()
		#policies = taxi.findPolicies()
		# for i in policies.keys():
		# 	a, b , c = i
		# 	if a == (1,0):
		# 		print str(i) + ": " + str(policies[i])
		# print('')
		for i in taxi.qvalues.keys():
				a, b = i
				if a[0] == (1,1) and a[1] == (2,2):
					print str(i) + ": " + str(taxi.qvalues[i])
		print "cruise time: " + str(float(world.cruiseTime) / float(world.numMoves))
		print('')
	
#def print_policy_grid(policies, location)

main()