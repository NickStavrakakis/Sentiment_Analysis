# -*- coding: utf-8 -*- #using this for printing emojis to test clear_emojis() function

import string
import csv
import io
#import nltk #run once to install
from nltk.corpus import stopwords
#nltk.download('stopwords') #run once to install
from nltk.tokenize import sent_tokenize, word_tokenize
#nltk.download('punkt') #run once to install
from nltk.stem import PorterStemmer

def stemming(w):
    ps = PorterStemmer()
    return ps.stem(w)

def cleaning(s):
    s = s.lower() #lowercase the current tweet
    for char in string.punctuation:
        s = s.replace(char, '')
    cleared_string = ""
    word_tokens = word_tokenize(s) 
    for word in word_tokens:
        word = stemming(word)
        if word not in stopwords.words('english') and \
            not word.startswith("http://") and \
            not word.startswith("@") and \
            all(ord(char) < 128 for char in word):
                cleared_string += word
                cleared_string += ' '
    return cleared_string

tweets = []

with open('twitter_data/test2017.tsv') as input_file:
    reader = csv.reader(input_file, delimiter='\t')
    for row in reader:
        tweets.append(cleaning(row[3].decode('utf-8')))
