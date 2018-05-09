from getTeamNum import getTeamNum
from getPosNum import getPosNum
import csv
from lineups import lineups
print("Hello!  Welcome to MLB Lineup Optimizer")

numLineups = int(input("Enter number of desired lineups: "))

pStackNum = int(input("Enter number of players desired from primary stack: "))

sStackNum = int(input("Enter number of players from secondary stack: "))

lCross = int(input("Enter max number of lineup crossover: "))


salaryCap = 50000

players = [[], [], [], [], [], [], [], [], []]

# Read in csv of players and predictions
with open('players.csv', 'r') as csvfile:
    spamreader = csv.DictReader(csvfile)

    for row in spamreader:
        players[getPosNum(row['Subposition'])].append(
            [row['Name'], float(row['Value']), int(row['Salary']), getTeamNum(row['Team']), getTeamNum(row['Opp']),
                float(row['Ceil']), float(row['Floor'])]
        )

    # Reads in csv of desired team stacks
with open('stacks.csv', 'r') as csvfile:
    spamreader = csv.DictReader(csvfile)

    stacks = []
    for row in spamreader:
        stacks.append([getTeamNum(row['T1']), getTeamNum(row['T2'])])
lineups(numLineups, players, salaryCap, pStackNum, sStackNum, lCross, stacks)

print("Program finished")

