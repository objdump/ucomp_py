# -*- coding: utf-8 -*-  
import itertools

class FARule:
    def __init__(self, state, character, next_state):
        self.state = state
        self.character = character
        self.next_state = next_state

    def __str__(self):
        return "<FARule {1} --> {2} --> {3}>".format(str(self.state),
                self,character, str(self.next_state))

    def follow(self):
        return self.next_state

    def applies_to(self, state, character):
        return state == self.state and self.character == character

class NFARulebook:
    def __init__(self, rules):
        self.rules = rules

    def next_states(self, states, character):
        follow_states_list = [ self.follow_rules_for(state, character) for state in states ]
        follow_states = list(itertools.chain.from_iterable(follow_states_list))
        follow_state_set = set(follow_states)

        return follow_state_set


    def follow_rules_for(self, state, character):
        follow_states = [ rule.follow() for rule in self.rules_for(state, character) ]
        return follow_states


    def rules_for(self, state, character):
        applies_rules = [ rule for rule in self.rules if rule.applies_to(state, character) ] 
        return applies_rules


rulebook = NFARulebook([
    FARule(1, 'a', 1), 
    FARule(1, 'b', 1),
    FARule(1, 'b', 2),
    FARule(2, 'a', 3),
    FARule(2, 'b', 3),
    FARule(3, 'a', 4),
    FARule(3, 'b', 4)])

print("Rule book testing ...")
print(rulebook.next_states(set([1]), 'b'))
print(rulebook.next_states(set([1,2]), 'a'))
print(rulebook.next_states(set([1,3]), 'b'))


class NFA:
    def __init__(self, current_states, accept_states, rulebook):
        self.current_states = current_states
        self.accept_states = set(accept_states)
        self.rulebook = rulebook

    def is_accept(self):
        return (self.current_states & self.accept_states) != set()

    def read_char(self, char):
        self.current_states = rulebook.next_states(self.current_states, char)
        return self.current_states

    def read_string(self, string):
        for char in string:
            self.read_char(char)
        return self.current_states

print("NFA testing ...")
nfa = NFA(set([1]), [4], rulebook)
print(nfa.is_accept())
nfa.read_char('b')
print(nfa.is_accept())
nfa.read_char('a')
print(nfa.is_accept())
nfa.read_char('b')
print(nfa.is_accept())


class NFADesign:
    def __init__(self, start_states, accept_states, rulebook):
        self.start_states = start_states
        self.accept_states = accept_states
        self.rulebook = rulebook

    def to_nfa(self):
        return NFA(self.start_states, self.accept_states, self.rulebook)

    def is_accept(self, string):
        dfa = self.to_nfa()
        nfa.read_string(string)
        return nfa.is_accept()
        
print("NFADesign testing ...")
nfa_design = NFADesign(set([1]), [4], rulebook)
print(nfa_design.is_accept('bab'))
print(nfa_design.is_accept('bbbbb'))
print(nfa_design.is_accept('bbabb'))

