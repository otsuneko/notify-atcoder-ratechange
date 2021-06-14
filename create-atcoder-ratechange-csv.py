import csv
import requests
from requests.api import request

#Get Codeforces User Info
USER_NAME = "otsuneko"
response = requests.get("https://atcoder.jp/users/" + USER_NAME + "/history/json")
jsonData = response.json()

#Write Codeforces rate info. to CSV file
with open('atcoder.csv','w', newline='') as f:
    writer = csv.writer(f)
    for contest in jsonData:
        l = []
        l.append(contest["ContestScreenName"])
        l.append(contest["ContestName"])
        l.append(contest["EndTime"])
        l.append(contest["Place"])
        l.append(contest["Performance"])
        l.append(contest["OldRating"])
        l.append(contest["NewRating"])
        # for item in contest.items():
        #     l.append(item[1])
        writer.writerow(l)