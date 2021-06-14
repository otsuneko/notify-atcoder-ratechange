import os
import psycopg2
import requests
from requests.api import request

# Connect to Heroku PostgreSQL DB
def connect():
    con = psycopg2.connect(os.environ['DATABASE_URL'])
    return con

# Search a record from connected DB
def search_DB(con, sql):
    with con.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    return rows

# Insert a record to DB table
def insert_DB(con, sql, data):
    with con.cursor() as cur:
        cur.execute(sql, data)    
    con.commit()

# Send a notification to LINE
def line_notify(message):
    line_notify_token = os.environ['LINE_NOTIFY_API_KEY']
    line_notify_api = 'https://notify-api.line.me/api/notify'
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    requests.post(line_notify_api, data=payload, headers=headers)


# 1. Get Atcoder rating change history
user_name = os.environ['ATCODER_USER_NAME']
response = requests.get("https://atcoder.jp/users/" + user_name + "/history/json")
json_data = response.json()
latest_contest_info = json_data[-1]
contest_screen_name = latest_contest_info["ContestScreenName"]
contest_name = latest_contest_info["ContestName"]
end_time = latest_contest_info["EndTime"]
place = latest_contest_info["Place"]
performance = latest_contest_info["Performance"]
old_rating = latest_contest_info["OldRating"]
new_rating = latest_contest_info["NewRating"]

# 2. Check if latest contestId exists in DB. If not, insert the record and send the notification with LINE Notify
con = connect()
sql_search_latest_contest_info = "SELECT * FROM contests WHERE contest_id=" + str(contest_screen_name)
res = search_DB(con,sql_search_latest_contest_info)

# If there is an update
if not res:
    # Insert the latest contest info. into DB
    insert_info = (contest_screen_name, contest_name, end_time, place, performance, old_rating, new_rating)
    sql_insert_latest_contest_info = "INSERT INTO contests VALUES(%s, %s, %s, %s, %s, %s, %s)"
    insert_DB(con, sql_insert_latest_contest_info, insert_info)

    # send the Notification to LINE
    message = "\n" + contest_name + "\n" + "順位：" + str(place) + "位\n" + "パフォーマンス" + str(performance) + "相当\n" + "レーティング：" + str(old_rating) + "→" + str(new_rating)
    if old_rating < new_rating:
        message += "(+" + str(new_rating-old_rating) + ") :)"
    elif old_rating == new_rating:
        message += "(±0) :|"
    else:
        message += "(" + str(new_rating-old_rating) +") :("

    line_notify(message)
    