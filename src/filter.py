from dataclasses import dataclass


@dataclass()
class Filter:
    title: str
    flair: str
    domain: str
