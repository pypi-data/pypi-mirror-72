#!/usr/bin/env python
"""
Command line Interface
======================


CLI using Click. The scoring formula and presentation is also in this module.

Note that fmt is contributing to warnings, while pep8 is contributing to errors.
Therefore one pep8 error cost 5 times more than a fmt error on your score.

"""
import os
import glob
import click
from flinter.struct_analysis import struct_analysis
from flinter.fmt_analysis import fmt_analysis


@click.group()
def main_cli():
    """--------------------    FLINT  ---------------------

.      - Flint, because our code stinks... -


You are now using the Command line interface of Flint,
a Fortran linter created at CERFACS (https://cerfacs.fr).

This is a python package currently installed in your python environement.

"""
    pass


@click.command()
@click.argument("file", nargs=1)
def fmt(file):
    """Score the formatting of .f90 FILE.
    """
    print(f"\n File {file}\n")
    with open(file, "r") as fin:
        lines = fin.readlines()
    warnings_nb, lines_nb, broken_rules = fmt_analysis(lines, verbose=True)
    print_broken_rules(broken_rules)
    print_score(0, warnings_nb, lines_nb)


main_cli.add_command(fmt)


@click.command()
@click.argument("folder", nargs=1)
def all_files(folder, rate_fmt=True, rate_pep8=True):
    """Score the formatting of all .f90 FILE under a folder arboressence.
    """
    files = []
    for motif in ["*.f90", "*.f"]:
        files += glob.glob(os.path.join(folder, "**", motif), recursive=True)
    # affichage:
    all_errors_nb = 0
    all_warnings_nb = 0
    all_lines_nb = 0
    all_broken_rules = dict()
    unreadable_files = []
    for i, fname in enumerate(files):
        print(f"({i+1}/{len(files)})   File {fname} \n")
        try:
            with open(fname, "r") as fin:
                lines = fin.readlines()

            if rate_fmt:
                warnings_nb, lines_nb, broken_rules = fmt_analysis(lines, verbose=False)

                all_warnings_nb += warnings_nb
                all_lines_nb += lines_nb
                for key in broken_rules:
                    if key in all_broken_rules:
                        all_broken_rules[key] += broken_rules[key]
                    else:
                        all_broken_rules[key] = broken_rules[key]

            if rate_pep8:
                errors_nb, lines_nb, broken_rules = struct_analysis(
                    lines, verbose=False
                )

                all_errors_nb += errors_nb
                # all_lines_nb += lines_nb
                for key in broken_rules:
                    if key in all_broken_rules:
                        all_broken_rules[key] += broken_rules[key]
                    else:
                        all_broken_rules[key] = broken_rules[key]

        except UnicodeDecodeError as err:
            print(err)
            unreadable_files.append(fname)

    print(f"\n {len(files)} Files parsed.")
    if unreadable_files:
        print("\nUnreadable_files:\n")
        print("\n -".join(unreadable_files))

    print_broken_rules(all_broken_rules)
    print_score(all_errors_nb, all_warnings_nb, all_lines_nb)


main_cli.add_command(all_files)


@click.command()
@click.argument(
    "file", nargs=1,
)
def pep8(file):
    """Score the complexity of .f90 FILE.
    """
    with open(file, "r") as fin:
        lines = fin.readlines()
    errors_nb, lines_nb, broken_rules = struct_analysis(lines, verbose=True)
    print_broken_rules(broken_rules)
    print_score(errors_nb, 0, lines_nb)


main_cli.add_command(pep8)


def comp_rate(errors_nb, warnings_nb, lines_nb):
    """Compute score.

    Formula is taken from Pylint."""
    rate = (float(errors_nb * 5 + warnings_nb) / lines_nb) * 10
    rate = 10.0 - rate
    return rate


def print_score(errors_nb, warnings_nb, lines_nb):
    """Footer showing the score"""
    print(f"\n\n Score on {lines_nb} lines:")
    score = comp_rate(errors_nb, warnings_nb, lines_nb)
    print(50 * "-")
    print("Your code has been rated at " + "{0:4.2f}".format(score) + "/10\n")


def print_broken_rules(broken_rules):
    """Footer showing a summary of the broken rules"""
    print("\n\n Broken rules:")
    print(50 * "-")
    for key in broken_rules:
        print(key, ":", broken_rules[key])
