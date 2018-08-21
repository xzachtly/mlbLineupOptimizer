import csv, random


def primeStacks(numLineups):

    primeStacks = ["T1"]
    secStacks = ["T2"]
    primePicks = ["CHC", "PIT", "MIA", "WAS", "TOR", "NYY", "BAL", "CLE", "SFG", "CIN", "TBR", "BOS", "COL", "ATL", "LAA", "TEX", "DET", "MIN", "KCR", "CHW", "MIL", "STL", "HOU", "OAK", "ARI", "SDP", "LAD", "SEA"]
    secPicks = ["CLE", "SFG", "HOU", "BOS", "ATL", "WAS", "ARI", "LAD", "TBR", "PIT"]

    for x in range(numLineups):
        pick1 = random.randint(0, len(primePicks)-1)
        primeStacks.append(primePicks[pick1])

    for y in range(numLineups):
        pick2 = random.randint(0, len(secPicks)-1)

        while secPicks[pick2] == primePicks[y+1]:
            pick2 = random.randint(0, len(secPicks)-1)

        secStacks.append(secPicks[pick2])

    stacks = []

    for x in range(0, numLineups + 1):
        stacks.append([primeStacks[x], secStacks[x]])

    myFile = open('stacks.csv', 'w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(stacks)



