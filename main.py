from world import World, Action
from qlearningAgents import TaxiAgent 
import os
from naiveAgents import *
import os.path 
import sys 

def main():
	taxi = TaxiAgent()
	os.system('clear')
	if len(sys.argv) == 1: #python main.py
		if os.path.isfile("output.csv"):
			size = 0
			for key, val in csv.reader(open("output.csv")):
				if key == 'size':
					size = int(val)
					break
			world = World(taxi, 'Taxi', size)
			world.run()
		else:
			world = World(taxi, 'Taxi')
			world.train()
			world.run()
	elif len(sys.argv) == 2: # python main.py size 
		world = World(taxi, 'Taxi', sys.argv[1])
		world.train()
		world.run()
	else:
		print "Must be of this format: python main.py SIZE"
		print "SIZE is the size of the grid"

main()

