import requests
from bs4 import BeautifulSoup
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

from utils import summarise, get_headfi_reviews, save_wordcloud

temp_webpage = "https://www.head-fi.org/showcase/sennheiser-x-massdrop-hd-6xx.22019/reviews"

# Get reviews
reviews = get_headfi_reviews(temp_webpage)
for review in reviews:
    summary = summarise(review)
    # if len(summary) > 1000:
    #     summary = summarise(summary)
    print(summary)
    print("*"*50)
    save_wordcloud("sads", review)


