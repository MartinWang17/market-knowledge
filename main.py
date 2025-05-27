import os
from dotenv import load_dotenv
from supabase import create_client, Client
from reddit_scraper import RedditScraper

load_dotenv()

supabase_url = os.getenv("SUPABASE_PROJECT_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(supabase_url, supabase_key)
scraper = RedditScraper()

def save_post_to_supabase(title, body, link, upvotes):
    """Saves a Reddit post to Supabase. Returns nothing."""
    data = {
        "title": title,
        "body": body,
        "link": link,
        "upvotes": upvotes,
    }
    supabase.table("reddit_posts").insert(data).execute()

top_posts = scraper.fetch_top_posts("cats", limit=100)
for post in top_posts:
    save_post_to_supabase(
        title=post["title"],
        body=post["body"],
        link=post["link"],
        upvotes=post["upvotes"],
        )
