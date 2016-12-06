from world import World, Action
from qlearningAgents import TaxiAgent 
import os
from naiveAgents import *

def main():
	taxi = TaxiAgent()
	world = World(taxi, 'Taxi')
	os.system('clear')
	world.run()

main()