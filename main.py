from world import World
from qlearningAgents import TaxiAgent 
from graphicsGridWorld import GraphicsGridworldDisplay

def main():
	taxi = TaxiAgent()
	world = World(taxi)
    # for i in range(10):
	#	world.run()
	#	print world.getFavoredProportion()
	# for i in taxi.qvalues.keys():
	# 	print str(i) +': ' + str(taxi.qvalues[i])

main()