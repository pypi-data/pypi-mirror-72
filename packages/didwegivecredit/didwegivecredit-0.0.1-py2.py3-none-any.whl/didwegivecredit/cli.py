"""Console script for didwegivecredit."""
import argparse
import sys
import errno
from pathlib import Path
from os.path import isfile
from os import strerror
from .didwegivecredit import check


def main():

    parser = argparse.ArgumentParser(description="{}".format(main.__doc__))
    parser.add_argument(
        "-p",
        "--path",
        help="""Provide a path to the root of a Git repository.
        Default: Current directory""",
        default='.'
    )
    parser.add_argument(
        "-a",
        "--allcontributors",
        help="""Provide a path to the .allcontributorsrc file of your repository.
        If not provided, it is assumed to be in the root of the provided path
        or current directory"""
    )
    parser.add_argument(
        "-s",
        "--since",
        help="""Specify a commit hash from when on the history should be checked.
        Example: ./didwegivecredit.py --since abb826407d5d7bf76""",
    )
    parser.add_argument(
        "-i",
        "--ignore-committer",
        nargs='+',
        help="""Specify the name of a committer to ignore in this run of the
        script. To ignore a committer for all subsequent calls of this script,
        add their name to the bots list in the script (useful for bots)."""
    )
    args = parser.parse_args()

    if args.ignore_committer:
        names = args.ignore_committer
        for name in names:
            if name not in bots:
                bots.append(name)
            else:
                print("\n\nNote: I was told to ignore {},"
                      " but I am already doing this!".format(name))
        print("\n\nCurrently, the following committers are ignored in this "
              "run:\n{}".format(" \n".join(bots)))

    path = Path(args.path) if args.path else Path('.').resolve()

    if args.allcontributors:
        allcontrib_file = Path(args.allcontributors).resolve()
    else:
        allcontrib_file = path / ".all-contributorsrc"
    if not isfile(allcontrib_file):
        raise FileNotFoundError(
            errno.ENOENT, strerror(errno.ENOENT), allcontrib_file)

    since = args.since or None

    check(path, allcontrib_file, since)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
