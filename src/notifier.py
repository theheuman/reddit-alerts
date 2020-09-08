from src.reddit_api_handler import get_fresh_posts
from src.reddit_post import RedditPost


def send_notification(post: RedditPost) -> bool:
    notification = {
        "message": "New Reddit Post",
        "text": post.title,
        "link": "https://www.reddit.com" + post.link,
    }
    print(notification)
    return True


def matches_filter(post: RedditPost) -> bool:
    if post:
        return True
    return False


def main():
    fresh_posts = get_fresh_posts()
    for post in fresh_posts:
        if matches_filter(post):
            send_notification(post)


if __name__ == "__main__":
    main()
