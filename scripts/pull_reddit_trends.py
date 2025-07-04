import praw
import re
import os
from dotenv import load_dotenv
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)

SUBREDDITS = ['femalefashionadvice', 'malefashionadvice', 'streetwear']
LIMIT = 200

EXTRA_STOPWORDS = set([
    'fashion', 'clothing', 'buy', 'shirt', 'shirts', 'pants', 'suit',
    'fragrance', 'makeup', 'hair', 'fitness', 'help', 'need', 'today',
    'quality', 'look', 'wear', 'fit', 'thread', 'thoughts', 'random',
    'love', 'general', 'question', 'questions', 'january', 'february', 'march',
    'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 
    'recent', 'feedback', 'id', 'skincare', 'waywt', 'favorite', 'brand'
])

def pull_from_reddit_phrases():
    all_titles = []

    for sub in SUBREDDITS:
        subreddit = reddit.subreddit(sub)
        posts = subreddit.new(limit=LIMIT)
        titles = [post.title.lower() for post in posts]
        all_titles.extend(titles)

    cleaned_titles = [re.sub(r'\d+', '', title) for title in all_titles]

    vectorizer = CountVectorizer(
        stop_words=stopwords.words('english') + list(EXTRA_STOPWORDS),
        ngram_range=(2, 3)
    )
    X = vectorizer.fit_transform(cleaned_titles)

    phrase_counts = X.sum(axis=0)
    phrases = [(phrase, int(phrase_counts[0, idx])) for phrase, idx in vectorizer.vocabulary_.items()]
    sorted_phrases = sorted(phrases, key=lambda x: x[1], reverse=True)

    return sorted_phrases[:50]

if __name__ == "__main__":
    phrases = pull_from_reddit_phrases()
    print("Top fashion phrases:")
    for phrase, count in phrases:
        print(f"{phrase}: {count}")
