from dataclasses import dataclass
from enum import Enum
from typing import List


@dataclass()
class Operator(Enum):
    check_in = "Check if string is IN post"
    check_not_in = "Check if string is NOT IN post"
    check_equals = "Check that the string is exact match (case insensitive)"
    check_not_equals = "Match anything that this string is not (case insensitive)"


@dataclass()
class PostFilter:
    operator: Operator
    text: str

    def match(self, post_text: str):
        if not self.operator:
            return False
        elif self.operator.name == Operator.check_in.name:
            return self.text.upper() in post_text.upper()
        elif self.operator.name == Operator.check_not_in.name:
            return self.text.upper() not in post_text.upper()
        elif self.operator.name == Operator.check_equals.name:
            return self.text.upper().__eq__(post_text.upper())
        else:
            return not self.text.upper().__eq__(post_text.upper())


@dataclass()
class RedditPostAlert:
    name: str
    title_filters: List[PostFilter]
    flair_filters: List[PostFilter]
    domain_filters: List[PostFilter]
