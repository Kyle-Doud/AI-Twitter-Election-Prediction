import csv, sys, json
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

#learn naive bayes
csv.field_size_limit(2147483647)

class0Count = 0
class1Count = 0

class0Words = dict()
class1Words = dict()
vocablary = set()

class0WordCount = 0
class1WordCount = 0

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

csvfile = open('training.csv', 'rt', encoding='utf8')
tweets = csv.reader(csvfile, delimiter = ' ', quotechar = '|')
for row in tweets:
    #handle class negative
    if row[0].split(',')[1] == '0':
        for word in row[1:]:
            class0WordCount += 1
            vocablary.add(word)
            if word in class0Words:class0Words[word] += 1
            else: class0Words[word] = 1
        class0Count += 1
    #handle class positive
    else:
        for word in row[1:]:
            class1WordCount += 1
            vocablary.add(word)
            if word in class1Words:class1Words[word] += 1
            else: class1Words[word] = 1
        class1Count += 1

totalCount = class0Count + class1Count
class0Voc = len(class0Words)
class1Voc = len(class1Words)

#p(c)
pbyClass0 = class0Count / totalCount
pbyClass1 = class1Count / totalCount

trump = 0
clinton = 0
#apply naive bayes
tweets_file = open('tweets.txt','r', encoding='utf8')
tweets_data = []
for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet.get("text", None))
        except:
            continue
for tweet in tweets_data:
    try:
        tweet = tweet.replace('\n','')
        
        #calcuate pby for class 0
        pby0 = pbyClass0
        for word in tweet.split(' '):
            if word not in class0Words: class0Words[word] = '0'
            pby0 *= (int(class0Words[word]) +1) / (class0WordCount + len(vocablary))
        
        #calculate pby for class 1
        pby1 = pbyClass1
        for word in tweet.split(' '):
            if word not in class1Words: class1Words[word] = '0'
            pby1 *= (int(class1Words[word]) + 1) / (class1WordCount + len(vocablary))

        if pby0 > pby1:
            #print(tweet.translate(non_bmp_map)+': '+'Negative \r')
            if word_in_text("trump", tweet):
                trump -= 1
            if word_in_text("clinton", tweet):
                clintion -= 1
            if word_in_text("hrc", tweet):
                clintion -= 1
        else:
            #print(tweet.translate(non_bmp_map)+': '+'Positive \r')
            if word_in_text("trump", tweet):
                trump += 1
            if word_in_text("clinton", tweet):
                clinton += 1
            if word_in_text("hrc", tweet):
                clintion += 1
    except:
        continue
print("trump positive count: " + str(trump) + "\n")
print("clinton positive count: " + str(clinton))
csvfile.close()
tweets_file.close()
