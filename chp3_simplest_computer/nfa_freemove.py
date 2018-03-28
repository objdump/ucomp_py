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

    def follow_free_moves(self, states):
            more_states = self.next_states(states, None)

            if more_states.issubset(states):
                return states
            else:
                return self.follow_free_moves( states | more_states)

    def rules_for(self, state, character):
        applies_rules = [ rule for rule in self.rules if rule.applies_to(state, character) ] 
        return applies_rules


rulebook = NFARulebook([
    FARule(1, None, 2), 
    FARule(1, None, 4),
    FARule(2, 'a', 3),
    FARule(3, 'a', 2),
    FARule(4, 'a', 5),
    FARule(5, 'a', 6),
    FARule(6, 'a', 4)])

print("Rule book testing ...")
print(rulebook.next_states(set([2,4]), 'a'))
print(rulebook.next_states(set([1,2,4]), 'a'))
print(rulebook.follow_free_moves(set([1])))


class NFA:
    def __init__(self, initial_states, accept_states, rulebook):
        self.accept_states = set(accept_states)
        self.rulebook = rulebook
        self.current_states = self.update_free_moves(set(initial_states))
        print("current states: {}".format(str(self.current_states)))

    def update_free_moves(self, states):
        return self.rulebook.follow_free_moves(states)

    def is_accept(self):
        return (self.current_states & self.accept_states) != set()

    def read_char(self, char):
        current_states = self.rulebook.next_states(self.current_states, char)
        self.current_states = self.update_free_moves(current_states)
        print("current states: {}".format(str(self.current_states)))
        return self.current_states

    def read_string(self, string):
        for char in string:
            self.read_char(char)
        return self.current_states

print("NFA testing ...")
nfa = NFA([1], [2,4], rulebook)
print(nfa.is_accept())
nfa.read_char('a')
print(nfa.is_accept())
nfa.read_char('a')
print(nfa.is_accept())
nfa.read_char('a')
print(nfa.is_accept())


class NFADesign:
    def __init__(self, start_states, accept_states, rulebook):
        self.start_states = start_states
        self.accept_states = accept_states
        self.rulebook = rulebook

    def to_nfa(self):
        return NFA(self.start_states, self.accept_states, self.rulebook)

    def is_accept(self, string):
        nfa = self.to_nfa()
        nfa.read_string(string)
        return nfa.is_accept()
        
print("NFADesign testing ...")
nfa_design = NFADesign([1], [2, 4], rulebook)
print(nfa_design.is_accept('aa'))
print(nfa_design.is_accept('aaa'))
print(nfa_design.is_accept('aaaa'))
print(nfa_design.is_accept('aaaaa'))

