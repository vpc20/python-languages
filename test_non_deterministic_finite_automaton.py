from unittest import TestCase

from non_deterministic_finite_automaton import NonDeterministicFiniteAutomaton
from random_data import random_binary_string


class Test(TestCase):
    def test_non_deterministic_finite_automaton(self):
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
        for _ in range(10_000):
            s = random_binary_string(20)

            s1 = s + '01'
            print(s1)
            self.assertEqual(True, nfa.accepts(s1))

            s2 = s + '10'
            print(s2)
            self.assertEqual(True, nfa.accepts(s2))

            s3 = s + '00'
            print(s3)
            self.assertEqual(False, nfa.accepts(s3))

            s4 = s + '11'
            print(s4)
            self.assertEqual(False, nfa.accepts(s4))

