import string
import csv
import io
import pickle
import re
import matplotlib.pyplot as plt
import pandas as pd
#import nltk #run once to install
from nltk.corpus import stopwords
#nltk.download('stopwords') #run once to install
from nltk.tokenize import sent_tokenize, word_tokenize
#nltk.download('punkt') #run once to install
from nltk.stem import PorterStemmer
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer

def stemming(w):
    ps = PorterStemmer()
    return ps.stem(w)

def cleaning(s):
    s = re.sub(r"(?:\@|http)\S+", "", s) #removing urls and mentions
    s = s.lower() #lowercase the current tweet
    for char in string.punctuation:
        s = s.replace(char, '')
    cleared_string = ""
    word_tokens = word_tokenize(s) 
    for word in word_tokens:
        if word not in stopwords.words('english') and all(ord(char) < 128 for char in word):
                cleared_string += stemming(word) #not for wordclouds
                #cleared_string += word
                cleared_string += ' '
    return cleared_string

def generate_wc(x, name):
    curr_wc = WordCloud(width = 800, height = 800, background_color = 'white', stopwords = stopwords.words('english'), min_font_size = 10).generate(x)
    plt.figure(figsize = [8, 8])
    plt.imshow(curr_wc, interpolation="bilinear")
    plt.axis("off")
    name = 'wordclouds/' + name + '.png'
    plt.savefig(name, format="png")

tweets = []
pos_tweets = []
neg_tweets = []
neu_tweets = []
i=0
print("Clearing tweets...")
with open('../twitter_data/train2017.tsv') as input_file:
    reader = csv.reader(input_file, delimiter='\t')
    for row in reader:
        cleaned_tweet = cleaning(row[3])
        tweets.append(cleaned_tweet)
        if row[2] == "positive":
            pos_tweets.append(cleaned_tweet)
        elif row[2] == "negative":
            neg_tweets.append(cleaned_tweet)
        else: #if neutral
            neu_tweets.append(cleaned_tweet)
print("Done\n")

print("Generating WordClouds...")
generate_wc((" ").join(tweets), "tweets_wordcloud")
generate_wc((" ").join(pos_tweets), "pos_tweets_wordcloud")
generate_wc((" ").join(neg_tweets), "neg_tweets_wordcloud")
generate_wc((" ").join(neu_tweets), "neu_tweets_wordcloud")
print("Done\n")

#VECTORIZATION WITH BOW
vectorizer = CountVectorizer() 
X = vectorizer.fit_transform(tweets)
#print(vectorizer.get_feature_names())
#print(X.toarray())

output = open('myfile.pkl', 'wb')
pickle.dump(X, output)
output.close()

#VECTORIZATION WITH TF-idf
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer() 
tfidf = tfidf_vectorizer.fit_transform(tweets)
print(tfidf.shape)
