"""
Solution for Advent of Code 2023, Day 9
"""

import re
import typing


def succeeding(values: typing.List[int]) -> int:
    """
    :param values:
    :return:
    """
    if all(x == 0 for x in values) or len(values) == 0:
        return 0
    return values[-1] + succeeding([b - a for a, b in zip(values[:-1], values[1:])])


def preceding(values: typing.List[int]) -> int:
    """
    :param values:
    :return:
    """
    if all(x == 0 for x in values) or len(values) == 0:
        return 0
    return values[0] - preceding([b - a for a, b in zip(values[:-1], values[1:])])


def part1(input: str) -> typing.Any:
    """
    Solution for Part 1
    """
    return sum(map(succeeding, [list(map(int, x.split())) for x in input.split("\n")]))


def part2(input: str) -> typing.Any:
    """
    Solution for Part 2
    """
    return sum(map(preceding, [list(map(int, x.split())) for x in input.split("\n")]))
