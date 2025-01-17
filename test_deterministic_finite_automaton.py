from unittest import TestCase

from deterministic_finite_automaton import DeterministicFiniteAutomaton
from random_data import random_binary_string


def even_zeroes(s):
    list0 = [c for c in s if c == '0']
    count0 = list0.count('0')
    return count0 % 2 == 0


class Test(TestCase):
    def test_deterministic_finite_automaton(self):
        # string that has even number of zeroes
        dfa = DeterministicFiniteAutomaton({'s1', 's2'},
                                           {'0', '1'},
                                           {('s1', '0'): 's2',
                                            ('s1', '1'): 's1',
                                            ('s2', '0'): 's1',
                                            ('s2', '1'): 's2'},
                                           's1',
                                           {'s1'})

        for _ in range(25_000):
            s = random_binary_string(20)
            print(s)
            self.assertEqual(even_zeroes(s), dfa.accepts(s))
