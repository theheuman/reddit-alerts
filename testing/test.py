import unittest
import jsonpickle
from typing import List
from src.reddit_post import RedditPost
from src.filter import Filter, SubFilter, Operator
from src import file_manipulation, reddit_api_handler
from src import notifier


def get_mock_posts_from_file(file_name: str) -> List[RedditPost]:
    file_manipulation.change_dir()
    with open("testing/input.json", "r") as file:
        content = file.read()
    post_dicts = jsonpickle.decode(content)
    posts = []
    for post in post_dicts:
        posts.append(
            RedditPost(
                post["title"],
                post["link"],
                post["flair"],
                post["id"],
                post["external_link"],
            )
        )
    return posts


MOCK_POSTS = get_mock_posts_from_file("input.json")


class TestRedditPost(unittest.TestCase):
    mock_post = MOCK_POSTS[4]

    def test_str(self):
        mock_post_string_value = (
            "title: [PREBUILT] Acer Aspire Desktop: i5-10400, 12GB DDR4, 512GB SSD, Win 10 - $499.17"
            + "\nlink: /r/buildapcsales/comments/iocyre/prebuilt_acer_aspire_desktop_i510400_12gb_ddr4/"
            + "\nflair: Prebuilt"
            + "\nid: iocyre"
            + "\nexternal_link: https://www.amazon.com/gp/product/B088X2YR3X"
        )
        self.assertEqual(self.mock_post.__str__(), mock_post_string_value)

    def test_json(self):
        mock_post_json_value = (
            "{"
            + '\n  "title": "[PREBUILT] Acer Aspire Desktop: i5-10400, 12GB DDR4, 512GB SSD, Win 10 - $499.17",'
            + '\n  "link": "/r/buildapcsales/comments/iocyre/prebuilt_acer_aspire_desktop_i510400_12gb_ddr4/",'
            + '\n  "flair": "Prebuilt",'
            + '\n  "id": "iocyre",'
            + '\n  "external_link": "https://www.amazon.com/gp/product/B088X2YR3X"'
            + "\n}"
        )

        self.assertEqual(self.mock_post.__json__(), mock_post_json_value)

    def test_eq(self):
        mock_post_equal = RedditPost(
            "[PREBUILT] Acer Aspire Desktop: i5-10400, 12GB DDR4, 512GB SSD, Win 10 - $499.17",
            "/r/buildapcsales/comments/iocyre/prebuilt_acer_aspire_desktop_i510400_12gb_ddr4/",
            "Prebuilt",
            "iocyre",
            "https://www.amazon.com/gp/product/B088X2YR3X",
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
            "{"
            + '\n  "title": "[PREBUILT] Acer Aspire Desktop: i5-10400, 12GB DDR4, 512GB SSD, Win 10 - $499.17",'
            + '\n  "link": "/r/buildapcsales/comments/iocyre/prebuilt_acer_aspire_desktop_i510400_12gb_ddr4/",'
            + '\n  "flair": "Prebuilt",'
            + '\n  "id": "iocyre",'
            + '\n  "external_link": "https://www.amazon.com/gp/product/B088X2YR3X"'
            + "\n}"
        )
        self.assertEqual(RedditPost.__from_file__(mock_post_json_value), self.mock_post)

    def test_match(self):
        # TODO consolidate sub filters into mock filters so we don't have so many mock filters
        mock_post = RedditPost(
            "[PREBUILT] Acer Aspire Desktop: i5-10400, 12GB DDR4, 512GB SSD, Win 10 - $499.17",
            "/r/buildapcsales/comments/iocyre/prebuilt_acer_aspire_desktop_i510400_12gb_ddr4/",
            "Prebuilt",
            "iocyre",
            "https://www.amazon.com/gp/product/B088X2YR3X",
        )
        sub_filter_empty = []
        sub_filter_no_match_in = [SubFilter(Operator.check_in, "No Match")]
        sub_filter_title_in = [SubFilter(Operator.check_in, "12GB")]
        sub_filter_flair_in = [SubFilter(Operator.check_in, "Prebuilt")]
        sub_filter_domain_in = [SubFilter(Operator.check_in, "amazon.com")]

        sub_filter_title_not_in = [SubFilter(Operator.check_not_in, "No Match")]
        sub_filter_title_not_in_fail = [SubFilter(Operator.check_not_in, "12GB")]
        sub_filter_title_equal = [
            SubFilter(
                Operator.check_equals,
                "[PREBUILT] Acer Aspire Desktop: i5-10400, 12GB DDR4, 512GB SSD, Win 10 - $499.17",
            )
        ]
        sub_filter_title_equal_fail = [SubFilter(Operator.check_equals, "No Match")]
        sub_filter_title_not_equal = [SubFilter(Operator.check_not_equals, "No Match")]
        sub_filter_title_not_equal_fail = [
            SubFilter(
                Operator.check_not_equals,
                "[PREBUILT] Acer Aspire Desktop: i5-10400, 12GB DDR4, 512GB SSD, Win 10 - $499.17",
            )
        ]
        sub_filter_no_operator = [SubFilter(None, "Doesn't matter")]

        mock_filter_all_match = Filter(
            "All match", sub_filter_title_in, sub_filter_flair_in, sub_filter_domain_in
        )
        mock_filter_title_no_match = Filter(
            "Title No Match",
            sub_filter_no_match_in,
            sub_filter_flair_in,
            sub_filter_domain_in,
        )
        mock_filter_title_empty = Filter(
            "Title Empty", sub_filter_empty, sub_filter_flair_in, sub_filter_domain_in
        )
        mock_filter_flair_no_match = Filter(
            "Flair No Match",
            sub_filter_empty,
            sub_filter_no_match_in,
            sub_filter_domain_in,
        )
        mock_filter_title_and_flair_empty = Filter(
            "Title, Flair Empty",
            sub_filter_empty,
            sub_filter_empty,
            sub_filter_domain_in,
        )
        mock_filter_domain_no_match = Filter(
            "Domain No Match",
            sub_filter_empty,
            sub_filter_empty,
            sub_filter_no_match_in,
        )

        mock_filter_title_not_in = Filter(
            "Title Not In", sub_filter_title_not_in, sub_filter_empty, sub_filter_empty
        )
        mock_filter_title_not_in_fail = Filter(
            "Title Not In Fail",
            sub_filter_title_not_in_fail,
            sub_filter_empty,
            sub_filter_empty,
        )
        mock_filter_title_equal = Filter(
            "Title Equal", sub_filter_title_equal, sub_filter_empty, sub_filter_empty
        )
        mock_filter_title_equal_fail = Filter(
            "Title Equal Fail",
            sub_filter_title_equal_fail,
            sub_filter_empty,
            sub_filter_empty,
        )
        mock_filter_title_not_equal = Filter(
            "Title Not Equal",
            sub_filter_title_not_equal,
            sub_filter_empty,
            sub_filter_empty,
        )
        mock_filter_title_not_equal_fail = Filter(
            "Title Not Equal Fail",
            sub_filter_title_not_equal_fail,
            sub_filter_empty,
            sub_filter_empty,
        )
        mock_filter_no_operator = Filter(
            "No Operator", sub_filter_no_operator, sub_filter_empty, sub_filter_empty
        )

        self.assertTrue(mock_post.matches(mock_filter_all_match))
        self.assertFalse(mock_post.matches(mock_filter_title_no_match))
        self.assertTrue(mock_post.matches(mock_filter_title_empty))
        self.assertFalse(mock_post.matches(mock_filter_flair_no_match))
        self.assertTrue(mock_post.matches(mock_filter_title_and_flair_empty))
        self.assertFalse(mock_post.matches(mock_filter_domain_no_match))

        self.assertTrue(mock_post.matches(mock_filter_title_not_in))
        self.assertFalse(mock_post.matches(mock_filter_title_not_in_fail))
        self.assertTrue(mock_post.matches(mock_filter_title_equal))
        self.assertFalse(mock_post.matches(mock_filter_title_equal_fail))
        self.assertTrue(mock_post.matches(mock_filter_title_not_equal))
        self.assertFalse(mock_post.matches(mock_filter_title_not_equal_fail))

        self.assertFalse(mock_post.matches(mock_filter_no_operator))


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
        self.assertEqual(self.test_url, reddit_api_handler.get_url(subreddit))

    def test_get_json_data(self):
        json_data = reddit_api_handler.get_json_data(self.test_url)
        # this asserts both that the json data has the correct node formatting, and that there are 25 posts
        self.assertEqual(len(json_data["data"]["children"]), 25)

    @classmethod
    def get_json_data(cls):
        with open("testing/example.json") as file:
            content = file.read()
        return jsonpickle.decode(content)

    def test_parse_posts_from_json(self):
        json_data = self.get_json_data()
        all_posts = reddit_api_handler.parse_posts_from_json(json_data)
        # TODO a better test here
        self.assertEqual(len(all_posts), 25)

    def test_get_new_posts(self):
        posts_zero_through_three = reddit_api_handler.get_new_posts(
            MOCK_POSTS, MOCK_POSTS[4]
        )
        self.assertEqual(posts_zero_through_three, MOCK_POSTS[:4])

        # we could use assertRaises here but I want to check that it throws my custom exception
        try:
            new_posts = reddit_api_handler.get_new_posts(
                MOCK_POSTS, RedditPost("", "", "", "", "")
            )
        except ValueError as e:
            self.assertEqual(
                e.__str__(), "Couldn't find last know post in passed posts list"
            )

    def test_get_last_known_post(self):
        mock_post = MOCK_POSTS[0]
        post_from_file = reddit_api_handler.get_last_known_post(
            "testing/mock_last_known_post.json", mock_post
        )
        self.assertEqual(post_from_file, mock_post)


class TestNotifier(unittest.TestCase):
    mock_post = RedditPost(
        "The Title", "The Link", "The Flair", "The ID", "The External Link"
    )

    def test_send_notification(self):
        self.assertTrue(notifier.send_notification(self.mock_post))

    def test_matches_filter(self):
        mock_post_does_match = RedditPost("x570", "", "MOTHERBOARD", "", "")

        self.assertFalse(notifier.matches_filter(self.mock_post))
        self.assertTrue(notifier.matches_filter(mock_post_does_match))
