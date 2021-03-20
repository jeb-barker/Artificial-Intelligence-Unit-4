"""Fill out a crossword structure specified on the command line with words from the specified dictionary. The
arguments, as with XWord1, are in the order HeightxWidth BlockCt dictToUse.txt V#x#spec ... H#x#spec where the Height
and Width identify the size of the crossword while BlockCt specifies the number of blocks.  dictToUse is a file where
each word appears on a distinct line.  All punctuation should be removed and all resulting letters should be upper
cased.  The remaining items specify letters and/or blocks to place at specific positions in the crossword.

The first eight tests currently use 20k.txt while the last two use the dictionary that Mr. Eckel provided.  Each test
run get 30 seconds.

Each problem is worth the same amount, and the score for a problem is a fraction where the denominator is twice the
number of letters that are to be filled in.  The numerator is given by the sum, for each letter to be filled in,
of how many complete, unique words it is in (either 0, 1, or 2)

The majority of the tests are on a 5x5 grid with at least one letter specified.

The final output crossword is the one that is examined, even if the script times out.   Letters that are not in two
distinct words are lower cased in the output shown to the user.  Because of the grading scheme, it might make sense to
only show output that is better than any prior output."""
# Jeb Barker, 3/4/2021
import os
import random
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


def check_complete(assignment, height, width, blocks, FAILED):

    xword = "".join(assignment)
    xw = BLOCKCHAR * (width + 3)
    xw += (BLOCKCHAR * 2).join([xword[p:p + width] for p in range(0, len(xword), width)])
    xw += BLOCKCHAR * (width + 3)
    illegalRegex = "([#](.?[-~]|[-~].?)[#])|([#].{}((.{})?[-~].{}|[-~].{}(.{})?)[#])".format("{" + str(width+1) + "}", "{" + str(width+2) + "}", "{" + str(width+1) + "}", "{" + str(width+1) + "}", "{" + str(width+2) + "}")

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


def recursive_backtracking(assignment, variables, height, width, blocks, FAILED):
    c = check_complete(assignment, height, width, blocks, FAILED)
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
        result = recursive_backtracking(assignment, variablesbutcooler, height, width, blocks, FAILED)
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
                w["word"] = match.group(4).upper() if match.group(4).upper() != "" else BLOCKCHAR
                w["direction"] = 1 if match.group(1).upper() == "H" else width
                w["coord"] = (width * int(match.group(2))) + int(match.group(3))
                words.append(w)
                # (3)
        else:
            dictionaryFile = arg

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
    FAILED = []
    xw = list(xw)
    bw = BLOCKCHAR * (width + 3)
    bw += (BLOCKCHAR * 2).join(["".join(xw)[p:p + width] for p in range(0, len(xw), width)])
    bw += BLOCKCHAR * (width + 3)
    final = ""
    variables = {}
    try:
        arr = area_fill("" + bw, [x for x in range(len(bw)) if bw[x] == OPENCHAR][0], width+2, "?")
    except IndexError:
        arr = []
    for x in range(len(xw)):
        if xw[x] == OPENCHAR:
            variables[x] = BLOCKCHAR
    if blocks == height * width:
        final = BLOCKCHAR * (height * width)
    elif OPENCHAR in arr or PROTECTEDCHAR in arr:
        for x in range(len(bw)):
            if bw[x] == OPENCHAR or bw[x] == PROTECTEDCHAR:

                b = area_fill("" + bw, x, width+2, "#")
                b = area_fill(b, len(b)-x, width+2, "#")
                b = "".join([b[p:p + width] for p in range(width + 3, len(b), width + 2)])  # remove border
                b = b[:height * width]
                if len(re.findall("#", b)) == blocks:
                    final = b
                    final = re.sub(PROTECTEDCHAR, OPENCHAR, final)
                    break
    else:
        out = recursive_backtracking(xw, variables, height, width, blocks, FAILED)
        final = re.sub(PROTECTEDCHAR, OPENCHAR, out)
    for word in words:
        c = word["coord"]
        for l in word["word"]:
            final = final[:c] + l + final[c+1:]
            c += word["direction"]
    # print(final)
    display(final, height, width)
    dictionary = {x: [] for x in range(50)}
    frequencyDict = {}
    with open(dictionaryFile) as file:
        for line in file.readlines():
            dictionary[len(line.strip().upper())].append(line.strip().upper())
            for index, char in enumerate(line.strip().upper()):
                wordTuple = (index, char, len(line.strip().upper()))
                if wordTuple not in frequencyDict:
                    frequencyDict[wordTuple] = 1
                else:
                    frequencyDict[wordTuple] += 1
    # print(dictionary)
    # print("\n", final)
    startPos = start_pos(width, height, final, dictionary)
    # print(startPos)
    # xw = transpose(final, height)
    # print(xw)
    display(word_backtracking(list(final), startPos, height, width, dictionary, frequencyDict), height, width)


