"""
"""

import argparse
import importlib
import logging
import os
import pathlib
import shutil
import typing


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

        parser_init = subparsers.add_parser("init")
        parser_init.add_argument("year", type=int)
        parser_init.add_argument("-f", "--force", action="store_true")
        parser_init.set_defaults(func=self.init)

        parser_remove = subparsers.add_parser("remove")
        parser_remove.add_argument("year", type=int)
        parser_remove.set_defaults(func=self.remove)

        parser_repair = subparsers.add_parser("repair")
        parser_repair.add_argument("year", type=int)
        parser_repair.set_defaults(func=self.repair)

        parser_solve = subparsers.add_parser("solve")
        parser_solve.add_argument("year", type=int)
        parser_solve.add_argument("day", type=int)
        parser_solve.add_argument("-t", "--test", action="store_true")
        parser_solve.set_defaults(func=self.solve)

        if not self.events.exists():
            os.mkdir(self.events)

        self.arguments = self.parser.parse_args()

        self.directory = self.events / f"aoc{self.arguments.year}"

    def init(self, args: argparse.Namespace) -> pathlib.Path:
        """
        :param args:
        :raise FileExistsError:
        """
        if self.directory.exists():
            LOGGER.debug(
                "Directory already exists (force=%s): %s", self.arguments.force, self.directory
            )

            if args.force:
                shutil.rmtree(self.directory)
                LOGGER.debug("Removed directory and children: %s", self.directory)
            else:
                raise FileExistsError(self.directory)

        os.mkdir(self.directory)
        LOGGER.debug("Created directory: %s", self.directory)

        for day in range(1, 26):
            subdirectory = self.directory / f"day{str(day).zfill(2)}"
            os.mkdir(subdirectory)
            LOGGER.debug("Created directory: %s", subdirectory)

            for file in os.listdir(self.template):
                shutil.copyfile(self.template / file, subdirectory / file)
                LOGGER.debug("Copied file: %s -> %s", self.template / file, subdirectory / file)

            with open(subdirectory / "solution.py", "r", encoding="utf-8") as file:
                formatted = file.read().format(year=args.year, day=day)
                LOGGER.debug("Read .py file: %s", subdirectory / "solution.py")

            with open(subdirectory / "solution.py", "w", encoding="utf-8") as file:
                file.write(formatted)
                LOGGER.debug("Formatted .py file: %s", subdirectory / "solution.py")

            LOGGER.debug("Copied directory: %s -> %s", self.template, subdirectory)

        return self.directory

    def remove(self) -> pathlib.Path:
        """
        :param args:
        :return:
        :raise FileNotFoundError:
        """
        if not self.directory.exists():
            LOGGER.debug("Directory does not exist: %s", self.directory)
            raise FileNotFoundError(self.directory)

        shutil.rmtree(self.directory)
        LOGGER.debug("Removed directory: %s", self.directory)

        return self.directory
    
    def repair(self) -> pathlib.Path:
        """
        :param args:
        :return:
        :raise FileNotFoundError:
        """
        if not self.directory.exists():
            LOGGER.debug("Directory does not exist: %s", self.directory)
            raise FileNotFoundError(self.directory)
        
        for day in range(1, 26):
            subdirectory = self.directory / f"day{str(day).zfill(2)}"
            if not subdirectory.exists():
                LOGGER.debug("Directory does not exist: %s", subdirectory)
                os.mkdir(subdirectory)
                LOGGER.debug("Created directory: %s", subdirectory)

            for file in os.listdir(self.template):
                if not (subdirectory / file).exists():
                    LOGGER.debug("File does not exist: %s", subdirectory / file)
                    shutil.copyfile(self.template / file, subdirectory / file)
                    LOGGER.debug("Copied file: %s -> %s", self.template / file, subdirectory / file)

            for file in os.listdir(subdirectory):
                if not (self.template / file).exists():
                    LOGGER.debug("Unknown file discovered: %s", subdirectory / file)
                    os.remove(subdirectory / file)
                    LOGGER.debug("Removed file: %s", subdirectory / file)

        return self.directory
    
    def solve(self, args: argparse.Namespace) -> None:
        """
        :param args:
        """
        return Solver(self.directory / f"day{str(args.day).zfill(2)}")


class Solver:
    """
    :param directory:
    """
    def __init__(self, directory: pathlib.Path):
        self.directory = directory
        self.module = importlib.import_module(
            ".".join(os.path.normpath(directory / "solution").split(os.sep))
        )

    def result(self, part: int, test: bool) -> typing.Any:
        """
        :aram part:
        :param test:
        :return:
        """
        with open(
            self.directory / (f"testin{part}.txt" if test else "in.txt"), "r", encoding="utf-8"
        ) as file:
            if part == 1:
                return self.module.part1(file.read())
            elif part == 2:
                return self.module.part2(file.read())
            else:
                raise ValueError(part)
            
    def expected(self, part: int) -> str:
        """
        :param part:
        :return:
        """
        with open(self.directory / f"testout{part}.txt", "r", encoding="utf-8") as file:
            return file.read()
        
    def check(self, part: int) -> typing.Optional[typing.Tuple[bool, typing.Any, typing.Any]]:
        """
        :param part:
        :return:
        """
        result = self.result(part, True)
        try:
            expected = type(result)(self.expected(part))
        except TypeError:
            return None

        return result == expected, result, expected
    
    def solve(self, part: int) -> typing.Any:
        """
        :param part:
        :return:
        """
        result = self.result(part, False)
        with open(self.directory / f"out{part}.txt", "w", encoding="utf-8") as file:
            file.write(str(result))

        return result


def main():
    aoc = AdventOfCode()
    
    if aoc.arguments.verbose == 0:
        LOGGER.setLevel(logging.WARNING)
    elif aoc.arguments.verbose == 1:
        LOGGER.setLevel(logging.INFO)
    else:
        LOGGER.setLevel(logging.DEBUG)

    LOGGER.info(aoc.arguments.__dict__)
    if aoc.arguments.name == "init":
        directory: pathlib.Path = aoc.arguments.func(aoc.arguments)
        LOGGER.info("Initialized: %s", directory)
    elif aoc.arguments.name == "remove":
        directory: pathlib.Path = aoc.arguments.func()
        LOGGER.info("Removed: %s", directory)
    elif aoc.arguments.name == "repair":
        directory: pathlib.Path = aoc.arguments.func()
        LOGGER.info("Repaired: %s", directory)
    elif aoc.arguments.name == "solve":
        solver: Solver = aoc.arguments.func(aoc.arguments)
        for n in (1, 2):
            if aoc.arguments.test:
                test, solve = solver.check(n), None
            else:
                test, solve = solver.check(n), solver.solve(n)
            LOGGER.info(f"Part {n}:\n\tTest:\t{test}\n\tSolve:\t{solve}")
        LOGGER.info("Solved: %s", solver.directory)
