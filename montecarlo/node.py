import math
import random
from math import log, sqrt


class Node:

    def __init__(self, state):
        self.state = state
        self.win_value = 0
        self.policy_value = None
        self.visits = [0]*2
        self.parent = None
        self.children = []
        self.expanded = False
        self.player_number = None
        self.discovery_factor = 1
        ### below code is added by us
        self.original_player = None
        ###

    def update_win_value(self, value, callingPlayer):
        ### below code is modified by us
        newValue=value
        multiplier = 1
        if self.visits[callingPlayer-1] != 0:
            sum = self.win_value * self.visits[callingPlayer-1]
            sum += (newValue * multiplier)
            newValue = sum / (self.visits[callingPlayer-1] + 1)

        self.win_value = newValue
        self.visits[callingPlayer-1] += 1
        if self.parent:
                self.parent.update_win_value(value, callingPlayer)
        ###
    def update_policy_value(self, value):
        self.policy_value = value

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def add_children(self, children):
        for child in children:
            self.add_child(child)

    def get_preferred_child(self, callingPlayer):
        best_children = []
        best_score = float('-inf')
        for child in self.children:
            score = child.get_score(callingPlayer)

            if score > best_score:
                best_score = score
                best_children = [child]
            elif score == best_score:
                best_children.append(child)
        return random.choice(best_children)

    def get_score(self, callingPlayer):
        ###Below code is modified by us
        if self.original_player is None:
                #or self.visits[callingPlayer -1] < 6:
            discovery_operand = float('inf')
            win_operand = 0
        else:
            discovery_operand = self.discovery_factor * (self.policy_value or 1) * ((sqrt(self.parent.visits[callingPlayer-1]))/(1 + self.visits[callingPlayer-1]))
            win_multiplier = 1 if self.original_player == callingPlayer else -1
            win_operand = win_multiplier * self.win_value
        self.score = win_operand + discovery_operand
        return self.score
        ###

