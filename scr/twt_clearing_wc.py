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
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

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
        if word not in stopwords.words('english') and \
            not word.startswith("http://") and \
            not word.startswith("@") and \
            all(ord(char) < 128 for char in word):
                #cleared_string += stemming(word) #not for wordclouds
                cleared_string += word
                cleared_string += ' '
    return cleared_string

tweets = ''
pos_tweets = ''
neg_tweets = ''
neu_tweets = ''

print "Clearing tweets..."
with open('../twitter_data/train2017.tsv') as input_file:
    reader = csv.reader(input_file, delimiter='\t')
    for row in reader:
        cleaned_tweet = cleaning(row[3].decode('utf-8'))
        tweets += cleaned_tweet
        if row[2] == "positive":
            pos_tweets+=cleaned_tweet
        elif row[2] == "negative":
            neg_tweets+=cleaned_tweet
        else: #if neutral
            neu_tweets+=cleaned_tweet
print "Done\n"

print "Generating WordClouds..."

gen_wc = WordCloud(width = 800, height = 800, background_color = 'white', stopwords = stopwords.words('english'), min_font_size = 10).generate(tweets)
plt.figure(figsize = [8, 8])
plt.imshow(gen_wc, interpolation="bilinear")
plt.axis("off")
plt.savefig("wordclouds/tweets_wordcloud.png", format="png")

pos_wc = WordCloud(width = 800, height = 800, background_color = 'white', stopwords = stopwords.words('english'), min_font_size = 10).generate(pos_tweets)
plt.figure(figsize = [8, 8])
plt.imshow(pos_wc, interpolation="bilinear")
plt.axis("off")
plt.savefig("wordclouds/pos_tweets_wordcloud.png", format="png")

neg_wc = WordCloud(width = 800, height = 800, background_color = 'white', stopwords = stopwords.words('english'), min_font_size = 10).generate(neg_tweets)
plt.figure(figsize = [8, 8])
plt.imshow(neg_wc, interpolation="bilinear")
plt.axis("off")
plt.savefig("wordclouds/neg_tweets_wordcloud.png", format="png")

neu_wc = WordCloud(width = 800, height = 800, background_color = 'white', stopwords = stopwords.words('english'), min_font_size = 10).generate(neu_tweets)
plt.figure(figsize = [8, 8])
plt.imshow(neu_wc, interpolation="bilinear")
plt.axis("off")
plt.savefig("wordclouds/neu_tweets_wordcloud.png", format="png")

print "Done\n"