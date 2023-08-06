"""
PEP 008 like analysis module.
=============================

The rules are quite limited right now (only 6).
The approach, a statefull line-by-line test using a class,
smells a lot.

We will need to do a simpler version of this with we want to go furthet.
(Well, for the moment,  if it iin't broke, don't fix it... )

Note. The way lines are counted seems a bit strange. Need a sanity scheck.

"""
BLOCKS = [
    "PROGRAM",
    "SUBROUTINE",
    "MODULE",
    "FUNCTION",
]

__all__ = ["struct_analysis"]


class LangFtn:
    """ class with all info and function specific to a fortran statement.

    Do we need to be classy here???
    """

    def __init__(self, stmt_list):

        lowerblck = [str_.lower() for str_ in BLOCKS]
        self.block_lst = lowerblck
        self.cur_block = None
        self.statement_lst = stmt_list

    def bstart(self, statement):
        """ return true when statement is a starting block
        """
        clean_st = rm_comment(statement)
        clean_st = clean_st.lower()
        # needed else end block  can be understood as start
        out = False
        for st_match in self.block_lst:
            if clean_st.startswith(st_match):
                out = True
                self.cur_block = clean_st.split()[1]

        return out

    def bstop(self, statement):
        """ return true when statement is an ending block
        """
        clean_st = rm_comment(statement)
        clean_st = clean_st.lower()
        for st_match in self.block_lst:
            if clean_st.startswith("end " + st_match):
                return True
        return False


def testifdo(statement, cur_ifdo, cur_depth):
    """ return true when statement is a starting block
    """
    clean_st = rm_comment(statement)
    # needed else end block  can be understood as start

    for st_match in ["IF", "DO", "if", "do"]:
        if clean_st.startswith(st_match):
            cur_ifdo += 1
            cur_depth = max(cur_depth, cur_ifdo)

        for ending in ["END", "END ", "end", "end "]:
            if clean_st.startswith(ending + st_match):
                cur_ifdo -= 1

    return cur_ifdo, cur_depth


def rm_comment(statement_str):
    """remove comment in statement_string
    """
    if statement_str[0] in ["!", "c", "C"]:
        return str()
    if "!" in statement_str:
        return statement_str.split("!")[0]
    return statement_str.strip()


def get_arguments(head):
    """ get arguments in the header of a block
    """
    start_idx = head.find("(") + 1
    end_idx = head.find(")")
    list_args = head[start_idx:end_idx].split(",")
    list_args = [name.strip() for name in list_args]
    return list_args


def get_variables(statement_lst):
    """ identifie a declaration line and give the list of varaibles
    """
    types_lst = ["REAL", "DOUBLE PRECISION", "LOGICAL", "INTEGER", "CHARACTER"]
    list_var = list()
    for statement in statement_lst:
        for typename in types_lst:
            if statement.startswith(typename):
                if "::" in statement:
                    list_var.extend(statement.split("::")[-1].split(","))
    list_var = [name.strip() for name in list_var]
    return list_var


def test_blockst(statement_lst):
    """ analysis of a block """

    # print("Analysis of :", statement_lst[0])
    clean_statement_lst = list(filter(None, (rm_comment(st) for st in statement_lst)))
    out = {
        "statements": clean_statement_lst,
        "args": get_arguments(statement_lst[0]),
        "locals": list(),
        "errors": list(),
    }
    for name in get_variables(clean_statement_lst):
        if name not in out["args"]:
            out["locals"].append(name)

    cur_ifdo = 0
    cur_depth = 0
    for statement in clean_statement_lst:
        cur_ifdo, cur_depth = testifdo(statement, cur_ifdo, cur_depth)

    out["errors"].extend(statements_errors(clean_statement_lst))
    out["errors"].extend(vars_errors(out["locals"]))
    out["errors"].extend(args_errors(out["args"]))
    out["errors"].extend(ifdoerrors(cur_depth))

    return out


def statements_errors(stt_list):
    """Assess staments"""
    out = list()
    lstat = len(stt_list)
    if lstat > 50:
        out.append("pep8-too-many-lines : " + str(lstat) + "/50")

    for stat in stt_list:
        if len(stat) > 100:
            out.append("pep8-line-too-long : " + str(len(stat)) + "/100")
    return out


def vars_errors(var_list):
    """Assess variables errors"""
    out = list()
    lstat = len(var_list)
    if lstat > 12:
        out.append("pep8-too-many-locals : " + str(lstat) + "/12")

    for varname in var_list:
        if len(varname) < 3:
            out.append("pep8-invalid-name : local var " + varname + " is too short")
    return out


def ifdoerrors(maxdepth):
    """Assess bock if and do complexity"""
    out = list()
    if maxdepth > 5:
        out.append(
            "pep8-too-many-levels : " + str(maxdepth) + "/5 nested IF and DO blocks"
        )

    return out


def args_errors(arg_list):
    """Assess arguments errors"""
    out = list()
    larg = len(arg_list)
    if larg > 5:
        out.append("pep8-too-many-arguments : " + str(larg) + "/5")

    for varname in arg_list:
        if len(varname) < 3:
            out.append("pep8-invalid-name : argument " + varname + " is too short")
    return out


def print_errors(info_errors):
    """PRint humar readable error log."""
    for block in info_errors:
        print(block + " :")
        for err in info_errors[block]["errors"]:
            print("  ", err)


def count_errors(info_errors):
    """Convert errors infos for statistics."""
    broken_rules = dict()
    for block in info_errors:
        for err in info_errors[block]["errors"]:
            key = err.split(":")[0]
            if key in broken_rules:
                broken_rules[key] += 1
            else:
                broken_rules[key] = 1
    return broken_rules


def struct_analysis(st_code, verbose=False):
    """ split a code into blocks
    st_code : raw string of file with carriage returns
    output a dictionary of blocks
    """
    code = LangFtn(st_code)
    buff_list = list()
    info_errors = dict()
    for statement in code.statement_lst:
        buff_list.append(statement)
        if code.bstart(statement):
            buff_list = [statement]
            continue

        if code.bstop(statement):
            info_errors[code.cur_block] = test_blockst(buff_list)
            buff_list = list()
            continue

    lines_nb = 0
    errors_nb = 0
    for block in info_errors:
        lines_nb += len(info_errors[block]["statements"])
        errors_nb += len(info_errors[block]["errors"])

    if verbose:
        print_errors(info_errors)

    return errors_nb, lines_nb, count_errors(info_errors)
