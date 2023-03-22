import snscrape.modules.twitter as sntwitter
import pandas as pd
from bs4 import BeautifulSoup
import requests
from sentiment import get_sentiment, sid
import threading
import time

url = 'https://www.coindesk.com/tag/ether/'
prev_articles_list = [pd.DataFrame()]
prev_tweets_list = [pd.DataFrame()]
stop_event = threading.Event()  # create an event to signal that the thread should stop

def update_articles():
    global prev_articles_list
    while not stop_event.is_set():  # check the flag periodically
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('div', class_='article-cardstyles__AcTitle-q1x8lc-1')

        articles_data = []
        for article in articles[:20]:
            title_element = article.find('a', class_='card-title')
            content_element = article.find('span', class_='content-text')
            title = title_element.text.strip()
            content = content_element.text.strip()
            sentiment = sid.polarity_scores(content)

            sentiment_label = 'Neutral'
            if sentiment['compound'] > 0:
                sentiment_label = 'Positive'
            elif sentiment['compound'] < 0:
                sentiment_label = 'Negative'

            articles_data.append({
                'title': title,
                'content': content,
                'sentiment': sentiment_label
            })

        new_articles_df = pd.DataFrame(articles_data)
        if not new_articles_df.equals(prev_articles_list[-1]):
            prev_articles_list.append(new_articles_df)
        time.sleep(2)


def get_tweets(search_terms, num_tweets=50):
    # Define a list to store the tweets
    tweets_list = []

    # Create a query string for the search
    query = f'{search_terms} -filter:replies'

    # Use sntwitter to execute the search query
    tweets = sntwitter.TwitterSearchScraper(query).get_items()

    # Loop through the tweets and extract the data you want
    tweet_count = 0
    for tweet in tweets:
        if tweet_count >= num_tweets:
            break
        text = tweet.rawContent
        date = tweet.date
        username = tweet.user.username
        user_id = tweet.user.id

        sentiment = get_sentiment(text)

        # Add the data to the list of tweets
        tweets_list.append({
            'text': text, 
            'date': date, 
            'username': username, 
            'user_id': user_id,
            'sentiment': sentiment
        })

        tweet_count += 1

    # Convert the list of tweets to a pandas DataFrame
    df = pd.DataFrame(tweets_list)
    
    # Write the tweets to a text file
    filename = 'tweets.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            f.write(f'{row["text"]}\n')
        #    f.write(f'Date: {row["date"]}\n')
        #    f.write(f'Username: {row["username"]}\n')
        #    f.write(f'User ID: {row["user_id"]}\n')
        #    f.write('\n')

    return df

search_terms = ['elonmusk', 'VitalikButerin']
search_terms_input = []
lock = threading.Lock()

def update_tweets():
    global search_terms_input, search_terms, prev_tweets_list, stop_event
    while not stop_event.is_set():
        with lock:
            if search_terms_input:
                search_terms.clear()
                search_terms.extend(search_terms_input)
                search_terms_input.clear()
            local_search_terms = search_terms.copy()
        formatted_search_terms = '(' + ' OR '.join([f'from:{handle}' for handle in local_search_terms]) + ')'
        print(formatted_search_terms)
        new_tweets_df = get_tweets(formatted_search_terms)
        if not new_tweets_df.equals(prev_tweets_list[-1]):
            neg_num = len(new_tweets_df[new_tweets_df['sentiment'] == 'Negative'])
            neu_num = len(new_tweets_df[new_tweets_df['sentiment'] == 'Neutral'])
            pos_num = len(new_tweets_df[new_tweets_df['sentiment'] == 'Positive'])
            prev_tweets_list.append(new_tweets_df)
        time.sleep(1)
        
stop_event = threading.Event()  # Create a threading.Event object
tweets_thread = None

def start_new_thread():
    global tweets_thread, stop_event

    if tweets_thread is not None and tweets_thread.is_alive():
        stop_event.set()  # Signal the old thread to stop
        tweets_thread.join()  # Wait for the old thread to finish

    stop_event.clear()  # Reset the stop_event
    tweets_thread = threading.Thread(target=update_tweets)
    tweets_thread.start()

# start_new_thread()