def select_unassigned_var(assignment, variables):
    smol = None
    for x in range(len(variables)):
        if "-" in variables[x][3]:
            try:
                if variables[x][0] < variables[smol][0]:
                    smol = x
            except TypeError:
                smol = x
    return smol


def heuristic(frequencyDict, word):
    total = 0
    for index, char in enumerate(word):
        total += frequencyDict[(index, char, len(word))]
    return total


def check_words(assignment, variables, dictionary):
    if OPENCHAR in assignment:
        return False
    # else:
    #     # print("found a full board")
    #     pass
    # for var in variables:
    #     if var[3] not in dictionary[len(var[3])]:
    #         return False
    return True


def word_backtracking(assignment, variables, height, width, dictionary, frequencyDict):
    c = check_words(assignment, variables, dictionary)
    if c == True:
        assignment = "".join(assignment)
        return assignment
    vary = select_unassigned_var(assignment, variables)
    # print(len(variables))
    if vary is None:
        return None
    pw = variables[vary][4].sort(key=lambda word: heuristic(frequencyDict, word), reverse=True)
    for var in variables[vary][4]:
        dictionary[len(var)].remove(var)
        count = 0
        bad = False
        for index in variables[vary][1]:
            if assignment[index] != var[count] and assignment[index] != OPENCHAR:
                bad = True
            assignment[index] = var[count]
            count += 1
        if bad:
            return None
        variablesbutcooler = start_pos(width, height, "".join(assignment), dictionary)
        result = word_backtracking(assignment, variablesbutcooler, height, width, dictionary, frequencyDict)
        if result:
            return result
        else:
            count = 0
            for index in variables[vary][1]:
                assignment[index] = variables[vary][3][count]
                count += 1
            dictionary[len(var)].append(var)
    return None


def area_fill(board, sp, width, replChar):
    dirs = [-1, width, 1, -1 * width]
    if sp < 0 or sp >= len(board):
        return board
    if board[sp] in {OPENCHAR, PROTECTEDCHAR}:
        board = board[0:sp] + replChar + board[sp + 1:]
        for d in dirs:
            if d == -1 and sp % width == 0: continue  # left edge
            if d == 1 and sp + 1 % width == 0: continue  # right edge
            board = area_fill(board, sp + d, width, replChar)
    return board


def transpose(xw, newWidth):
    return "".join([xw[col::newWidth] for col in range(newWidth)])


def start_pos(width, height, board, all_words):
    xw = BLOCKCHAR*(width+3)
    xw += (BLOCKCHAR*2).join([board[p:p+width] for p in range(0, len(board), width)])
    xw += BLOCKCHAR*(width+3)
    pattern = r'[{}]({}|\w)*(?=[{}])'.format(BLOCKCHAR, OPENCHAR, BLOCKCHAR)
    regex = re.compile(pattern)
    width_turn = [width+2, height+2]
    pos_word_list = []
    for turn in range(2):
        for m in regex.finditer(xw):
            pos = 0
            pos_list = []
            word = xw[m.start()+1:m.end()]
            regex2 = re.compile('\\b' + word.replace(OPENCHAR, '\\w') + '\\b')
            if len(word)>0 and word.count(OPENCHAR) == 0 and turn == 0:
                pos_word_list.append([0, pos_list, 'H', word, []])

            elif len(word)>0 and word.count(OPENCHAR) == 0 and turn == 1:
                pos_word_list.append([0, pos_list, 'V', word, []])

            elif len(word)>0 and turn==0:
                candidates = [a for a in all_words[len(word)] if regex2.match(a) is not None]
                pos = ((m.start()+1)//(width+2)-1)*width + (m.start()+1) % (width+2) -1
                pos_list = [p for p in range(pos, pos+len(word))]
                pos_word_list.append([len(candidates), pos_list, 'H', word, candidates])
            elif len(word)>0 and turn == 1:
                if len(board) < 100:
                    candidates = [a for a in all_words[len(word)] if regex2.match(a) is not None]
                    pos = (((m.start()+1) % (height+2))-1)*width + (m.start()+1)//(height+2)-1
                    pos_list = [pos + p*width for p in range(len(word))]
                    pos_word_list.append([len(candidates), pos_list, 'V', word, candidates])
        xw = transpose(xw, width_turn[turn])
    # for item in pos_word_list:
    #     num_of_o = item[3].count(OPENCHAR)
    return pos_word_list


if __name__ == '__main__': main()
