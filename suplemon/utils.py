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


def divide(n, percentages):
    """
    Devide n with each percentage and return as list of integers.

    Percentages should add up to 100 and the remainder
    is added to the last item.
    """
    # TODO: distribute remainder between last items instead of just adding it all to the last one
    i = 0
    sizes = []
    last_index = 0  # Last index that had a percentage (where we add the remainder)
    while i < len(percentages):
        if percentages[i]:
            sizes.append(int(n * (percentages[i] / 100)))
            last_index = i
        else:
            sizes.append(0)
        i += 1
    if sum(sizes) < n:
        sizes[last_index] += n - sum(sizes)
    return sizes

