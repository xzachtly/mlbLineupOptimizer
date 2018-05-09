from ortools.linear_solver import pywraplp

def lineupBuilder(players, salaryCap, lineups, stackNum, pStackNum, sStackNum, overlap, stacks):
    solver = pywraplp.Solver('CoinsGridCLP', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    currLineup = []

    rangeP = range(len(players[0]))
    rangeC = range(len(players[1]))
    range1B = range(len(players[2]))
    range2B = range(len(players[3]))
    range3B = range(len(players[4]))
    rangeSS = range(len(players[5]))
    rangeOF = range(len(players[6]))

    takeP = [solver.IntVar(0, 1, 'takeP[%i]' % j) for j in rangeP]
    takeC = [solver.IntVar(0, 1, 'takeC[%i]' % j) for j in rangeC]
    take1B = [solver.IntVar(0, 1, 'take1B[%i]' % j) for j in range1B]
    take2B = [solver.IntVar(0, 1, 'take2B[%i]' % j) for j in range2B]
    take3B = [solver.IntVar(0, 1, 'take3B[%i]' % j) for j in range3B]
    takeSS = [solver.IntVar(0, 1, 'takeSS[%i]' % j) for j in rangeSS]
    takeOF = [solver.IntVar(0, 1, 'takeOF[%i]' % j) for j in rangeOF]

    teamsP = []
    teamsC = []
    teams1B = []
    teams2B = []
    teams3B = []
    teamsSS = []
    teamsOF = []

    # Creates sum arrays for each position later to be used for stacking and limiting max players per team
    for teamNumber in range(0, 29):
        teamsP.insert(teamNumber, solver.Sum([(players[0][i][3] == teamNumber) * takeP[i] for i in rangeP]))
        teamsC.insert(teamNumber, solver.Sum([(players[1][i][3] == teamNumber) * takeC[i] for i in rangeC]))
        teams1B.insert(teamNumber, solver.Sum([(players[2][i][3] == teamNumber) * take1B[i] for i in range1B]))
        teams2B.insert(teamNumber, solver.Sum([(players[3][i][3] == teamNumber) * take2B[i] for i in range2B]))
        teams3B.insert(teamNumber, solver.Sum([(players[4][i][3] == teamNumber) * take3B[i] for i in range3B]))
        teamsSS.insert(teamNumber, solver.Sum([(players[5][i][3] == teamNumber) * takeSS[i] for i in rangeSS]))
        teamsOF.insert(teamNumber, solver.Sum([(players[6][i][3] == teamNumber) * takeOF[i] for i in rangeOF]))

    oppP = []
    oppC = []
    opp1B = []
    opp2B = []
    opp3B = []
    oppSS = []
    oppOF = []

    # Creates sum arrays for player's opposing teams.  This is later used to insure a team stack does not get picked
    # against an opposing pitcher
    for teamNumber in range(0, 29):
        oppP.insert(teamNumber, solver.Sum([(players[0][i][4] == teamNumber) * takeP[i] for i in rangeP]))
        oppC.insert(teamNumber, solver.Sum([(players[1][i][4] == teamNumber) * takeC[i] for i in rangeC]))
        opp1B.insert(teamNumber, solver.Sum([(players[2][i][4] == teamNumber) * take1B[i] for i in range1B]))
        opp2B.insert(teamNumber, solver.Sum([(players[3][i][4] == teamNumber) * take2B[i] for i in range2B]))
        opp3B.insert(teamNumber, solver.Sum([(players[4][i][4] == teamNumber) * take3B[i] for i in range3B]))
        oppSS.insert(teamNumber, solver.Sum([(players[5][i][4] == teamNumber) * takeSS[i] for i in rangeSS]))
        oppOF.insert(teamNumber, solver.Sum([(players[6][i][4] == teamNumber) * takeOF[i] for i in rangeOF]))

    lCrossP = []
    lCrossC = []
    lCross1B = []
    lCross2B = []
    lCross3B = []
    lCrossSS = []
    lCrossOF = []

    # Creates a sum array comparing each lineup to the lineups before it.  This is used to create varriance in the
    # lineups
    for j in range(0, len(lineups)):
        lCrossP.insert(j, solver.Sum([((players[0][i][0] == lineups[j][0]) or (players[0][i][0] == lineups[j][1])) * takeP[i] for i in rangeP]))
        lCrossC.insert(j, solver.Sum([(players[1][i][0] == lineups[j][2]) * takeC[i] for i in rangeC]))
        lCross1B.insert(j, solver.Sum([(players[2][i][0] == lineups[j][3]) * take1B[i] for i in range1B]))
        lCross2B.insert(j, solver.Sum([(players[3][i][0] == lineups[j][4]) * take2B[i] for i in range2B]))
        lCross3B.insert(j, solver.Sum([(players[4][i][0] == lineups[j][5]) * take3B[i] for i in range3B]))
        lCrossSS.insert(j, solver.Sum([(players[5][i][0] == lineups[j][6]) * takeSS[i] for i in rangeSS]))
        lCrossOF.insert(j, solver.Sum([((players[6][i][0] == lineups[j][7]) or (players[6][i][0] == lineups[j][8]) or (players[6][i][0] == lineups[j][9])) * takeOF[i] for i in rangeOF]))

    valueP = solver.Sum([players[0][i][1] * takeP[i] for i in rangeP])
    valueC = solver.Sum([players[1][i][1] * takeC[i] for i in rangeC])
    value1B = solver.Sum([players[2][i][1] * take1B[i] for i in range1B])
    value2B = solver.Sum([players[3][i][1] * take2B[i] for i in range2B])
    value3B = solver.Sum([players[4][i][1] * take3B[i] for i in range3B])
    valueSS = solver.Sum([players[5][i][1] * takeSS[i] for i in rangeSS])
    valueOF = solver.Sum([players[6][i][1] * takeOF[i] for i in rangeOF])

    ceilP = solver.Sum([players[0][i][5] * takeP[i] for i in rangeP])
    ceilC = solver.Sum([players[1][i][5] * takeC[i] for i in rangeC])
    ceil1B = solver.Sum([players[2][i][5] * take1B[i] for i in range1B])
    ceil2B = solver.Sum([players[3][i][5] * take2B[i] for i in range2B])
    ceil3B = solver.Sum([players[4][i][5] * take3B[i] for i in range3B])
    ceilSS = solver.Sum([players[5][i][5] * takeSS[i] for i in rangeSS])
    ceilOF = solver.Sum([players[6][i][5] * takeOF[i] for i in rangeOF])

    floorP = solver.Sum([players[0][i][6] * takeP[i] for i in rangeP])
    floorC = solver.Sum([players[1][i][6] * takeC[i] for i in rangeC])
    floor1B = solver.Sum([players[2][i][6] * take1B[i] for i in range1B])
    floor2B = solver.Sum([players[3][i][6] * take2B[i] for i in range2B])
    floor3B = solver.Sum([players[4][i][6] * take3B[i] for i in range3B])
    floorSS = solver.Sum([players[5][i][6] * takeSS[i] for i in rangeSS])
    floorOF = solver.Sum([players[6][i][6] * takeOF[i] for i in rangeOF])

    salaryP = solver.Sum([players[0][i][2] * takeP[i] for i in rangeP])
    salaryC = solver.Sum([players[1][i][2] * takeC[i] for i in rangeC])
    salary1B = solver.Sum([players[2][i][2] * take1B[i] for i in range1B])
    salary2B = solver.Sum([players[3][i][2] * take2B[i] for i in range2B])
    salary3B = solver.Sum([players[4][i][2] * take3B[i] for i in range3B])
    salarySS = solver.Sum([players[5][i][2] * takeSS[i] for i in rangeSS])
    salaryOF = solver.Sum([players[6][i][2] * takeOF[i] for i in rangeOF])

    # Constraint for keeping salary under the salary cap
    solver.Add(salaryP + salaryC + salary1B + salary2B + salary3B + salarySS + salaryOF <= salaryCap)

    # Sets number of player to pick per position
    solver.Add(solver.Sum(takeP[i] for i in rangeP) == 2)
    solver.Add(solver.Sum(takeC[i] for i in rangeC) == 1)
    solver.Add(solver.Sum(take1B[i] for i in range1B) == 1)
    solver.Add(solver.Sum(take2B[i] for i in range2B) == 1)
    solver.Add(solver.Sum(take3B[i] for i in range3B) == 1)
    solver.Add(solver.Sum(takeSS[i] for i in rangeSS) == 1)
    solver.Add(solver.Sum(takeOF[i] for i in rangeOF) == 3)

    # Max 5 hitters per team
    for i in range(0, 29):
        solver.Add(teamsC[i] + teams1B[i] + teams2B[i] + teams3B[i] + teamsSS[i] + teamsOF[i] <= 5)

    if stackNum <= 19:
        # Stack five hitters from primary team
        solver.Add(teamsC[stacks[stackNum][0]] + teams1B[stacks[stackNum][0]] + teams2B[stacks[stackNum][0]]
                   + teams3B[stacks[stackNum][0]] + teamsSS[stacks[stackNum][0]] + teamsOF[stacks[stackNum][0]] == pStackNum)
        solver.Add(oppP[stacks[stackNum][0]] == 0)

        # Stack three hitters from secondary team
        solver.Add(teamsC[stacks[stackNum][1]] + teams1B[stacks[stackNum][1]] + teams2B[stacks[stackNum][1]]
                   + teams3B[stacks[stackNum][1]] + teamsSS[stacks[stackNum][1]] + teamsOF[stacks[stackNum][1]] == sStackNum)
        solver.Add(oppP[stacks[stackNum][1]] == 0)

    else:
        for i in range(0, 29):
            solver.Add(oppP[i] + teamsC[i] + teams1B[i] + teams2B[i] + teams3B[i] + teamsSS[i] + teamsOF[i] <= 1)


    # Add constraint to adjust for lineup overlap
    for i in range(0, len(lineups)):
        solver.Add(lCrossP[i] + lCrossC[i] + lCross1B[i] + lCross2B[i] + lCross3B[i] + lCrossSS[i] + lCrossOF[i] <= overlap)

    varP = ceilP - floorP
    varC = ceilC - floorC
    var1B = ceil1B - floor1B
    var2B = ceil2B - floor2B
    var3B = ceil3B - floor3B
    varSS = ceilSS - floorSS
    varOF = ceilOF - floorOF

    solver.Maximize(valueP + varC + var1B + var2B + var3B + varSS + varOF)
    solver.Solve()
    assert solver.VerifySolution(1e-7, True)
    print('Solved in', solver.wall_time(), 'milliseconds!', "\n")

    salary = 0
    projection = 0
    ceilProjection = 0
    floorProjection = 0

    for i in rangeP:
        if (takeP[i].SolutionValue()):
            salary += players[0][i][2]
            projection += players[0][i][1]
            ceilProjection += players[0][i][5]
            floorProjection += players[0][i][6]
            currLineup.append(players[0][i][0])

    for i in rangeC:
        if (takeC[i].SolutionValue()):
            salary += players[1][i][2]
            projection += players[1][i][1]
            ceilProjection += players[1][i][5]
            floorProjection += players[1][i][6]
            currLineup.append(players[1][i][0])

    for i in range1B:
        if (take1B[i].SolutionValue()):
            salary += players[2][i][2]
            projection += players[2][i][1]
            ceilProjection += players[2][i][5]
            floorProjection += players[2][i][6]
            currLineup.append(players[2][i][0])

    for i in range2B:
        if (take2B[i].SolutionValue()):
            salary += players[3][i][2]
            projection += players[3][i][1]
            ceilProjection += players[3][i][5]
            floorProjection += players[3][i][6]
            currLineup.append(players[3][i][0])

    for i in range3B:
        if (take3B[i].SolutionValue()):
            salary += players[4][i][2]
            projection += players[4][i][1]
            ceilProjection += players[4][i][5]
            floorProjection += players[4][i][6]
            currLineup.append(players[4][i][0])

    for i in rangeSS:
        if (takeSS[i].SolutionValue()):
            salary += players[5][i][2]
            projection += players[5][i][1]
            ceilProjection += players[5][i][5]
            floorProjection += players[5][i][6]
            currLineup.append(players[5][i][0])

    for i in rangeOF:
        if (takeOF[i].SolutionValue()):
            salary += players[6][i][2]
            projection += players[6][i][1]
            ceilProjection += players[6][i][5]
            floorProjection += players[6][i][6]
            currLineup.append(players[6][i][0])


    return [currLineup, salary, projection, ceilProjection, floorProjection]
