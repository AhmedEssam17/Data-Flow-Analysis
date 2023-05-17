import math
from chars import *


def manageFile(filepath):
    file = open(filepath, 'r')
    splits = []
    word = ''
    opr = ''
    codeBox = ''

    lineNumber = 0
    variables = []
    occurrence = {}
    liveVariables = {}
    reachingDefinitions = {}

    for line in file:
        lineNumber += 1
        for char in line:
            codeBox += char
            if char in macro:
                break
            if char in separators:
                if word:
                    splits.append(word)
                if opr:
                    splits.append(opr)
                    opr = ''
                word = ''
            elif char in opers and char in doubleOpers:  # check for ++ or += or ....
                if word:
                    splits.append(word)
                opr += char
                word = ''
            elif char in opers:
                if word:
                    splits.append(word)
                splits.append(char)
                word = ''
            else:
                if opr:
                    splits.append(opr)
                    opr = ''
                word += char

    print(splits)

    statements = {}
    statm = ""
    flag = 0
    statNum = 0
    braces = 0
    incrFor = ""
    incrSplit = []
    operationsSplit = []
    mappingDictionary = {}
    conditionIndex = 0
    ifIndex = 0
    incrIndex = 0
    currentBraces = 0

    for i in range(4, len(splits)):
        if splits[i] in define:
            statm = splits[i] + " "
            operationsSplit.append(splits[i])
            while splits[i] != ';':
                if splits[i] in define:
                    i += 1
                    continue
                if splits[i] == ',':
                    statm = statm + splits[i] + " "
                    operationsSplit.append(splits[i])
                    i += 1
                    continue
                variables.append(splits[i])
                statm = statm + splits[i]
                operationsSplit.append(splits[i])
                i += 1
            statements[statNum] = statm
            if statNum not in mappingDictionary:
                mappingDictionary[statNum] = []
            mappingDictionary[statNum].append(statNum + 1)
            statNum += 1
            operationsSplit.append('~')
            statm = ""

        if splits[i] in scanf:
            statm = "scan("
            operationsSplit.append(splits[i])
            while splits[i] != '&':
                i += 1
            i += 1
            statm = statm + splits[i] + ")"
            operationsSplit.append(splits[i])
            statements[statNum] = statm
            if statNum not in mappingDictionary:
                mappingDictionary[statNum] = []
            mappingDictionary[statNum].append(statNum + 1)
            statNum += 1
            operationsSplit.append('~')
            statm = ""

        if splits[i] in printf:
            statm = "print("
            while splits[i] != ',' and splits[i] != ';':
                i += 1
            if splits[i] == ';':
                statm = ""
            else:
                i += 1
                operationsSplit.append("printf")
                operationsSplit.append(splits[i])
                statm = statm + splits[i] + ")"
                statements[statNum] = statm
                if statNum not in mappingDictionary:
                    mappingDictionary[statNum] = []
                mappingDictionary[statNum].append(statNum + 1)
                statNum += 1
                operationsSplit.append('~')
                statm = ""
                flag = 0

        if splits[i] == "for":
            semicol = 0
            braces += 1
            i += 2
            while splits[i] != '{':
                if splits[i] == ';':
                    semicol += 1
                    operationsSplit.append('~')
                    statements[statNum] = statm
                    if statNum not in mappingDictionary:
                        mappingDictionary[statNum] = []
                    mappingDictionary[statNum].append(statNum + 1)
                    if semicol == 2:
                        conditionIndex = statNum
                        if statNum not in mappingDictionary:
                            mappingDictionary[statNum] = []
                    statNum += 1
                    statm = ""
                    i += 1
                    continue
                if splits[i] == ')':
                    i += 1
                if semicol == 2:
                    incrFor = incrFor + splits[i]
                    incrSplit.append(splits[i])
                    i += 1
                else:
                    statm = statm + splits[i]
                    operationsSplit.append(splits[i])
                    i += 1

        if splits[i] == "if":
            currentBraces = braces
            braces += 1
            i += 2
            while splits[i] != ')':
                statm = statm + splits[i]
                operationsSplit.append(splits[i])
                i += 1
            statements[statNum] = statm
            if statNum not in mappingDictionary:
                mappingDictionary[statNum] = []
            mappingDictionary[statNum].append(statNum + 1)
            ifIndex = statNum
            statNum += 1
            operationsSplit.append('~')
            statm = ""

        if splits[i] == '}':
            braces -= 1
            if braces == 0:
                statements[statNum] = incrFor
                if statNum not in mappingDictionary:
                    mappingDictionary[statNum] = []
                mappingDictionary[statNum].append(conditionIndex)
                mappingDictionary[conditionIndex].append(statNum + 1)
                incrIndex = statNum
                statNum += 1
                incrFor = ""
                for x in incrSplit:
                    operationsSplit.append(x)
                operationsSplit.append('~')
            if currentBraces == braces:
                if ifIndex not in mappingDictionary:
                    mappingDictionary[ifIndex] = []
                nextInd = int(mappingDictionary[ifIndex][0])
                mappingDictionary[ifIndex].append(nextInd + 1)

        if splits[i] == "return":
            mappingDictionary[statNum-1] = "x"

    print(variables)
    print(statements)
    print(operationsSplit)
    print(mappingDictionary)

    operators = {}
    operands = {}

    for index in splits:
        if index in keyWords or index in opers:
            if index in operators:
                count = operators[index]
                count += 1
                operators[index] = count
            else:
                operators[index] = 1
        else:
            if index in operands:
                count = operands[index]
                count += 1
                operands[index] = count
            else:
                operands[index] = 1

    smallN1 = 0
    capitalN1 = 0
    smallN2 = 0
    capitalN2 = 0
    temp = 0

    for n in operators:
        capitalN1 += operators[n]
        smallN1 += 1

    for n in operands:
        capitalN2 += operands[n]
        smallN2 += 1

    ccCount = 1

    for n in operators:
        if n in loopWords:
            ccCount += operators[n]

    progLength = capitalN1 + capitalN2
    progVocab = smallN1 + smallN2
    estimatedLength = (smallN1 * math.log2(smallN1)) + (smallN2 * math.log2(smallN2))
    purityRatio = estimatedLength / progLength
    volume = estimatedLength * math.log2(progVocab)
    difficulty = (smallN1 / 2) * (capitalN2 / smallN2)
    progEffort = difficulty * volume
    progTime = progEffort / 18
    deliveredBug = volume / 3000

    results = {'n1': smallN1, 'N1': capitalN1, 'n2': smallN2, 'N2': capitalN2, 'progLength': progLength,
               'progVocab': progVocab,
               'estimatedLength': estimatedLength, 'purityRatio': purityRatio, 'volume': volume,
               'difficulty': difficulty,
               'progEffort': progEffort, 'progTime': progTime, 'deliveredBug': deliveredBug, 'codeBox': codeBox,
               'ccCount': ccCount}

    file.close()
    return results
