#!/usr/bin/python3
import argparse
import os

from lib.settings import config


def parse_args():
    arguments = argparse.ArgumentParser(
        description="mknotes. Simple cli tool for creating and managing markdown notes."
    )

    arguments.add_argument("-a", "--add", dest="add", type=str, help="Add note")
    arguments.add_argument("-e", "--edit", dest="edit", type=str, help="Edit note")
    arguments.add_argument(
        "-d", "--delete", dest="delete", type=str, help="Delete note"
    )

    args = arguments.parse_args()

    return args


def main():
    arguments = parse_args()


if __name__ == "__main__":
    main()
