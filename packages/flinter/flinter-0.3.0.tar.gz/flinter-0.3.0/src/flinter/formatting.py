"""Module containing base functions to lint
    and dectect broken formatting rules
"""
import re
import pkg_resources
import yaml


def init_format_rules(line_length=132):
    """Load format rules from resosurces.

    :param line_length: int, opt. max line accepted"""
    syntax_rules = pkg_resources.resource_filename("flinter", "rules/syntax.yaml")
    format_rules = pkg_resources.resource_filename("flinter", "rules/format_rules.yaml")
    with open(syntax_rules) as fin:
        syntax = yaml.load(fin, Loader=yaml.FullLoader)
    with open(format_rules) as fin:
        rules = yaml.load(fin, Loader=yaml.FullLoader)

    for key in syntax:
        syntax[key] = r"|".join(syntax[key])

    # keys = ['message', 'regexp', 'replacement']
    syntax["types_upper"] = syntax["types"].upper()
    syntax["linelen"] = "%s" % line_length
    syntax["linelen_re"] = "{%s}" % line_length
    for key in rules:
        rules[key] = _compile_format_rule(rules[key], syntax)
    return rules


def _compile_format_rule(rule, syntax):
    """Compile the regexp action for a rule
    :param rule: dict
        - message
        - regexp
        - repalcement
        the rules to be implemented
        some rules a based upon lists stored in syntax
    :param syntax: dict
        - types
        - operators
        - structs
        - punctuation
        language specific lists of items

    """
    if rule["message"] is not None:
        rule["message"] = rule["message"].format(**syntax)
    else:
        rule["message"] = None

    rule["regexp"] = re.compile(rule["regexp"].format(**syntax))

    return rule


def parse_format_line(line, line_no, rules, verbose):
    """Analyse line

    :param line: str, line itself
    :param line_no: int, position in the file
    :param rules: rules read from config

    :returns :
        dict {
            rule_name : nb_of_error
        )
         """
    msg_info = {"line_no": line_no, "line": line.replace("\n", "")}
    out = dict()
    for key in rules:
        rule = rules[key]
        error_nb = _parse_format_rule(line, msg_info, rule, verbose=verbose)

        if error_nb > 0:
            try:
                out[key].append(msg_info)
            except KeyError:
                out[key] = [msg_info]

    return out


def _parse_format_rule(line, msg_info, rule, verbose):
    """Interpret rules

    :param line: str, line to check
    :param msg_info: dict, identifier of position
    :param rule: key to the rules dictionnary

    return:
        dict
        errors: number of errors
        modifs: number of mofifs
    """
    error_nb = 0
    modifs_nb = 0
    replacement = line
    for res in rule["regexp"].finditer(line):
        msg_info["column"] = res.start() + 1
        if rule["replacement"] is not None:
            modifs_nb += 1
            replacement = rule["regexp"].sub(rule["replacement"], replacement)
        msg_info["replacement"] = replacement
        if rule["message"] is not None:
            error_nb += 1
            if verbose:
                print(_str_msg(rule["message"], msg_info))
                print("|" + replacement)

    return error_nb


def _str_msg(msg, info):
    """Format error message.

    :param msg: category of message
    :param info: dict locating the error."""
    pos = " " * (info["column"]) + "^"
    template = "{info[line_no]}:{info[column]}:"
    template = template + "{msg} :\n"
    template = template + "|{info[line]}\n"
    template = template + "|{pos}"
    show_msg = template.format(info=info, msg=msg, pos=pos)
    return show_msg
