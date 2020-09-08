import requests
from typing import List
from src import file_manipulation
from src.reddit_post import RedditPost


def get_url(subreddit):
    return "https://www.reddit.com/r/" + subreddit + "/new.json"


LAST_KNOWN_POST_FILE_NAME = "src/last_post.json"
SUBREDDIT = "buildapcsales"
URL = get_url(SUBREDDIT)


def get_json_data(url):
    json_data = requests.get(url, headers={"User-agent": "build_a_pc_scraper.1"}).json()
    return json_data


def parse_posts_from_json(json_data):
    posts = []
    post_dicts = json_data["data"]["children"]
    for post_dict in post_dicts:
        posts.append(RedditPost.__from_web__(post_dict["data"]))
    return posts


def get_new_posts(posts: List[RedditPost], last_known_post: RedditPost):
    try:
        new_posts = posts[: posts.index(last_known_post)]
        file_manipulation.update_last_known_post(LAST_KNOWN_POST_FILE_NAME, posts[0])
    except ValueError:
        # TODO throw error saying we cant find last post
        raise ValueError("Couldn't find last know post in passed posts list")
    return new_posts


def get_last_known_post(file_name: str):
    return file_manipulation.get_last_known_post(file_name)


def get_fresh_posts():
    json_data = get_json_data(URL)
    all_posts = parse_posts_from_json(json_data)
    last_known_post = get_last_known_post(LAST_KNOWN_POST_FILE_NAME)
    new_posts = get_new_posts(all_posts, last_known_post)
    for post in new_posts:
        print(post)
