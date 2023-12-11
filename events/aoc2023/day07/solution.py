"""
Solution for Advent of Code 2023, Day 7
"""

import re
import typing


CARDS = "AKQJT98765432"


def classify(hand: str, *, joker: bool = False) -> typing.Tuple[int, int, int, int, int, int]:
    """
    :param hand:
    :return:
    """
    cardset = "AKQT98765432J" if joker else "AKQJT98765432"
    strengths = [(5,), (4, 1), (3, 2), (3, 1, 1), (2, 2, 1), (2, 1, 1, 1), (1, 1, 1, 1, 1)]
    cards = {x: hand.count(x) for x in set(hand)}

    if joker:
        if cards == {"J": 5}:
            counts = (5,)
        else:
            counts = [v for k, v in cards.items() if k != "J"]
            counts[counts.index(max(counts))] += cards.get("J", 0)
            counts = tuple(sorted(counts, reverse=True))
    else:
        counts = tuple(sorted(cards.values(), reverse=True))

    return (strengths.index(counts), *[cardset.index(x) for x in hand])


def part1(input: str) -> int:
    """
    Solution for Part 1
    """
    hands = {
        a: int(b) for a, b in (
            re.search(r"([2-9TJQKA]{5}) (\d+)", x).groups() for x in input.split("\n")
        )
    }
    return sum(
        (i + 1) * hands[x] for i, x in enumerate(sorted(hands, key=classify, reverse=True))
    )


def part2(input: str) -> typing.Any:
    """
    Solution for Part 2
    """
    hands = {
        a: int(b) for a, b in (
            re.search(r"([2-9TJQKA]{5}) (\d+)", x).groups() for x in input.split("\n")
        )
    }
    return sum(
        (i + 1) * hands[x] for i, x in enumerate(
            sorted(hands, key=lambda x: classify(x, joker=True), reverse=True)
        )
    )
