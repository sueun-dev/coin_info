from flask import Flask, render_template, jsonify, request, redirect
import threading
from utils import *
from scraper import search_terms, start_new_thread

app = Flask(__name__)

articles_thread = threading.Thread(target=update_articles)
articles_thread.start()

@app.route('/')
def index():
    global prev_tweets_list
    tweets_df = prev_tweets_list[-1]
    tweets_data = tweets_df.to_dict(orient='records')
    return render_template('index.html', tweets_data=tweets_data)

@app.route('/tweets')
def tweets():
    global prev_tweets_list
    tweets_df = prev_tweets_list[-1]
    return jsonify(tweets_df.to_dict(orient='records'))

@app.route('/articles')
def articles():
    global prev_articles_list
    articles_df = prev_articles_list[-1]
    return jsonify(articles_df.to_dict(orient='records'))

@app.route('/add_user', methods=['POST'])
def add_user():
    global search_terms
    new_user = request.form['user']
    search_terms.append(new_user)
    start_new_thread()  # Call the start_new_thread function here
    return redirect('/')



if __name__ == '__main__':
    app.run()
