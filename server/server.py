from concurrent.futures import thread
import uuid
from flask import Flask
from flask import jsonify
from flask import send_from_directory
from flask import Blueprint
from flask_cors import CORS, cross_origin
from utils import get_headfi_reviews, summarise, calculate_sentiment, save_wordcloud

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/data/<name>")
@cross_origin()
def get_summaries(name=None):
    print("Summarising: "+name)
    url = "https://www.head-fi.org/showcase/{}/reviews".format(name)
    reviews = get_headfi_reviews(url)
    summaries = []
    for review in reviews:
        summary = summarise(review)
        # if(len(summary) > 3500):
        #     summary = summarise(summary)
        sentiment = calculate_sentiment(summary)
        wordcloud_name = uuid.uuid4().hex
        save_wordcloud(wordcloud_name, review)
        summaries.append({
            "summary": summary,
            "sentiment": sentiment,
            "wordcloud": wordcloud_name+".png",
        })
    return jsonify(summaries)

@app.route('/wordclouds/<name>')
@cross_origin()
def send_report(name=None):
    return send_from_directory('wordclouds', name)


if __name__ == '__main__':
    app.run(threaded=False, host='0.0.0.0', port=80)

