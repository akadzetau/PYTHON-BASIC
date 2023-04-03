"""
Write a parametrized test for two functions.
The functions are used to find a number by ordinal in the Fibonacci sequence.
One of them has a bug.

Fibonacci sequence: https://en.wikipedia.org/wiki/Fibonacci_number

Task:
 1. Write a test with @pytest.mark.parametrize decorator.
 2. Find the buggy function and fix it.
"""
import pytest


def fibonacci_1(n):
    if n <= 0:
        return 0
    a, b = 0, 1
    for _ in range(n-1):
        a, b = b, a + b
    return b


def fibonacci_2(n):
    fibo = [0, 1]
    for i in range(2, n+1):
        fibo.append(fibo[i-1] + fibo[i-2])
    return fibo[n]


FIBONACCI = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]


def fibonacci_expected():
    return [[i, FIBONACCI[i]] for i in range(len(FIBONACCI))]


@pytest.mark.parametrize("test_input,expected", fibonacci_expected())
def test_fibonacci_1(test_input, expected):
    assert fibonacci_1(test_input) == expected


@pytest.mark.parametrize("test_input,expected", fibonacci_expected())
def test_fibonacci_2(test_input, expected):
    assert fibonacci_2(test_input) == expected
