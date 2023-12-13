"""
Solution for Advent of Code 2023, Day 10
"""

import typing


def connections(array: typing.List[str], row: int, col: int) -> typing.Set[typing.Tuple[int, int]]:
    """
    :param array:
    :param row:
    :param col:
    :return:
    """
    connections = set()
    node = array[row][col]

    if node in "|LJS" and row > 0 and array[row - 1][col] in "|7FS":
        connections.add((row - 1, col))
    if node in "|7FS" and row < len(array) - 1 and array[row + 1][col] in "|LJS":
        connections.add((row + 1, col))
    if node in "-J7S" and col > 0 and array[row][col - 1] in "-LFS":
        connections.add((row, col - 1))
    if node in "-LFS" and col < len(array[0]) - 1 and array[row][col + 1] in "-J7S":
        connections.add((row, col + 1))

    return connections


def determinant(a: typing.Tuple[int, int], b: typing.Tuple[int, int]) -> int:
    """
    :param a:
    :param b:
    :return:
    """
    return a[0] * b[1] - b[0] * a[1]


def part1(input: str) -> int:
    """
    Solution for Part 1
    """
    array = input.split("\n")
    node, points = divmod(input.index("S"), len(array) + 1), set()

    while True:
        points.add(node)
        try:
            node = (connections(array, *node) - points).pop()
        except KeyError:
            return (len(points) + 1) // 2


def part2(input: str) -> int:
    """
    Solution for Part 2
    """
    array = input.split("\n")
    node, points, boundary = divmod(input.index("S"), len(array) + 1), set(), []

    while True:
        points.add(node)
        boundary.append(node)
        try:
            node = (connections(array, *node) - points).pop()
        except KeyError:
            break

    area = (1 / 2) * sum(determinant(boundary[i - 1], p) for i, p in enumerate(boundary))
    return int((area + 1) - len(boundary) / 2)
