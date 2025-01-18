class NonDeterministicFiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_states, accept_states):
        self.states = states  # finite set of states
        self.alphabet = alphabet  # input alphabet
        self.transitions = transitions  # transition functions
        self.start_states = start_states  # set of start states
        self.accept_states = accept_states  # set of accept states

    def __repr__(self):
        return f'''NonDeterministic Finite Automaton Definition
   Set of finite states: {self.states}  
   Input alphabet: {self.alphabet}  
   Transition functions: {self.transitions}  
   Start states: {self.start_states}  
   Accept states: {self.accept_states}'''

    def null_transition(self, c, state):
        to_states_null = self.transitions[(state, '')] if (state, '') in self.transitions else set()
        new_current_states_null = set()
        for to_state in to_states_null:
            new_states_null = self.transitions[(to_state, c)] if (to_state, c) in self.transitions else set()
            new_current_states_null.update(new_states_null)
        return new_current_states_null

    def accepts(self, s):
        current_states = self.start_states
        for c in s:
            new_current_states = set()
            for state in current_states:
                to_states = self.transitions[(state, c)] if (state, c) in self.transitions else set()
                new_current_states.update(to_states)
                new_current_states_null = self.null_transition(c, state)
                new_current_states.update(new_current_states_null)
            current_states = new_current_states
        return bool(current_states.intersection(self.accept_states))


if __name__ == '__main__':
    #  strings that end in '10' and strings that end in '01'
    nfa = NonDeterministicFiniteAutomaton({'a', 'b', 'c', 'd', 'e', 'f', 'g'},
                                          {'0', '1'},
                                          {('a', '0'): {'a'},
                                           ('a', '1'): {'a'},
                                           ('a', ''): {'b', 'e'},
                                           ('b', '0'): {'c'},
                                           ('c', '1'): {'d'},
                                           ('e', '1'): {'f'},
                                           ('f', '0'): {'g'}},
                                          {'a'},
                                          {'d', 'g'})
    print(nfa.accepts('01'))
    print(nfa)

    #  string with penultimate symbol of 1
    # nfa = NonDeterministicFiniteAutomaton({0, 1, 2},
    #                                       {'0', '1'},
    #                                       {(0, '0'): {0},
    #                                        (0, '1'): {0, 1},
    #                                        (1, '0'): {2},
    #                                        (1, '1'): {2}},
    #                                       {0},
    #                                       {2})
    # print(nfa.accepts('1010110'))
