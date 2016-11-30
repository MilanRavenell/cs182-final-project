from world import World
from qlearningAgents import TaxiAgent 

def main():
	taxi = TaxiAgent()
	world = World(taxi)
	world.run()

main()