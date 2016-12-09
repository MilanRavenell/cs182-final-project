
from world import *
from learningAgents import ReinforcementAgent
import itertools
import copy
import numpy as np

import random,util,math

class QLearningAgent(ReinforcementAgent):
    
    def __init__(self, **args):
        ReinforcementAgent.__init__(self, **args)
        self.qvalues = util.Counter()
        self.statecount = util.Counter()
        self.policies = {}
        self.prev_policies = {}
        self.isConverged = False
        self.in_training = True
        self.convergeCount = 0

    def getQValue(self, state, action):
        the_state = (state.taxiLocation, state.destination, state.hasPassenger)
        if self.in_training:
          return self.qvalues[(the_state, action)]
        else:
          key = str((the_state, action))
          return float(self.qvalues[key])

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
        the_state = (state.taxiLocation, state.destination, state.hasPassenger)
        action = None
        if not legalActions == []:
          action = legalActions[0]
          if self.in_training:
            value = float("inf")
            for act in legalActions:
              if self.statecount[(the_state, act)] < value:
                value = self.statecount[(the_state, act)]
                if util.flipCoin(0.75):
                  action = act
              else:
                if util.flipCoin(0.25):
                  action = act
          else: 
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
        self.prev_policies = copy.deepcopy(self.policies)
        the_state = (state.taxiLocation, state.destination, state.hasPassenger)
        if self.in_training:
          key = (the_state, action)
        else:
          key = str((the_state, action))
        self.qvalues[key] = (1 - self.alpha) * self.getQValue(state, action) + (self.alpha) * (reward + (self.discount * self.computeValueFromQValues(nextState)))
        self.policies = self.findPolicies(state.ssize)
        self.statecount[(the_state, action)] += 1
        self.converges()
        
    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)

    def findPolicies(self, size):
        a = [i for i in range(size)]
        b = [i for i in range(size)]
        states = list(itertools.product(a, b))
        passenger = copy.copy(states)
        list(passenger)
        passenger.append(None)
        freePassenger = [True, False]
        policies = {}
        for state_data in itertools.product(states, passenger, freePassenger):
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
            if self.in_training:
              key = (state_data, action)
            else:
              key = str((state_data, action))
            if self.qvalues[key] > max_val:
              max_val = self.qvalues[key]
              max_action = action
          policies[state_data] = max_action
        return policies

    def converges(self):
      for key in self.policies.keys():
        if not self.prev_policies or (self.policies[key] != self.prev_policies[key]):
          self.convergeCount = 0
          return
      self.convergeCount += 1
      if self.convergeCount >= 150:
        self.isConverged = True


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
