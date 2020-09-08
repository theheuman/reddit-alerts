from dataclasses import dataclass
import json
from urllib.parse import urlparse
from src.reddit_post import RedditPost


def get_domain(url: str):
    parsed_uri = urlparse(url)
    return "{uri.netloc}".format(uri=parsed_uri)


@dataclass()
class Filter:
    title: str
    flair: str
    domain: str

    def matches(self, post: RedditPost) -> bool:
        if self.title and self.title.upper() not in post.title.upper():
            return False
        if self.flair and self.flair.upper() != post.flair.upper():
            return False
        if (
            self.domain
            and self.domain.upper() not in get_domain(post.external_link).upper()
        ):
            return False
        return True
