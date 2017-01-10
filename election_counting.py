import json
#import pandas as pd
#import matplotlib.pyplot as plt
import re


def word_in_text(word, text):
    if text is None:
        return False
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    else:
        return False


def main():
    tweets_data_path = 'tweets.txt'

    tweets_data = []
    tweets_file = open(tweets_data_path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet.get("text", None))
        except:
            continue
    trump = 0
    clinton = 0
    for index, item in enumerate(tweets_data):
        if word_in_text("trump", item):
            trump += 1
        if word_in_text("clinton", item):
            clinton += 1

    print("trump count: " + str(trump) + "\n")
    print("clinton count: " + str(clinton))


if __name__ == '__main__':
    main()
