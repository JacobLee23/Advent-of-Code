"""
Solution for Advent of Code 2023, Day 2
"""

import functools
import operator
import re


CONTENTS = {"red": 12, "green": 13, "blue": 14}


def part1(input: str) -> int:
    """
    Solution for Part 1
    """
    result = 0

    for line in input.split("\n"):
        game, record = re.search(r"^Game (\d+): (.*)$", line).groups()

        subsets = [
            {b: int(a) for a, b in re.findall(r"(\d+) (red|blue|green)", x)}
            for x in record.split(";")
        ]
        if all(cubes.get(k, 0) <= v for k, v in CONTENTS.items() for cubes in subsets):
            result += int(game)

    return result


def part2(input: str) -> int:
    """
    Solution for Part 2
    """
    result = 0

    for line in input.split("\n"):
        _, record = re.search(r"^Game (\d+): (.*)$", line).groups()

        subsets = [
            {b: int(a) for a, b in re.findall(r"(\d+) (red|blue|green)", x)}
            for x in record.split(";")
        ]
        maxcubes = {k: max(x.get(k, 0) for x in subsets) for k in CONTENTS}
        result += functools.reduce(operator.mul, maxcubes.values())

    return result
