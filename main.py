from world import World, Action
from qlearningAgents import TaxiAgent 
import os
from naiveAgents import *

def main():
	taxi = NaiveAgent()
	world = World(taxi, 'Naive')
	os.system('clear')
	world.run()

main()