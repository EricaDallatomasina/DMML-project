import twint
import os
from datetime import date
from Backend.Preprocess import makePreprocess


def addTweets():
    now = date.today()
    datetime_now = now.strftime("%Y-%m-%d %H:%M:%S")
    # print(datetime_now)

    output_file = "Backend/scraped.csv"
    __scrapeTweets(__getLastDatetime(), datetime_now, output_file)

    if os.path.exists('Backend/scraped.csv'):
        makePreprocess(output_file)
        os.remove(output_file)

    with open("Backend/lastTimestamp.txt", "w") as f:
        f.write(datetime_now)


def __scrapeTweets(datetime_from, datetime_to, output_file):
    string = __readKeywords()
    c = twint.Config()
    c.Lang = 'it'
    c.Search = string
    c.Custom["tweet"] = ["id", "date", "time", "username", "tweet", "likes_count"]
    c.Since = datetime_from
    c.Until = datetime_to
    c.Store_csv = True
    c.Filter_retweets = True
    c.Output = output_file
    c.Hide_output = True
    twint.run.Search(c)


def __getLastDatetime():
    with open('Backend/lastTimestamp.txt', 'r') as f:
        last = f.readline()
    return last


def __readKeywords():
    string = ""
    condition = " OR "
    start = True
    with open('Backend/keywords.txt', 'r') as file:
        for line in file:
            if start:
                start = False
            else:
                string += condition

            string += line.strip()
    # print(string)
    return string
