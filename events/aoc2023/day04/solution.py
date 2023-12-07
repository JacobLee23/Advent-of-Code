"""
Solution for Advent of Code 2023, Day 4
"""

import re


def part1(input: str) -> int:
    """
    Solution for Part 1
    """
    result = 0

    for line in input.split("\n"):
        match = re.search(r"^Card\s+\d+: (.*) \| (.*)$", line)
        a = set(map(int, match.group(1).split()))
        b = set(map(int, match.group(2).split()))

        result += (2 ** (len(a & b) - 1) if a & b else 0)

    return result


def part2(input: str) -> int:
    """
    Solution for Part 2
    """
    copies = {(x + 1): 1 for x, _ in enumerate(input.split("\n"))}

    for line in input.split("\n"):
        match = re.search(r"^Card\s+(\d+): (.*) \| (.*)$", line)
        card = int(match.group(1))
        a = set(map(int, match.group(2).split()))
        b = set(map(int, match.group(3).split()))

        for n, _ in enumerate(a & b, 1):
            copies[card + n] += copies[card]

    return sum(copies.values())
