import pandas as pd

# Imports csv projection data from rotogrinders for pitchers and hitters, concatenates them and exports them to a joint
# csv file

hdata = pd.read_csv('https://rotogrinders.com/projected-stats/mlb-hitter.csv?site=draftkings', header=None)

pdata = pd.read_csv('https://rotogrinders.com/projected-stats/mlb-pitcher.csv?site=draftkings', header=None)

headers = pd.read_csv('Headers.csv', header=None)

hdata.append(pdata)

frames = [headers, hdata, pdata]
result = pd.concat(frames)

result.to_csv('players.csv', header=False, index=False)