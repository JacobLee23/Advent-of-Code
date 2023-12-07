"""
Solution for Advent of Code 2023, Day 3
"""

import re
import string
import typing


def seek_number(line: str, index: int) -> int:
    """
    :param line:
    :param index:
    :return:
    :raise ValueError:
    """
    if not line[index].isdecimal():
        raise ValueError(line[index])
    digits = [line[index]]

    for char in reversed(line[:index]):
        if not char.isdecimal():
            break
        digits.insert(0, char)

    for char in line[(index + 1):]:
        if not char.isdecimal():
            break
        digits.append(char)

    return int("".join(digits))


def part1(input: str) -> typing.Any:
    """
    Solution for Part 1
    """
    result = 0
    array = input.split("\n")

    for row, line in enumerate(array):
        col = 0

        while col < len(line):
            if not line[col].isdecimal():
                col += 1
                continue

            num = re.search(r"\d+", line[col:]).group()
            start = col - 1 if col > 0 else col
            end = col + len(num) + 1 if col + len(num) < len(line) else col + len(num)

            characters = set()
            if start < col:
                characters.add(line[start])
            if end > col + len(num):
                characters.add(line[end - 1])
            if row > 0:
                characters.update(array[row - 1][start:end])
            if row < len(line) - 1:
                characters.update(array[row + 1][start:end])

            if (characters - {"."}) & set(string.punctuation):
                result += int(num)
            col = end

    return result


def part2(input: str) -> typing.Any:
    """
    Solution for Part 2
    """
    result = 0
    array = input.split("\n")

    for row, line in enumerate(array):
        for col, char in enumerate(line):
            if char != "*":
                continue

            start = col - 1 if col > 0 else col
            end = col + 1 if col < len(line) else col

            numbers = []
            if col > 0 and line[start].isdecimal():
                numbers.append(seek_number(line, start))
            if col < len(line) and line[end].isdecimal():
                numbers.append(seek_number(line, end))
            if row > 0:
                if array[row - 1][col].isdecimal():
                    numbers.append(seek_number(array[row - 1], col))
                else:
                    if array[row - 1][col - 1].isdecimal():
                        numbers.append(seek_number(array[row - 1], col - 1))
                    if array[row - 1][col + 1].isdecimal():
                        numbers.append(seek_number(array[row - 1], col + 1))
            if row < len(line) - 1:
                if array[row + 1][col].isdecimal():
                    numbers.append(seek_number(array[row + 1], col))
                else:
                    if array[row + 1][col - 1].isdecimal():
                        numbers.append(seek_number(array[row + 1], col - 1))
                    if array[row + 1][col + 1].isdecimal():
                        numbers.append(seek_number(array[row + 1], col + 1))

            if len(numbers) == 2:
                result += numbers[0] * numbers[1]

    return result
