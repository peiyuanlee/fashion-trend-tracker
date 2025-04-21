import praw
import re
from nltk.corpus import stopwords
from collections import Counter
from dotenv import load_dotenv
import os

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)

SUBREDDITS = ['femalefashionadvice', 'malefashionadvice', 'streetwear']
LIMIT = 200 

def pull_from_reddit():
    all_titles = []
    for sub in SUBREDDITS:
        subreddit = reddit.subreddit(sub)
        posts = subreddit.new(limit = LIMIT)
        titles = [post.title.lower() for post in posts]
        all_titles.extend(titles)

    words = []
    for title in all_titles:
        title_words = re.findall(r'\b\w+\b', title)
        words.extend(title_words)

    stopword = stopwords.words('english')
    stopword.extend(['fashion', 'clothing', 'buy', 'shirts', 'shirt',
                       'fragrance', 'makeup', 'hair', 'fitness', 'dress', 'dresses', 'help', 'need', 'pants',
                       'suit', 'today', 'quality', 'look', 'general', 'wear', 'questions', 'fit', 'thread', '2025', 'thoughts',
                       'random', 'love', '18', '16'])
    cleaned_words = [word for word in words if word not in stopword]
    count = Counter((cleaned_words))
    return count.most_common(50)

if __name__ == "__main__":
    keywords = pull_from_reddit()
    print("Top keywords:")
    for word, count in keywords:
        print(f"{word}: {count}")

