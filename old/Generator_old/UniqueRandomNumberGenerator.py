import random


class UniqueRandomNumberGenerator:
    def __init__(self, N):
        self.numbers = list(range(N))
        random.shuffle(self.numbers)

    def get_unique_random_number(self):
        if not self.numbers:
            return -1
        return self.numbers.pop()


if __name__ == '__main__':
    # Example usage:
    N = 10  # Replace with your desired N
    generator = UniqueRandomNumberGenerator(N)

    for _ in range(N):
        random_number = generator.get_unique_random_number()
        print(random_number)

    # After all N numbers are returned, it will return -1
    print(generator.get_unique_random_number())
