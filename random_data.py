import random


def random_binary_string(strlen):
    length = random.randint(0, strlen)
    return ''.join(random.choice('01') for _ in range(length))


print(random_binary_string(1))
