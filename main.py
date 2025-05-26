import os
from dotenv import load_dotenv
import praw
import html



load_dotenv()

client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
user_agent = os.getenv("REDDIT_USER_AGENT")
username = os.getenv("REDDIT_USER_NAME")
password = os.getenv("REDDIT_USER_PASSWORD")



reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
)

print("Fetching top posts from r/OnePiece...")
for submission in reddit.subreddit("OnePiece").top(limit=100):
    cleaned_title = html.unescape(submission.title)
    cleaned_text = html.unescape(submission.selftext)
    print("Title", cleaned_title)
    print("Body:", cleaned_text)
    print("Link:", submission.url)
    print("------------END POST------------")