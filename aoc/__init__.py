"""
"""

import argparse
import logging
import os
import pathlib
import shutil


LOGGER = logging.getLogger(__name__)
STREAM_HANDLER = logging.StreamHandler()
FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
STREAM_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(STREAM_HANDLER)


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
        self.parser.add_argument("-v", "--verbose", action="count", default=0)

        subparsers = self.parser.add_subparsers(dest="name")

        parser_init = subparsers.add_parser("init", aliases=["i"])
        parser_init.add_argument("year", type=int)
        parser_init.add_argument("-f", "--force", action="store_true")
        parser_init.set_defaults(func=self.init)

        paser_remove = subparsers.add_parser("remove", aliases=["rm"])
        paser_remove.add_argument("year", type=int)
        paser_remove.set_defaults(func=self.remove)

        parser_solve = subparsers.add_parser("solve", aliases=["s"])
        parser_solve.add_argument("year", type=int)
        parser_solve.add_argument("-p", "--part", type=int, choices=[1, 2])
        parser_solve.add_argument("-t", "--test", action="store_true")
        parser_solve.set_defaults(func=self.solve)

        if not self.events.exists():
            os.mkdir(self.events)

        self.arguments = self.parser.parse_args()

    def init(self, args: argparse.Namespace) -> pathlib.Path:
        """
        :param args:
        :raise FileExistsError:
        """
        directory = self.events / str(args.year)
        if directory.exists():
            LOGGER.debug(
                "Directory already exists (force=%s): %s", self.arguments.force, directory
            )

            if args.force:
                shutil.rmtree(directory)
                LOGGER.debug("Removed directory and children: %s", directory)
            else:
                raise FileExistsError(directory)

        os.mkdir(directory)
        LOGGER.debug("Created directory: %s", directory)

        for day in range(1, 26):
            subdirectory = directory / str(day).zfill(2)
            os.mkdir(subdirectory)

            for file in os.listdir(self.template):
                shutil.copy(self.template / file, subdirectory / file)

            with open(subdirectory / "solution.py", "w+", encoding="utf-8") as file:
                file.write(file.read().format(year=args.year, day=day))

            LOGGER.debug("Copied directory: %s -> %s", self.template, subdirectory)

        return directory

    def remove(self, args: argparse.Namespace) -> pathlib.Path:
        """
        :param args:
        :return:
        :raise FileNotFoundError:
        """
        directory = self.events / str(args.year)
        if not directory.exists():
            LOGGER.debug("Directory already exists: %s", directory)
            raise FileNotFoundError(directory)

        shutil.rmtree(directory)
        LOGGER.debug("Removed directory: %s", directory)

        return directory
    
    def solve(self, args: argparse.Namespace) -> None:
        """
        :param args:
        """


def main():
    aoc = AdventOfCode()
    
    if aoc.arguments.verbose == 0:
        LOGGER.setLevel(logging.WARNING)
    elif aoc.arguments.verbose == 1:
        LOGGER.setLevel(logging.INFO)
    else:
        LOGGER.setLevel(logging.DEBUG)

    result = aoc.arguments.func(aoc.arguments)
    if aoc.arguments.name == "init":
        LOGGER.info("Initialized: %s", result)
    elif aoc.arguments.name == "remove":
        LOGGER.info("Removed: %s", result)
    elif aoc.arguments.name == "solve":
        LOGGER.info(result)
