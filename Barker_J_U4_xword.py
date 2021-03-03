"""This lab is for the creation of a structure that can hold a valid US-style crossword puzzle.
The command line inputs to the script are:
#x# where the two # symbols represent the height and width of the crossword.  The height will be in [3,15] while the width is in [3,30].

# where the # represents an integer for the number of blocks (black squares) the puzzle must have.

The dictionary file name - it should be ignored for this lab.

H#x#chars and V#x#chars where the two # symbols are the vertical and horizontal (0 based) position, respectively,
of the indicated chars.  An H indicates a horizontal orientation, while a V indicates a vertical one.  These should
be processed in the order encountered in the command line.

NOTE WELL: If no US-style crossword rule precludes it (see below), and if no prior H or V entry precludes it, then any time characters are placed and there is a run of at least 3 on the crossword grid, the ends may be bracketed by a block (or edge).  This does not mandate placement of blocks at such indicated positions, but it may be done.

There will be a series of 10 problems (currently there are 8).

Note that the block character is "#" (the use of # above is to indicate a number, and not as a character) and the open character is "-".  Since this might change, In your code, you should not have these inline, but rather set explicitly with:
BLOCKCHAR = "#"
OPENCHAR = "-"

The rules for US-style crosswords:
Block positions must be symmetric with respect to 180 degree rotation about the center.
All letters must be in both a horizontal and vertical word.
All words must be at least three letters.
All non-block entries should be connected.
No duplicate words in the crossword."""

# Jeb Barker, 3/2/2021
import os
import re
import sys
from copy import copy, deepcopy

BLOCKCHAR = "#"
OPENCHAR = "-"
PROTECTEDCHAR = "~"


def display(xword, height, width):
    for x in range(height):
        b = xword[x*height: x*height+width]
        print(b)


def initial_variables(puzzle, csp_table, neighbors):
    out = {}
    for x in range(0, height * width):
        out[x] = {y for y in range(1, 10)} if puzzle[x] == "." else {int(puzzle[x])}
    for var in out:
        for val in out[var]:
            if len(out[var]) == 1:
                update_variables(val, var, puzzle, out, csp_table, neighbors)
    return out


def check_complete(assignment):
    return False


def ordered_domain(assignment, variables, freq):
    return sorted(variables, key=lambda a: 9 - freq[a], reverse=False)


def select_unassigned_var(assignment, variables):
    smol = None
    for x in range(81):
        if assignment[x] == '.':
            try:
                if len(variables[x]) < len(variables[smol]):
                    smol = x
            except KeyError:
                smol = x
    return smol
    # return assignment.index(min([(a, b) for a, b in enumerate(assignment)], key=lambda val: len(variables[val[0]]) if val[1] != "." else 10)[1])


def update_variables(value, var_index, assignment, variables, csp_table, neighbors):
    for var in neighbors[var_index]:
        if value in variables[var]:
            # variables[var] = {a for a in variables[var] if a != value}
            c = variables[var].copy()
            c.remove(value)
            variables[var] = c
    return variables


def recursive_backtracking(assignment, variables, csp_table_temp, neighbors):
    if check_complete(assignment):
        assignment = "".join(assignment)
        return assignment
    var = select_unassigned_var(assignment, variables)
    for value in variables[var]:
        assignment[var] = str(value)
        variablesbutcooler = variables.copy()  # {a: b for a, b in variables.items()} # variables.deepcopy()
        variablesbutcooler = update_variables(value, var, assignment, variablesbutcooler, csp_table_temp, neighbors)
        result = recursive_backtracking(assignment, variablesbutcooler, csp_table_temp, neighbors)
        if result:
            return result
        else:
            assignment[var] = "."
    return None


def main():
    intTest = ["^(\d+)x(\d+)$", "^\d+$", "^(H|V)(\d+)x(\d+)(.+)$"]
    words = []
    for arg in sys.argv:
        if not os.path.isfile(arg):
            if re.search(intTest[0], arg, re.I):
                match = re.search(intTest[0], arg, re.I)
                height = int(match.group(1))
                width = int(match.group(2))
                print(1)
            elif re.search(intTest[1], arg, re.I):
                match = re.search(intTest[1], arg, re.I)
                blocks = int(match.group(0))
                print(2)
            elif re.search(intTest[2], arg, re.I):
                match = re.search(intTest[2], arg, re.I)
                w = {}
                w["word"] = match.group(4).upper()
                w["direction"] = 1 if match.group(1).upper() == "H" else width
                w["coord"] = (width * int(match.group(2))) + int(match.group(3))
                words.append(w)
                print(3)

    xword = ""
    for x in range(height * width):
        xword += OPENCHAR
    xw = deepcopy(xword)
    for word in words:
        c = word["coord"]
        for l in word["word"]:
            xword = xword[:c] + l + xword[c+1:]
            xw = xw[:c] + PROTECTEDCHAR + xw[c+1:]
            c += word["direction"]

    print(blocks)
    if blocks % 2 != 0 and height*width % 2 != 0:
        xword = xword[:(height*width)//2] + PROTECTEDCHAR + xword[(height*width)//2 + 1:]
        print((height*width)//2)

    xw = BLOCKCHAR * (width + 3)
    xw += (BLOCKCHAR * 2).join([xword[p:p + width] for p in range(0, len(xword), width)])
    xw += BLOCKCHAR * (width + 3)

    xw = re.sub("#\w\w-", BLOCKCHAR + PROTECTEDCHAR * 3, xw)
    xw = re.sub("#\w-", BLOCKCHAR + PROTECTEDCHAR*2, xw)
    xw = re.sub("(?<=#.{8}\w.{8}.{9})-|-(?=>.{9}.{8}\w.{8}#)", PROTECTEDCHAR, xw)
    xw = re.sub("((?<=#.{8}\w.{8})-)|(-(?=>.{8}\w.{8}#))", PROTECTEDCHAR, xw)

    xw = re.sub("\w", PROTECTEDCHAR, xw)

    xw = "".join([xw[p:p + width] for p in range(10, len(xw), width+2)]) #remove border
    display(xword, height, width)
    print()
    display(xw, height, width)
    print(str(height)+" x "+str(width))

if __name__ == '__main__': main()