"""
Format analysis module.
=======================

This will use the regexp rules given in configuration file to identify errors.
It intends to follows the coding conventions
mentioned in
`OMS Documentation Wiki page <https://alm.engr.colostate.edu/cb/wiki/16983>`__

The repalcement pipeline exists but is not implemented fully,
since I am not so sure of the result for multiple errors in one line.

"""
from flinter.formatting import parse_format_line, init_format_rules


__all__ = ["fmt_analysis"]


def fmt_analysis(lines, verbose=True):
    """Start the linter of file FILENAME."""
    all_errors = dict()
    lines_nb = 0
    errors_nb = 0
    format_rules = init_format_rules()

    for i, line in enumerate(lines, 1):
        if line.strip().startswith("!>"):  #  Doxygen pragma
            continue
        if line.strip().startswith("!!"):  #  Doxygen pragma
            continue
        if line.strip() == "":  # . Blank line
            continue

        lines_nb += 1

        errors_found = parse_format_line(line, i, format_rules, verbose)

        for key in errors_found:

            nb_ = len(errors_found[key])
            errors_nb += nb_
            if key in all_errors:
                all_errors[key] += nb_
            else:
                all_errors[key] = nb_

    broken_rules = dict()
    for key in all_errors:
        broken_rules[format_rules[key]["message"]] = all_errors[key]

    return errors_nb, lines_nb, broken_rules
