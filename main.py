from world import World
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
		print world.getFavoredProportion()
	for i in taxi.qvalues.keys():
		print str(i) + ": " + str(taxi.qvalues[i])


main()