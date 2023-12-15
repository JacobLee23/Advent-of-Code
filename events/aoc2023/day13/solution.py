"""
Solution for Advent of Code 2023, Day 13
"""

import typing


def mirror(array: typing.List[str]) -> typing.Optional[int]:
    """
    :param array:
    :return:
    """
    for i, _ in enumerate(array):
        before, after = array[:i], array[i:]
        if (before and after) and all(a == b for a, b in zip(after, reversed(before))):
            return i


def smudge(array: typing.List[str]) -> typing.Optional[int]:
    """
    :param array:
    :return:
    """
    for i, _ in enumerate(array):
        before, after = array[:i], array[i:]
        if (before and after) and sum(
            x != y for a, b in zip(after, reversed(before)) for x, y in zip(a, b)
        ) == 1:
            return i


def part1(input: str) -> int:
    """
    Solution for Part 1
    """
    result = 0

    for array in (x.split("\n") for x in input.split("\n\n")):
        try:
            result += 100 * mirror(array)
        except TypeError:
            result += mirror(["".join(x) for x in zip(*array)])

    return result


def part2(input: str) -> int:
    """
    Solution for Part 2
    """
    result = 0

    for array in (x.split("\n") for x in input.split("\n\n")):
        try:
            result += 100 * smudge(array)
        except TypeError:
            result += smudge(["".join(x) for x in zip(*array)])

    return result
