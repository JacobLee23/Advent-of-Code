"""
Solution for Advent of Code 2023, Day 5
"""

import re
import typing


def get_seeds(input: str) -> typing.List[int]:
    """
    :param input:
    :return:
    """
    return list(map(int, re.findall(r"\d+", input.split("\n\n", 1)[0])))


def get_maps(input: str) -> typing.Dict[
    typing.Tuple[str, str], typing.List[typing.Tuple[int, int, int]]
]:
    """
    :param input:
    :return:
    """
    maps = {}

    for section in input.split("\n\n")[1:]:
        lines = section.split("\n")
        key = re.search(r"^(\w+)-to-(\w+) map:$", lines.pop(0)).groups()
        maps[key] = [tuple(map(int, re.findall(r"\d+", x))) for x in lines]

    return maps


def get_progression(input: str) -> typing.List[str]:
    """
    :param input:
    """
    progression = []

    for a, b in re.findall(r"(\w+)-to-(\w+) map:", input):
        if a not in progression:
            progression.append(a)
        if b not in progression:
            progression.append(b)

    return progression


def transform_seed(
    seed: int, transformation: typing.List[typing.Tuple[int, int, int]]
) -> int:
    """
    :param seed:
    :param transformation:
    :return:
    """
    for destination, source, length in transformation:
        if source <= seed < source + length:
            return destination + (seed - source)
        
    return seed


def transform_interval(
    interval: typing.Tuple[int, int], transformations: typing.List[typing.Tuple[int, int, int]]
) -> typing.List[typing.Tuple[int, int]]:
    """
    :param interval:
    :param transformations:
    :return:
    """
    intervals = []

    for destination, source, length in sorted(transformations, key=lambda x: x[1]):

        if interval[0] < source:
            if interval[0] + interval[1] < source:
                intervals.append(interval)
                return intervals
            elif interval[0] + interval[1] < source + length:
                intervals.append((interval[0], source - interval[0]))
                intervals.append((destination, interval[0] + interval[1] - source))
                return intervals
            else:
                intervals.append((interval[0], source))
                intervals.append((destination, length))
                interval = (source + length, (interval[0] + interval[1]) - (source + length))

        elif interval[0] < source + length:
            if interval[0] + interval[1] < source + length:
                intervals.append((destination + (interval[0] - source), interval[1]))
                return intervals
            else:
                intervals.append((destination + (interval[0] - source), length - (interval[0] - source)))
                interval = (source + length, (interval[0] + interval[1]) - (source + length))

    intervals.append(interval)
    
    return intervals


def part1(input: str) -> int:
    """
    Solution for Part 1
    """
    seeds, maps, progression = get_seeds(input), get_maps(input), get_progression(input)
    key = progression[0], progression[1]

    while True:
        seeds = [transform_seed(x, maps[key]) for x in seeds]

        if key[1] == progression[-1]:
            break
        key = key[1], progression[progression.index(key[1]) + 1]

    return min(seeds)


def part2(input: str) -> int:
    """
    Solution for Part 2
    """
    seeds, maps, progression = get_seeds(input), get_maps(input), get_progression(input)
    intervals = list(sorted(zip(seeds[::2], seeds[1::2]), key=lambda x: x[0]))
    key = progression[0], progression[1]

    while True:
        transformed = []
        for interval in intervals:
            transformed.extend(transform_interval(interval, maps[key]))
        intervals = transformed.copy()

        if key[1] == progression[-1]:
            break
        key = key[1], progression[progression.index(key[1]) + 1]

    return min(intervals, key=lambda x: x[0])[0]
