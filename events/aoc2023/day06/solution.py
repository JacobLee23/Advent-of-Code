"""
Solution for Advent of Code 2023, Day 6
"""

import functools
import operator
import re
import typing


def part1(input: str) -> int:
    """
    Solution for Part 1
    """
    records = list(zip(*[map(int, re.findall(r"\d+", s)) for s in input.split("\n")]))
    return functools.reduce(
        operator.mul, (
            sum(t * (time - t) > distance for t in range(time + 1))
            for time, distance in records
        )
    )


def part2(input: str) -> typing.Any:
    """
    Solution for Part 2
    """
    record = tuple(int("".join(re.findall(r"\d+", s))) for s in input.split("\n"))
    
    for time in range(record[0] + 1):
        if time * (record[0] - time) > record[1]:
            return (record[0] - time) - time + 1
