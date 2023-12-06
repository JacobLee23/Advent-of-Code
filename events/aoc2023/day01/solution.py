"""
Solution for Advent of Code 2023, Day 1
"""

import re
import typing


DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def normalize_str(string: str, *, reverse: bool = False) -> str:
    """
    :param string:
    :param reverse:
    :return:
    """
    digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    if reverse:
        digits, string = [s[::-1] for s in digits], string[::-1]

    return re.sub(
        f"({'|'.join(digits)})", lambda m: str(digits.index(m.group()) + 1), string
    )


def part1(input: str) -> int:
    """
    Solution for Part 1
    """
    result = 0

    for line in input.split("\n"):
        digits = re.findall(r"\d", line)
        result += 10 * int(digits[0]) + int(digits[-1])

    return result


def part2(input: str) -> typing.Any:
    """
    Solution for Part 2
    """
    result = 0

    for line in input.split("\n"):
        first = re.findall(r"\d", normalize_str(line))[0]
        last = re.findall(r"\d", normalize_str(line, reverse=True))[0]
        result += 10 * int(first) + int(last)
    
    return result
