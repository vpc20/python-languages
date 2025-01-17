class NFA:
    def __init__(self, num_states, alphabet, transitions, start_state, accept_states):
        self.num_states = num_states  # Total number of states
        self.alphabet = alphabet  # Input alphabet
        self.transitions = transitions  # Transition function (dictionary)
        self.start_state = start_state  # Start state
        self.accept_states = accept_states  # Accept states

    def epsilon_closure(self, states):
        # Find the epsilon closure of a set of states
        stack = list(states)
        closure = set(states)

        while stack:
            state = stack.pop()
            if (state, '') in self.transitions:
                for next_state in self.transitions[(state, '')]:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)

        return closure

    def move(self, states, symbol):
        # Find the set of states reachable from a set of states on a given input symbol
        next_states = set()
        for state in states:
            if (state, symbol) in self.transitions:
                next_states.update(self.transitions[(state, symbol)])

        return next_states

    def accepts(self, input_string):
        # Check if the NFA accepts the input string
        current_states = self.epsilon_closure({self.start_state})

        for symbol in input_string:
            current_states = self.epsilon_closure(self.move(current_states, symbol))

        return not current_states.isdisjoint(self.accept_states)


# Example usage
num_states = 6
alphabet = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
transitions = {('a', ('0', '1')): 'a',
               ('a', ''): {'b', 'e'},
               ('b', '0'): 'c',
               ('c', '1'): 'd',
               ('e', '1'): 'f',
               ('f', '0'): 'g'}
start_state = 'a'
accept_states = {'d', 'g'}

nfa = NFA(num_states, alphabet, transitions, start_state, accept_states)

input_string = "1010"
if nfa.accepts(input_string):
    print(f"The NFA accepts the input string '{input_string}'")
else:
    print(f"The NFA does not accept the input string '{input_string}'")
