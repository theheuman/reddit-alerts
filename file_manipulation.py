from reddit_post import RedditPost
from typing import List
import json
import jsonpickle


def write_file(file_name: str, text: str):
    with open(file_name, "w") as file:
        file.write(text)


def read_file(file_name: str):
    with open(file_name, "r") as file:
        content = file.read()
    return content


def get_last_known_post(file_name: str) -> RedditPost:
    json_data = read_file(file_name)
    return RedditPost.__from_file__(json_data)


def update_last_known_post(file_name: str, post: RedditPost):
    write_file(file_name, post.__json__())


# used for initial test data
def write_all_posts(file_name: str, posts: List[RedditPost]):
    with open(file_name, "w") as file:
        file.write(jsonpickle.encode(posts, unpicklable=False, indent=2))
