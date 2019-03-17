# -*- encoding: utf-8

"""
Basic util functions.
"""


def halve(n):
    """
    Divide n into two halves and return as tuple of ints.
    Remainder is added to the second element.
    """

    return (int(n/2), int(n/2) + n % 2)


def divide_evenly(n, divisor):
    """
    Devide n into equal or almost equal items and return as list of integers.

    The remainder is distributed between the first items of the returned list.
    """
    if n < divisor:
        return ([1] * n) + ([0] * (divisor - n))

    results = ([n/divisor]*divisor)
    remainder = n % divisor
    items = list(map(int, results))
    for i in range(len(items)):
        if not remainder:
            break
        items[i] += 1
        remainder -= 1
    return items


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
