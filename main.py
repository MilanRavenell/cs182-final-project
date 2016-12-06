from world import World, Action
from qlearningAgents import TaxiAgent 
import os
from naiveAgents import *
import os.path 

def main():
	taxi = TaxiAgent()
	world = World(taxi, 'Taxi')

	os.system('clear')
	if os.path.isfile("output.csv"):
		print "yay2"
		print taxi.in_training
		world.run()
	else:
		print "yay"
		print taxi.in_training
		world.train()
		# world.run()
	

main()