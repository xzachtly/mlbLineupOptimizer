import csv
from lineupBuilder import lineupBuilder


def lineups(numLineups, players, salaryCap, pStackNum, sStackNum, overlap, stacks):

    lineupList = []
    resultList = []
    lineupList.append(['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'])

    for stackNum in range(0, numLineups):
        results = lineupBuilder(players, salaryCap, lineupList, stackNum, pStackNum, sStackNum, overlap, stacks)
        lineupList.append(results[0])
        resultList.append(results)

    lineupsOnly = [['P', 'P', 'C', '1B', '2B', '3B', 'SS', 'OF', 'OF', 'OF']]

    for i in range(0, numLineups):
        lineupsOnly.append(resultList[i][0])

    # Create csv file of lineups
    myFile = open('lineups.csv', 'w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(lineupsOnly)

    print("Writing complete")

    # Create csv file of lineups with additional results
    mF2 = open('lineupsWithResults.csv', 'w')
    with mF2:
        writer = csv.writer(mF2)
        writer.writerows(resultList)

    print("Writing complete")

    return resultList
