from src.reddit_api_handler import get_fresh_posts
from src.reddit_post import RedditPost
from src.filter import Filter


LAST_KNOWN_POST_FILE_NAME = "src/last_post.json"
mock_filter = Filter("x570", "MOTHERBOARD", "")


def send_notification(post: RedditPost) -> bool:
    notification = {
        "message": "New Reddit Post",
        "text": post.title,
        "link": "https://www.reddit.com" + post.link,
    }
    print(notification)
    return True


def matches_filter(post: RedditPost) -> bool:
    if mock_filter.matches(post):
        return True
    return False


def main():
    fresh_posts = get_fresh_posts(LAST_KNOWN_POST_FILE_NAME)
    for post in fresh_posts:
        if matches_filter(post):
            send_notification(post)
    print("Found this many new posts: " + str(len(fresh_posts)))


if __name__ == "__main__":
    main()
