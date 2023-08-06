"""
This is a helper tool that compares the committers in the Git history of a
repository to the names of people acknowledged in the allcontribtursrc file
in this repository.

Examples:
- Run the tool in the root of the repository:

    $ tools/didwegivecredit.py

- Run the tool on a repository in a different location:

    $ tools/didwegivecredit.py --path /path/to/root-directory

"""

import json
import shutil
import errno
from random import randint
from os.path import isfile
from pathlib import Path
from subprocess import run, PIPE
from fuzzywuzzy import fuzz, process
from rich import print as rprint
from rich.console import Console
from rich.style import Style
from rich.highlighter import Highlighter
from rich.table import Column, Table

class RainbowHighlighter(Highlighter):
    def highlight(self, text):
        for index in range(len(text)):
            text.stylize(index, index + 1, str(randint(16, 255)))

# bots don't need acknowledgement even though they are doing a great job
bots = ['allcontributors[bot]', 'The Gitter Badger', 'dependabot[bot]']
# some styles:
welcome = "orange1 on black"
rainbow = RainbowHighlighter()
attention = "bold white on black"
console = Console()


def get_committers(path, since=None):
    """
    Find all contributors to a project from the Git commit history

    Args:
        path: str; Path to the root of the git repository

    Returns:
        committers: list; Names of committers
    """

    cmd = ["git"]
    # But if we were pointed to a different location...
    if path != Path.cwd():
        # ... we need to modify the git call
        cmd.extend(["-C", str(path)])
    cmd.extend(["shortlog", "-s"])
    if since:
        # we want to specify a range
        cmd.extend(["{}..HEAD".format(since)])

    shortlog = run(cmd,
                   stdout=PIPE).stdout.decode().split('\n')

    committers = [c.split('\t', 1)[-1] for c in shortlog]

    return committers


def parse_allcontributors(allcontrib_file):
    """
    get the names and github handles of all contributors as acknowledged by
    the .allcontributorsrc file.

    Args:
        allcontrib_file: Path object
    Returns:
        allcontrib_names: list; names of contributors
        allcontrib_login: list; github handles of contributors
    """

    allcontrib = json.loads(allcontrib_file.read_text())

    allcontrib_names = [
        " ".join(val["name"].split(",")[::-1]).strip()
        for val in allcontrib["contributors"]
    ]
    allcontrib_login = [
        " ".join(val["login"].split(",")[::-1]).strip() for val in
        allcontrib["contributors"]
    ]
    return allcontrib_names, allcontrib_login


def match_authors(name, allcontrib_names, allcontrib_login):
    """
    Use fuzzy string matching to match names of committers
    to the names or handles mentioned in the allcontributors file.

    Args:
        name: str; name of committer
        allcontrib_names: list; names in allcontributorsrc file
        allcontrib_login: list; logins in allcontributorsrc file

    Returns:

    """

    # First, match the name. If no match, try Github login
    matching = process.extract(name,
                               allcontrib_names,
                               scorer=fuzz.token_sort_ratio,
                               limit=1)
    if matching[0][1] < 71:
        # we likely haven't found a match yet, lets check Github handles
        matching = process.extract(name,
                                   allcontrib_login,
                                   scorer=fuzz.token_sort_ratio,
                                   limit=1)
    if matching[0][1] >= 71:
        return [name, matching[0][0]], None
    else:
        return None, name


def get_new_contributors():
    """
    Query the Git log on which people committed in a given time frame
    and the .allcontributorsrc file which people were added
    :return:
    """


def report_on_missings(missings, path):
    """
    Summary report on potentially unaknowledged contributors
    Args:
        missings: list; Names of users

    Returns:
    """
    no = len(missings)
    if no == 0:
        console.print("\n:clap: Wonderful! I did not find commits of yet unacknowledged"
                      "contributors! :dizzy: \n\n", style=welcome)
    else:
        console.print("\n:point_down: [underline]Number of potentially unacknowledged "
                      "contributors to this repository:", style=attention)
        rprint(rainbow("{}\n".format(no)))
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Contributor", style='dim', width=12)
        table.add_column("Their contribution")
        for i, name in enumerate(missings):
            author = '--author={}'.format(name)

            cmd = ["git", "shortlog", author]
            if path != Path.cwd():
                # ... we need to modify the git call
                cmd = ["git", "-C", str(path), "shortlog", author]
            commits = run(cmd,
                          stdout=PIPE).stdout.decode().splitlines()[1:]
            #import pdb; pdb.set_trace()
            table.add_row(name + '\n', '\n'.join(commits).replace('  ', '') + '\n')
        console.print(table)



def generate_missings(committers,
                      bots,
                      allcontrib_names,
                      allcontrib_logins):
    """
    Find which committers are not mentioned in allcontributors file.

    Args:
        committers: list; names of all people that committed
        bots: list; names of all contributors to ignore
        allcontrib_names: list; names of all contributors in rc file
        allcontrib_logins: list; Github handles of all contributors in rc file

    Returns:
        missings: list; names of all committers who couldn't be matched
    """
    missings = []
    # check acknowledgements
    for name in committers:
        if name != '' and name not in bots:
            match, mismatch = match_authors(name,
                                            allcontrib_names,
                                            allcontrib_logins)
            if mismatch:
                missings.append(mismatch)

    return missings


def check(path,
          allcontrib_file,
          since=None):
    """
    Query the repository for unacknowledged contributors.
    Basic usage: tools/didweacknowledge [--path path/to/repo/clone] [ --since <hash/tag>]

    """

    committers = get_committers(path, since)
    allcontrib_names, allcontrib_logins = parse_allcontributors(allcontrib_file)
    missings = generate_missings(committers,
                                 bots,
                                 allcontrib_names,
                                 allcontrib_logins)

    msg = console.print("\n:sparkles: :sparkles: :sparkles:"
                        "\nRunning the didwegivecredit helper to find out whether "
                        "people have committed to the repository {} and may not be "
                        "acknowledged in the.allcontributorsrc file. \n"
                        ":sparkles: :sparkles: :sparkles:\n".format(
        path.resolve()), style=welcome, justify='center')
    report_on_missings(missings, path)

