import os
from dotenv import load_dotenv
import praw

load_dotenv()

print("CLIENT_ID:", os.getenv("REDDIT_CLIENT_ID"))
print("CLIENT_SECRET:", os.getenv("REDDIT_CLIENT_SECRET"))
print("USER_AGENT:", os.getenv("REDDIT_USER_AGENT"))

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

print("Attempting to access subreddit...")
try:
    for submission in reddit.subreddit("cats").hot(limit=3):
        print(submission.title)
except Exception as e:
    print("Exception:", e)
    print(os.getenv("REDDIT_CLIENT_ID"))
    print(os.getenv("REDDIT_CLIENT_SECRET"))
    print(os.getenv("REDDIT_USER_AGENT"))