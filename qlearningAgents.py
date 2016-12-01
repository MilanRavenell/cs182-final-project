
import world
from learningAgents import ReinforcementAgent

import random,util,math

class QLearningAgent(ReinforcementAgent):
    
    def __init__(self, **args):
        ReinforcementAgent.__init__(self, **args)
        self.qvalues = util.Counter()

    def getQValue(self, state, action):
        return self.qvalues[(state.taxiLocation, state.destination, action)]

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
        self.qvalues[(state.taxiLocation, state.destination, action)] = (1 - self.alpha) * self.getQValue(state, action) + (self.alpha) * (reward + (self.discount * self.computeValueFromQValues(nextState)))
    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class TaxiAgent(QLearningAgent):
    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.location = None #random
        self.hasPassenger = False 
        self.passenger_destination = None
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action) 
        return action
