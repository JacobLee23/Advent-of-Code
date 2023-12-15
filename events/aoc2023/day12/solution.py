"""
Solution for Advent of Code 2023, Day 12
"""

import itertools
import typing


def arrangements(row: str, sizes: typing.Tuple[int]) -> int:
    """
    :param row:
    :param sizes:
    :return:
    """
    count = 0
    for replacements in itertools.combinations(
        (i for i, char in enumerate(row) if char == "?"), sum(sizes) - row.count("#")
    ):
        arrangement = "".join(
            ("#" if i in replacements else ".") if char == "?" else char
            for i, char in enumerate(row)
        )
        if all(
            x == sizes[i] for i, x in enumerate(
                map(len, (x for x in arrangement.split(".") if x))
            )
        ):
            count += 1

    return count


def part1(input: str) -> int:
    """
    Solution for Part 1
    """
    rows = [
        (a, tuple(map(int, b.split(",")))) for a, b in [
            x.split() for x in input.split("\n")
        ]
    ]
    return sum(arrangements(*x) for x in rows)


def part2(input: str) -> typing.Any:
    """
    Solution for Part 2
    """
