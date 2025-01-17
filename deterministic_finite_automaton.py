class DeterministicFiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states  # finite set of states
        self.alphabet = alphabet  # input alphabet
        self.transitions = transitions  # transition functions
        self.start_state = start_state  # start state
        self.accept_states = accept_states  # accept/final states

    def accepts(self, s):
        curr_state = self.start_state
        for c in s:
            curr_state = self.transitions[(curr_state, c)]

        return curr_state in self.accept_states


# string that has even number of zeroes
dfa = DeterministicFiniteAutomaton({'s1', 's2'},
                                   {'0', '1'},
                                   {('s1', '0'): 's2',
                                    ('s1', '1'): 's1',
                                    ('s2', '0'): 's1',
                                    ('s2', '1'): 's2'},
                                   's1',
                                   {'s1'})
print(dfa.accepts('1'))
print(dfa.accepts('001'))
print(dfa.accepts('010'))
print(dfa.accepts('100'))
print(dfa.accepts('0101'))
print(dfa.accepts('1010'))
print(dfa.accepts('101010'))
