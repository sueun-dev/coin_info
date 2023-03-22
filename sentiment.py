from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Load model and tokenizer
roberta = "cardiffnlp/twitter-roberta-base-sentiment"
model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

# Define labels
labels = ['Negative', 'Neutral', 'Positive']

sid = SentimentIntensityAnalyzer()

def preprocess_tweet(tweet):
    return ' '.join(['@user' if word.startswith('@') and len(word) > 1 else
                     'http' if word.startswith('http') else word
                     for word in tweet.split()])

def get_sentiment(tweet):
    tweet_proc = preprocess_tweet(tweet)
    encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')
    output = model(**encoded_tweet)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    if scores.max() > 0.5:
        label = labels[scores.argmax()]
    else:
        label = 'Undefined'

    return label