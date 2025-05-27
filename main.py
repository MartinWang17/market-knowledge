import os
from dotenv import load_dotenv
import praw
import html
from supabase import create_client, Client



load_dotenv()

client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
user_agent = os.getenv("REDDIT_USER_AGENT")
username = os.getenv("REDDIT_USER_NAME")
password = os.getenv("REDDIT_USER_PASSWORD")
supabase_url = os.getenv("SUPABASE_PROJECT_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(supabase_url, supabase_key)


reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
)

def save_post_to_supabase(title, body, link, upvotes):
    """Saves a Reddit post to Supabase. Returns nothing."""
    data = {
        "title": title,
        "body": body,
        "link": link,
        "upvotes": upvotes,
    }
    supabase.table("reddit_posts").insert(data).execute()

print("Fetching top posts from r/OnePiece...")

posts = list(reddit.subreddit("OnePiece").top(limit=10))
# Sort posts by score in descending order using anonymous func by getting hold of each post's score (item)
posts_sorted = sorted(posts, key=lambda item: item.score, reverse=True)

for submission in posts_sorted:

    cleaned_title = html.unescape(submission.title)
    cleaned_text = html.unescape(submission.selftext)
    link = f"https://reddit.com{submission.permalink}"
    upvotes = submission.score

    print("------------START POST------------")
    print("Title", cleaned_title)
    print("Body:", cleaned_text)
    print("Link:", link)
    print("Upvotes:", upvotes)
    print("------------END POST------------")

    save_post_to_supabase(title=cleaned_title, body=cleaned_text, link=link, upvotes=upvotes)
