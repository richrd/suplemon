# -*- encoding: utf-8

"""
Basic util functions.
"""

from operator import add


def halve(n):
    """
    Divide n into two halves and return as tuple of ints.
    Remainder is added to the second element.
    """

    return (int(n/2), int(n/2) + n % 2)


def divide_evenly(n, divisor):
    # TODO: Write docstring
    results = ([n/divisor]*divisor)
    results[-1] += n % divisor
    return list(map(int, results))


def divide_by_percentages(n, percentages):
    """
    Devide n with each percentage and return as list of integers.

    Percentages should add up to 100 and the remainder is distributed evenly to the resulting items.
    """
    i = 0
    sizes = []
    percent_indices = []
    while i < len(percentages):
        if percentages[i]:
            # Only positive values are treated as percentages
            percent_indices.append(i)
            sizes.append(int(n * (percentages[i] / 100)))
        else:
            sizes.append(0)
        i += 1
    if sum(sizes) < n:
        remainder = n - sum(sizes)
        for i in range(remainder):
            sizes[percent_indices[i]] += 1
    return sizes
