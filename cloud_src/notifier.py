from cloud_src.reddit_api_handler import get_fresh_posts
from cloud_src.reddit_post import RedditPost
from cloud_src.redditpostalert import RedditPostAlert, PostFilter, Operator


LAST_KNOWN_POST_FILE_NAME = "cloud_src/last_post.json"
sub_filter_1 = PostFilter(Operator.check_in, "x570")
sub_filter_2 = PostFilter(Operator.check_in, "MOTHERBOARD")
mock_filter = RedditPostAlert("Mock Filter", [sub_filter_1], [sub_filter_2], [])


def send_notification(post: RedditPost) -> bool:
    notification = {
        "message": "New Reddit Post",
        "text": post.title,
        "link": "https://www.reddit.com" + post.link,
    }
    print(notification)
    return True


def matches_filter(post: RedditPost) -> bool:
    if post.matches(mock_filter):
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
