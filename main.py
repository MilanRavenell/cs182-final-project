from world import World
from qlearningAgents import TaxiAgent 

def main():
	taxi = TaxiAgent()
	world = World(taxi)
	for i in range(10):
		world.run()
		print world.getFavoredProportion()


main()