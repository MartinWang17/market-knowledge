import os
from dotenv import load_dotenv
import praw
import html
from prawcore.exceptions import Forbidden

load_dotenv()

class RedditScraper:

    def __init__(self):
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.user_agent = os.getenv("REDDIT_USER_AGENT")
        self.username = os.getenv("REDDIT_USER_NAME")
        self.password = os.getenv("REDDIT_USER_PASSWORD")

        self.reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
            )
        
    def fetch_top_posts(self, subreddit_name, limit=10):
        """
        Takes a subreddit name and an optional limit (default is 10). NOTE: subreddit_name should not include the 'r/' prefix,
        it should be just the name of the subreddit.
        
        Fetches top posts from a given subreddit and returns a json containing data of the posts including:
        title, body, link, and upvotes.
        """
        try:
            # Check if the subreddit exists
            self.reddit.subreddit(subreddit_name).display_name
        except Forbidden:
            print(f"Error: The subreddit '{subreddit_name}' does not exist or is private.")
            return []
        except Exception as e:
            print(f"An error occurred while accessing the subreddit: {e}")
            return []
        else: 
            subreddit = self.reddit.subreddit(subreddit_name).top(limit=limit)
            posts = list(subreddit)
            # Sort posts by score in descending order using anonymous func by getting hold of each post's score (item)
            posts_sorted = sorted(posts, key=lambda item: item.score, reverse=True)

            posts_data = [] 
            for submission in posts_sorted:

                cleaned_title = html.unescape(submission.title)
                cleaned_text = html.unescape(submission.selftext)
                link = f"https://reddit.com{submission.permalink}"
                upvotes = submission.score
                print(f"fetching posts from subreddit: {subreddit_name}...\n")


                print("------------START POST------------")
                print("Title", cleaned_title)
                print("Body:", cleaned_text)
                print("Link:", link)
                print("Upvotes:", upvotes)
                print("------------END POST------------")
                post_data = {
                    "title": cleaned_title,
                    "body": cleaned_text,
                    "link": link,
                    "upvotes": upvotes
                }
                posts_data.append(
                    post_data
                )
            return posts_data
            



