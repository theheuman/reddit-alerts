from dataclasses import dataclass
import json
from urllib.parse import urlparse
from cloud_src.redditpostalert import RedditPostAlert


def get_domain(url: str):
    parsed_uri = urlparse(url)
    return "{uri.netloc}".format(uri=parsed_uri)


@dataclass()
class RedditPost:
    title: str
    link: str
    flair: str
    id: str
    external_link: str

    def __str__(self):
        return (
            "title: "
            + self.title
            + "\nlink: "
            + self.link
            + "\nflair: "
            + self.flair
            + "\nid: "
            + self.id
            + "\nexternal_link: "
            + self.external_link
        )

    def matches(self, reddit_post_alert: RedditPostAlert) -> bool:
        for post_filter in reddit_post_alert.title_filters:
            if not post_filter.match(self.title):
                return False
        for post_filter in reddit_post_alert.flair_filters:
            if not post_filter.match(self.flair):
                return False
        for post_filter in reddit_post_alert.domain_filters:
            if not post_filter.match(get_domain(self.external_link)):
                return False
        return True

    def __json__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    @classmethod
    def __from_file__(cls, json_as_string: str):
        json_data = json.loads(json_as_string)
        return RedditPost(
            json_data["title"],
            json_data["link"],
            json_data["flair"],
            json_data["id"],
            json_data["external_link"],
        )

    @classmethod
    def __from_web__(cls, json_data: dict):
        return RedditPost(
            json_data["title"],
            json_data["permalink"],
            json_data["link_flair_text"],
            json_data["id"],
            json_data["url_overridden_by_dest"],
        )

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return (self.id, self.link) == (other.id, other.link)
