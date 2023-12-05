"""
"""

import argparse


class Parser(argparse.ArgumentParser):
    """
    """
    def __init__(self):
        super().__init__(prog=__name__, description=__doc__, epilog="Advent of Code")

        self.subparsers = self.add_subparsers()

        self.parse_args()


def main():
    parser = Parser()
