import re
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('punkt')

def get_headfi_reviews(url: str) -> list:
    req = requests.get(url)

    soup = BeautifulSoup(req.content, 'lxml')

    reviews_soup = soup.find_all("div", {"class": "message-content"})

    reviews = []
    for review_soup in reviews_soup:
        user_content = review_soup.find("div", {"class": "message-userContent"}).text.strip()
        reviews.append(user_content)
    return reviews


def summarise(text: str) -> str:
    """
    Summarise the text.
    """

    text = re.sub("[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)", "", text)
    text = re.sub("(?!\d)\.(?!\d)(?!\s)", ". ", text)
    # text = re.sub("\.\n+", ". ", text)
    # text = re.sub("\n+", ". ", text)
    

    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)

    freq_table = dict()
    for word in words:
        word = word.lower()
        if word in stop_words:
            continue
        if word in freq_table:
            freq_table[word] += 1
        else:
            freq_table[word] = 1

    sentences = []
    sentences_tokenized = sent_tokenize(text)
    for i in range(0, len(sentences_tokenized)):
        sentences = sentences + sentences_tokenized[i].split("\n")
    
    sentence_value = dict()

    for sentence in sentences:
        for word, freq in freq_table.items():
            if word in sentence.lower():
                if sentence in sentence_value:
                    sentence_value[sentence] += freq
                else:
                    sentence_value[sentence] = freq

    sum_values = 0
    for sentence in sentence_value:
        sum_values += sentence_value[sentence]

    average = int(sum_values/len(sentences))


    summary = ''
    for sentence in sentences:
        if (sentence in sentence_value) and (sentence_value[sentence] > (1.5*average)):
            summary += " "+sentence
    return summary.strip()

def calculate_sentiment(text: str) -> float:
    """
    Calculate sentiment of text.
    """
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(text)
    return ss['compound']

def save_wordcloud(name: str, text: str):
    wordcloud = WordCloud(width = 800, height = 800,
				background_color ='white',
				stopwords = set(STOPWORDS),
				min_font_size = 10).generate(text.lower())
    
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.savefig("wordclouds/"+name+".png", dpi = 300)
    plt.close()
