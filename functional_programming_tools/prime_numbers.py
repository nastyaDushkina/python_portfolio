# -*- coding: utf-8 -*-


def get_prime_numbers(n):
    prime_numbers = []
    for number in range(2, n + 1):
        for prime in prime_numbers:
            if number % prime == 0:
                break
        else:
            prime_numbers.append(number)
    return prime_numbers


def get_divisors(n):
    divisors_list = []
    for i in range(n // 2):
        if n % (i + 1) == 0:
            divisors_list.append(i + 1)
    return divisors_list


class PrimeNumbers:
    def __init__(self, n):
        self.limit = n

    def __iter__(self):
        self.number = 1
        self.prime_numbers = []
        return self

    def __next__(self):
        while self.number <= self.limit:
            self.number += 1
            for prime in self.prime_numbers:
                if self.number % prime == 0:
                    break
            else:
                self.prime_numbers.append(self.number)
                return self.number
        raise StopIteration


def prime_numbers_generator(n, filter_func=None):
    prime_numbers = []
    for number in range(2, n + 1):
        for prime in prime_numbers:
            if number % prime == 0:
                break
        else:
            prime_numbers.append(number)
            if filter_func and filter_func(number) or not filter_func:
                yield number


def lucky_number(n):
    n = str(n)
    sum_start = 0
    sum_end = 0
    for i in range(0, len(n) // 2):
        sum_start += int(n[i])
        sum_end += int(n[-1 - i])
    return sum_start == sum_end if len(n) != 1 else False


def palindrome_number(n):
    n = str(n)
    return n == n[::-1]


def full_time_number(n):
    prime_numbers = get_prime_numbers(n // 2)
    divisors = get_divisors(n)
    prime_divisors = set(prime_numbers) & set(divisors)
    for number in prime_divisors:
        if n % (number ** 2) != 0:
            return False
    return prime_divisors


for number in filter(lucky_number, prime_numbers_generator(n=100000)):
    print(number)
