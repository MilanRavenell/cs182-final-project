
from world import *
from learningAgents import ReinforcementAgent
import itertools

import random,util,math

class QLearningAgent(ReinforcementAgent):
    
    def __init__(self, **args):
        ReinforcementAgent.__init__(self, **args)
        self.qvalues = util.Counter()
        # a = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
        # for loc in a:
        #   self.qvalues[(loc, None, True), 'Pick'] = float("inf")
        #   self.qvalues[(loc, loc, True), 'Drop'] = float("inf")
        #   self.qvalues[(loc, loc, False), 'Drop'] = float("inf")

    def getQValue(self, state, action):
        the_state = (state.taxiLocation, state.destination, state.hasPassenger)
        return self.qvalues[(the_state, action)]

    def computeValueFromQValues(self, state):
        if len(self.getLegalActions(state)) == 0:
          return 0.0

        qvalue = -float("inf")
        for action in self.getLegalActions(state):
          qvalue = max(qvalue, self.getQValue(state, action))
        return qvalue

    def computeActionFromQValues(self, state):
        if len(self.getLegalActions(state)) == 0:
          return None

        max_qvalue = -float("inf")
        opt_action = None
        for action in self.getLegalActions(state):
          qvalue = self.getQValue(state, action)
          if qvalue > max_qvalue:
            max_qvalue = qvalue
            opt_action = action
          elif qvalue == max_qvalue:
            opt_action = random.choice([action, opt_action])
        return opt_action

    def getAction(self, state):
        legalActions = self.getLegalActions(state)
        action = None
        if not legalActions == []:
          if util.flipCoin(self.epsilon): # Take random action
            action = random.choice(legalActions)
          else: # Take best action
            action = self.computeActionFromQValues(state)
        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        the_state = (state.taxiLocation, state.destination, state.hasPassenger)
        self.qvalues[(the_state, action)] = (1 - self.alpha) * self.getQValue(state, action) + (self.alpha) * (reward + (self.discount * self.computeValueFromQValues(nextState)))
    
    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)

    def findPolicies(self):
        actions_as_list = [Action.NORTH, Action.SOUTH, Action.EAST, Action.WEST, Action.STAY, Action.PICK, Action.DROP]
        states = []
        a = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
        b = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2), None]
        c = [True, False]
        policies = {}
        for state_data in itertools.product(a, b, c):
          state = State()
          if state_data[1]:
            passenger = Passenger((0,0),state_data[1])
          else:
            passenger = None

          if state_data[2]:
            freePass = Passenger((0,0),(0,0))
          else:
            freePass = None
          state.taxiLocation = state_data[0]
          state.taxiPassenger = passenger
          state.freePassenger = freePass

          max_val = -float("inf")
          max_action = None 
          for action in state.getLegalActions():
            if self.qvalues[(state_data,action)] > max_val:
              max_val = self.qvalues[(state_data,action)]
              max_action = action
          policies[state_data] = max_action
        return policies

class TaxiAgent(QLearningAgent):
    def __init__(self, epsilon=0.01,gamma=0.8,alpha=0.6, numTraining=0, **args):
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.location = None 
        self.hasPassenger = False 
        self.passenger_destination = None
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action) 
        return action
