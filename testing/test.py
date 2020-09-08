import unittest
import jsonpickle
import requests
from reddit_post import RedditPost
import file_manipulation
import query_reddit_posts
from typing import List


def get_mock_posts_from_file(file_name: str) -> List[RedditPost]:
    with open("testing/input.json", 'r') as file:
        content = file.read()
    post_dicts = jsonpickle.decode(content)
    posts = []
    for post in post_dicts:
        posts.append(RedditPost(post['title'], post['link'], post['flair'], post['id'], post['external_link']))
    return posts


MOCK_POSTS = get_mock_posts_from_file("input.json")


class TestRedditPost(unittest.TestCase):
    mock_post = MOCK_POSTS[4]

    def test_str(self):
        mock_post_string_value = (
            "title: [PREBUILT] Acer Aspire Desktop: i5-10400, 12GB DDR4, 512GB SSD, Win 10 - $499.17" +
            "\nlink: /r/buildapcsales/comments/iocyre/prebuilt_acer_aspire_desktop_i510400_12gb_ddr4/" +
            "\nflair: Prebuilt" +
            "\nid: iocyre" +
            "\nexternal_link: https://www.amazon.com/gp/product/B088X2YR3X"
        )
        self.assertEqual(self.mock_post.__str__(), mock_post_string_value)

    def test_json(self):
        mock_post_json_value = (
            '{' +
            '\n  "title": "[PREBUILT] Acer Aspire Desktop: i5-10400, 12GB DDR4, 512GB SSD, Win 10 - $499.17",' +
            '\n  "link": "/r/buildapcsales/comments/iocyre/prebuilt_acer_aspire_desktop_i510400_12gb_ddr4/",' +
            '\n  "flair": "Prebuilt",' +
            '\n  "id": "iocyre",' +
            '\n  "external_link": "https://www.amazon.com/gp/product/B088X2YR3X"' +
            '\n}'
        )

        self.assertEqual(self.mock_post.__json__(), mock_post_json_value)

    def test_eq(self):
        mock_post_equal = RedditPost(
            "[PREBUILT] Acer Aspire Desktop: i5-10400, 12GB DDR4, 512GB SSD, Win 10 - $499.17",
            "/r/buildapcsales/comments/iocyre/prebuilt_acer_aspire_desktop_i510400_12gb_ddr4/",
            "Prebuilt",
            "iocyre",
            "https://www.amazon.com/gp/product/B088X2YR3X"
        )

        mock_post_not_equal = RedditPost(
            "The Title",
            "The Link",
            "The Flair",
            "The different ID",
            "The External Link",
        )
        self.assertTrue(self.mock_post.__eq__(mock_post_equal))
        self.assertFalse(self.mock_post.__eq__(mock_post_not_equal))
        self.assertEqual(self.mock_post.__eq__("Hello"), NotImplemented)

    def test_from_json_self(self):
        mock_post_json_value = (
            '{' +
            '\n  "title": "[PREBUILT] Acer Aspire Desktop: i5-10400, 12GB DDR4, 512GB SSD, Win 10 - $499.17",' +
            '\n  "link": "/r/buildapcsales/comments/iocyre/prebuilt_acer_aspire_desktop_i510400_12gb_ddr4/",' +
            '\n  "flair": "Prebuilt",' +
            '\n  "id": "iocyre",' +
            '\n  "external_link": "https://www.amazon.com/gp/product/B088X2YR3X"' +
            '\n}'
        )
        self.assertEqual(RedditPost.__from_file__(mock_post_json_value), self.mock_post)


class TestFileManipulation(unittest.TestCase):
    mock_post = RedditPost(
        "The Title", "The Link", "The Flair", "The ID", "The External Link"
    )
    output_file_name = "testing/output.json"

    def test_read_and_write(self):
        file_manipulation.update_last_known_post(self.output_file_name, self.mock_post)
        self.assertEqual(
            self.mock_post, file_manipulation.get_last_known_post(self.output_file_name)
        )


class TestQueryReddit(unittest.TestCase):

    test_url = "https://www.reddit.com/r/buildapcsales/new.json"

    def test_get_url(self):
        subreddit = "buildapcsales"
        self.assertEqual(self.test_url, query_reddit_posts.get_url(subreddit))

    def test_get_json_data(self):
        json_data = query_reddit_posts.get_json_data(self.test_url)
        # this asserts both that the json data has the correct node formatting, and that there are 25 posts
        self.assertEqual(len(json_data['data']['children']), 25)

    @classmethod
    def get_json_data(cls):
        with open("testing/example.json") as file:
            content = file.read()
        return jsonpickle.decode(content)

    def test_parse_posts_from_json(self):
        json_data = self.get_json_data()
        all_posts = query_reddit_posts.parse_posts_from_json(json_data)
        # TODO a better test here
        self.assertEqual(len(all_posts), 25)

    def test_get_new_posts(self):
        posts_zero_through_three = query_reddit_posts.get_new_posts(MOCK_POSTS, MOCK_POSTS[4])
        self.assertEqual(posts_zero_through_three, MOCK_POSTS[:4])
        # we could use assertRaises here but I want to check that it throws my custom exception
        try:
            new_posts = query_reddit_posts.get_new_posts(MOCK_POSTS, RedditPost("", "", "", "", ""))
        except ValueError as e:
            self.assertEqual(e.__str__(), "Couldn't find last know post in passed posts list")

    def test_get_last_known_post(self):
        post_from_file = query_reddit_posts.get_last_known_post("testing/mock_last_known_post.json")
        mock_post = MOCK_POSTS[0]
        self.assertEqual(post_from_file, mock_post)
