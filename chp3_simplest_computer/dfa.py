# -*- coding: utf-8 -*-  

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

class DFARulebook:
    def __init__(self, rules):
        self.rules = rules

    def next_state(self, state, character):
        rule = self.rule_for(state, character)
        if rule:
            return rule.follow()
        else:
            return None 

    def rule_for(self, state, character):
        applies_rules = (rule for rule in self.rules if rule.applies_to(state, character))
        try:
            return next(applies_rules)
        except StopIteration:
            return None
        """for rule in self.rules:
            if rule.applies_to(state, character):
                return rule
        return None"""


rulebook = DFARulebook([
    FARule(1, 'a', 2), 
    FARule(1, 'b', 1),
    FARule(2, 'a', 2),
    FARule(2, 'b', 3),
    FARule(3, 'a', 3),
    FARule(3, 'b', 3)])

print("Rule book testing ...")
print(rulebook.next_state(1, 'a'))
print(rulebook.next_state(1, 'b'))
print(rulebook.next_state(2, 'b'))
print(rulebook.next_state(2, 'c'))


class DFA:
    def __init__(self, current_state, accept_states, rulebook):
        self.current_state = current_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def is_accept(self):
        return self.current_state in self.accept_states

    def read_char(self, char):
        self.current_state = rulebook.next_state(self.current_state, char)
        return self.current_state

    def read_string(self, string):
        for char in string:
            self.read_char(char)
        return self.current_state

print("DFA testing ...")
print(DFA(1, [1, 3], rulebook).is_accept())
print(DFA(1, [3], rulebook).is_accept())

class DFADesign:
    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def to_dfa(self):
        return DFA(self.start_state, self.accept_states, self.rulebook)

    def is_accept(self, string):
        dfa = self.to_dfa()
        dfa.read_string(string)
        return dfa.is_accept()
        
print("DFADesign testing ...")
dfa_design = DFADesign(1, [3], rulebook)
print(dfa_design.is_accept('a'))
print(dfa_design.is_accept('baa'))
print(dfa_design.is_accept('baba'))







        

