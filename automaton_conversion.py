from deterministic_finite_automaton import DeterministicFiniteAutomaton
from non_deterministic_finite_automaton import NonDeterministicFiniteAutomaton


# Since every DFA is an NFA by definition, we simply copy the DFA structure to an NFA
# Change the single state to set of state (in the transitions and start date)
def dfa_to_nfa(dfa):
    nfa_transitions = {k: {v} for k, v in dfa.transitions.items()}
    nfa = NonDeterministicFiniteAutomaton(dfa.states, dfa.alphabet, nfa_transitions, {dfa.start_state},
                                          dfa.accept_states)
    return nfa


if __name__ == '__main__':
    dfa = DeterministicFiniteAutomaton({'s1', 's2'},
                                       {'0', '1'},
                                       {('s1', '0'): 's2',
                                        ('s1', '1'): 's1',
                                        ('s2', '0'): 's1',
                                        ('s2', '1'): 's2'},
                                       's1',
                                       {'s1'})
    print(dfa)
    nfa = dfa_to_nfa(dfa)
    print(nfa)
