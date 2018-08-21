import requests as rq
import pandas as pd

destinationFilePathHit = "/Users/zacharyduncan/Code/mlbLineupOptimizer/hitters.csv"  # set this, this must be the fully qualified file path for your operating system.
url = "https://rotogrinders.com/projected-stats/mlb-hitter.csv"
params = {"site": "draftkings"}
response = rq.get(url=url, params=params, stream=True)

print("Downloading file to \"{ffp}\"".format(ffp=destinationFilePathHit))
with open(destinationFilePathHit, "wb") as fileHandle:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            fileHandle.write(chunk)

destinationFilePathPitch = "/Users/zacharyduncan/Code/mlbLineupOptimizer/pitchers.csv"  # set this, this must be the fully qualified file path for your operating system.
url = "https://rotogrinders.com/projected-stats/mlb-hitter.csv"
params = {"site": "draftkings"}
response = rq.get(url=url, params=params, stream=True)

print("Downloading file to \"{ffp}\"".format(ffp=destinationFilePathPitch))
with open(destinationFilePathPitch, "wb") as fileHandle:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            fileHandle.write(chunk)

print("Download complete")


# pitchers and hitters csv's still need to be concatennated and header added