'''
This program is for training the naive bayes model
get the class count and total count in the data set
record the count for each words for each class
'''
import csv
import sys

#setting csv file maximum entries
csv.field_size_limit(2147483647)

#variables for tracking count
class0Count = 0
class1Count = 0

#defining variables for tracking word count
class0Words = dict()
class1Words = dict()
vocablary = set()

#total words in each class
class0WordCount = 0
class1WordCount = 0


#This is for reading the csv training sample
csvfile = open('training.csv', 'rt', encoding='utf8')
tweets = csv.reader(csvfile, delimiter = ' ', quotechar = '|')
for row in tweets:

    #add to class 0 dictionary and increase count
    if row[0].split(',')[1] == '0':
        for word in row[1:]:
            word = word.lower()
            class0WordCount += 1
            vocablary.add(word)
            if word in class0Words:class0Words[word] += 1
            else: class0Words[word] = 1
        class0Count += 1

    #add to class 1 dictionary and increase count
    else:
        for word in row[1:]:
            word = word.lower()
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

#input file
tweetData = open('tweets.txt','r')

def getPbyValues(tweet):
    #calcuate pby for class 0
    pby0 = pbyClass0
    for word in tweet:
        word = word.lower()
        if word not in class0Words: class0Words[word] = '0'
        pby0 *= (int(class0Words[word]) +1) / (class0WordCount + len(vocablary))
    
    #calculate pby for class 1
    pby1 = pbyClass1
    for word in tweet:
        word = word.lower()
        if word not in class1Words: class1Words[word] = '0'
        pby1 *= (int(class1Words[word]) + 1) / (class1WordCount + len(vocablary))

    #return positive or negative
    if pby0 > pby1:return -1
    else: return 1

#get the spilt factor
split = int(input('enter split factor: '))

for tweet in tweetData:
    #cleaning
    tweet = tweet.replace('\n','')
    
    #get each individual split of data
    scanString = []
    tweet = tweet.split(' ')
    slen = len(tweet)

    #initialize start end pair
    start = 0
    end = split

    #get the split strings
    if(slen <= split):scanString.append(tweet)
    else:
        while(end < slen):
            scanString.append(tweet[start:end])
            start = end
            if(end+split < slen):end = end+split
            else:
                scanString.append(tweet[start:slen])
                end = slen
                break

    totalSent = []
    #run for each split string
    for splitData in scanString:
        print(splitData)
        value = getPbyValues(splitData)
        totalSent.append(value)
        
    if totalSent.count(1) > totalSent.count(-1):print(' '.join(tweet)+': '+'Positive')
    else: print(' '.join(tweet)+': '+'Negative')
    
#close the csv file
csvfile.close()
tweetData.close()
