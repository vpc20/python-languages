from random import choice
from random import randrange


# def random_binary_string(strlen):
#     length = random.randint(0, strlen)
#     return ''.join(random.choice('01') for _ in range(length))

def random_binary_string(strlen):
    length = randrange(strlen)
    return ''.join(choice('01') for _ in range(length))


if __name__ == '__main__':
    print(random_binary_string(2))
