"""
"""

import argparse
import os
import pathlib
import shutil


class AdventOfCode:
    """
    """
    root = pathlib.Path(__file__).parent
    events = pathlib.Path("events")
    template = root / "template"

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog=__name__, description=__doc__, epilog="Advent of Code"
        )

        subparsers = self.parser.add_subparsers(dest="name")

        parser_init = subparsers.add_parser("init", aliases=["i"])
        parser_init.add_argument("year", type=int)
        parser_init.add_argument("-f", "--force", action="store_true")
        parser_init.set_defaults(func=self.init)

        parser_init = subparsers.add_parser("remove", aliases=["rm"])
        parser_init.add_argument("year", type=int)
        parser_init.set_defaults(func=self.remove)

        if not self.events.exists():
            os.mkdir(self.events)

        self.arguments = self.parser.parse_args()
        directory = self.arguments.func(self.arguments)

        print(directory)

    def init(self, args: argparse.Namespace) -> pathlib.Path:
        """
        :param args:
        :raise FileExistsError:
        """
        directory = self.events / str(args.year)
        if directory.exists():
            if args.force:
                shutil.rmtree(directory)
            else:
                raise FileExistsError(directory)

        os.mkdir(directory)

        for day in range(1, 26):
            subdirectory = directory / str(day).zfill(2)
            os.mkdir(subdirectory)

            for file in os.listdir(self.template):
                shutil.copy(self.template / file, subdirectory / file)

            with open(subdirectory / "solution.py", "w+", encoding="utf-8") as file:
                file.write(file.read().format(year=args.year, day=day))

        return directory

    def remove(self, args: argparse.Namespace) -> pathlib.Path:
        """
        :param args:
        :return:
        :raise FileNotFoundError:
        """
        directory = self.events / str(args.year)
        if not directory.exists():
            raise FileNotFoundError(directory)

        shutil.rmtree(directory)

        return directory


def main():
    aoc = AdventOfCode()
