"""
Solution for Advent of Code 2023, Day 8
"""

import functools
import math
import re
import typing


def get_path(line: str) -> typing.List[int]:
    """
    :param line:
    :return:
    """
    return ["LR".index(x) for x in line]


def get_network(lines: typing.List[str]) -> typing.Dict[str, typing.Tuple[str, str]]:
    """
    :param lines:
    :return:
    """
    return {
        a: (b, c) for a, b, c in (
            re.search(r"([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)", x).groups()
            for x in lines
        )
    }


def part1(input: str) -> int:
    """
    Solution for Part 1
    """
    path = get_path(input.split("\n\n")[0])
    network = get_network(input.split("\n\n")[1].split("\n"))

    node, steps = "AAA", 0
    while node != "ZZZ":
        node = network[node][path[steps % len(path)]]
        steps += 1

    return steps


def part2(input: str) -> typing.Any:
    """
    Solution for Part 2
    """
    path = get_path(input.split("\n\n")[0])
    network = get_network(input.split("\n\n")[1].split("\n"))

    steps = []
    for node in filter(lambda x: x.endswith("A"), network):
        steps.append(0)
        while not node.endswith("Z"):
            node = network[node][path[steps[-1] % len(path)]]
            steps[-1] += 1

    return functools.reduce(math.lcm, set(steps))
