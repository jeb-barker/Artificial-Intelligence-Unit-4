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
from copy import deepcopy

BLOCKCHAR = "#"
OPENCHAR = "-"
PROTECTEDCHAR = "~"


def display(xword, height, width):
    for x in range(height):
        b = xword[x*width: x*width+width]
        print(b)


def check_complete(assignment, height, width, blocks):
    xword = "".join(assignment)
    xw = BLOCKCHAR * (width + 3)
    xw += (BLOCKCHAR * 2).join([xword[p:p + width] for p in range(0, len(xword), width)])
    xw += BLOCKCHAR * (width + 3)
    illegalRegex = "([#](.?[~-]|[~-].?)[#])|([#].{}((.{})?[~-].{}|[~-].{}(.{})?)[#])".format("{" + str(width+1) + "}", "{" + str(width+2) + "}", "{" + str(width+1) + "}", "{" + str(width+1) + "}", "{" + str(width+2) + "}")

    if re.search(illegalRegex, xw):
        return -1
    if len(re.findall("#", xword)) == blocks:
        return True
    return False


def update_variables(value, var_index, assignment, variables):
    del variables[var_index]
    try:
        del variables[len(assignment) - 1 - var_index]
    except KeyError:
        pass
    return variables


def recursive_backtracking(assignment, variables, height, width, blocks):
    c = check_complete(assignment, height, width, blocks)
    if c == True:
        assignment = "".join(assignment)
        return assignment
    if c == -1:
        return None
    # var = select_unassigned_var(assignment, variables)
    # print(len(variables))
    for var in variables:
        assignment[var] = BLOCKCHAR
        assignment[len(assignment) - 1 - var] = BLOCKCHAR
        variablesbutcooler = {a: b for a, b in variables.items()} # variables.deepcopy()
        variablesbutcooler = update_variables(BLOCKCHAR, var, assignment, variablesbutcooler)
        result = recursive_backtracking(assignment, variablesbutcooler, height, width, blocks)
        if result:
            return result
        else:
            assignment[var] = OPENCHAR
            assignment[len(assignment) - 1 - var] = OPENCHAR
            # print("back")
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
                # print(1)
            elif re.search(intTest[1], arg, re.I):
                match = re.search(intTest[1], arg, re.I)
                blocks = int(match.group(0))
                # print(2)
            elif re.search(intTest[2], arg, re.I):
                match = re.search(intTest[2], arg, re.I)
                w = {}
                w["word"] = match.group(4).upper()
                w["direction"] = 1 if match.group(1).upper() == "H" else width
                w["coord"] = (width * int(match.group(2))) + int(match.group(3))
                words.append(w)
                # (3)

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
        xword = xword[:(height*width)//2] + BLOCKCHAR + xword[(height*width)//2 + 1:]
        # print((height*width)//2)
    elif blocks % 2 == 0 and height*width % 2 != 0:
        xword = xword[:(height * width) // 2] + PROTECTEDCHAR + xword[(height * width) // 2 + 1:]
    xw = BLOCKCHAR * (width + 3)
    xw += (BLOCKCHAR * 2).join([xword[p:p + width] for p in range(0, len(xword), width)])
    xw += BLOCKCHAR * (width + 3)

    # display(xw, height + 2, width + 2)
    print()
    for x in range(len(xw)):
        if xw[x] == PROTECTEDCHAR or xw[x] == BLOCKCHAR:
            xw = xw[:len(xw)-x-1] + xw[x] + xw[len(xw)-x:]

    substituteRegex = "[{}]{}(?=[{}])".format(BLOCKCHAR, OPENCHAR, BLOCKCHAR)
    subRE2 = "[{}]{}{}(?=[{}])".format(BLOCKCHAR, OPENCHAR, OPENCHAR, BLOCKCHAR)
    subRE3 = "#[^#]{3}#"
    subRE4 = "(?<=[#].{})-(?=.{}[#])".format("{"+str(width+1)+"}", "{"+str(width+1)+"}")
    subRE5 = "(?<=[#].{}-.{})-(?=.{}[#])".format("{"+str(width+1)+"}", "{"+str(width+1)+"}", "{"+str(width+1)+"}")

    xw = re.sub(substituteRegex, BLOCKCHAR * 2, xw)
    xw = re.sub(subRE5, BLOCKCHAR, xw)
    xw = re.sub(subRE4, BLOCKCHAR, xw)
    xw = re.sub(subRE2, BLOCKCHAR * 3, xw)
    xw = re.sub(subRE3, BLOCKCHAR+PROTECTEDCHAR*3+BLOCKCHAR, xw)

    xw = re.sub("#\w--", BLOCKCHAR + PROTECTEDCHAR * 3, xw)
    xw = re.sub("--\w#", PROTECTEDCHAR * 3 + BLOCKCHAR, xw)
    xw = re.sub("#\w-", BLOCKCHAR + PROTECTEDCHAR*2, xw)
    xw = re.sub("-\w#", PROTECTEDCHAR*2+BLOCKCHAR, xw)
    xw = re.sub("(?<=#.{}\w.{}.{})-|-(?=>.{}.{}\w.{}#)".format("{"+str(width+1)+"}", "{"+str(width+1)+"}", "{"+str(width+2)+"}", "{"+str(width+2)+"}", "{"+str(width+1)+"}", "{"+str(width+1)+"}"), PROTECTEDCHAR, xw)
    xw = re.sub("((?<=#.{}\w.{})-)|(-(?=>.{}\w.{}#))".format("{"+str(width+1)+"}","{"+str(width+1)+"}","{"+str(width+1)+"}","{"+str(width+1)+"}"), PROTECTEDCHAR, xw)

    xw = re.sub("\w", PROTECTEDCHAR, xw)
    # display(xw, height+2, width+2)
    xw = "".join([xw[p:p + width] for p in range(width+3, len(xw), width+2)])  # remove border
    xw = xw[:height*width]
    # print()
    # display(xw, height, width)
    for x in range(len(xw)):
        if xw[x] == PROTECTEDCHAR or xw[x] == BLOCKCHAR:
            xw = xw[:len(xw)-x-1] + xw[x] + xw[len(xw)-x:]

    # display(xword, height, width)
    # print()
    # display(xw, height, width)
    # print(xw)
    # print(str(height)+" x "+str(width))

    xw = list(xw)
    variables = {}
    for x in range(len(xw)):
        if xw[x] == OPENCHAR:
            variables[x] = BLOCKCHAR
    if blocks == height * width:
        final = BLOCKCHAR * (height * width)
    else:
        final = recursive_backtracking(xw, variables, height, width, blocks)
        final = re.sub(PROTECTEDCHAR, OPENCHAR, final)
    for word in words:
        c = word["coord"]
        for l in word["word"]:
            final = final[:c] + l + final[c+1:]
            c += word["direction"]
    # print(final)
    display(final, height, width)
    # print("\n", final)


if __name__ == '__main__': main()
