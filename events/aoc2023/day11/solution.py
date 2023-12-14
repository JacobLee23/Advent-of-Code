"""
Solution for Advent of Code 2023, Day 11
"""

import itertools


def part1(input: str) -> int:
    """
    Solution for Part 1
    """
    array = input.split("\n")
    empty_rows = [i for i, x in enumerate(array) if x.count("#") == 0]
    empty_cols = [j for j, x in enumerate(map(list, zip(*array))) if x.count("#") == 0]
    nodes = [
        (i, j) for (i, line) in enumerate(array) for (j, char) in enumerate(line) if char == "#"
    ]

    return sum(
        abs(b[0] - a[0]) + abs(b[1] - a[1]) + len(
            [i for i in empty_rows if a[0] < i < b[0] or b[0] < i < a[0]]
        ) + len(
            [j for j in empty_cols if a[1] < j < b[1] or b[1] < j < a[1]]
        ) for a, b in itertools.combinations(nodes, r=2)
    )


def part2(input: str) -> int:
    """
    Solution for Part 2
    """
    array = input.split("\n")
    empty_rows = [i for i, x in enumerate(array) if x.count("#") == 0]
    empty_cols = [j for j, x in enumerate(map(list, zip(*array))) if x.count("#") == 0]
    nodes = [
        (i, j) for (i, line) in enumerate(array) for (j, char) in enumerate(line) if char == "#"
    ]

    return sum(
        abs(b[0] - a[0]) + abs(b[1] - a[1]) + 999999 * len(
            [i for i in empty_rows if a[0] < i < b[0] or b[0] < i < a[0]]
        ) + 999999 * len(
            [j for j in empty_cols if a[1] < j < b[1] or b[1] < j < a[1]]
        ) for a, b in itertools.combinations(nodes, r=2)
    )
