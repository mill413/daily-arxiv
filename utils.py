import logging
import tomllib
from datetime import datetime, timedelta, timezone
from typing import Generator, Self

import requests
from arxiv import Result
from mdBuilder import MdBuilder
from mdElement import *

logging.basicConfig(format="[%(asctime)s %(levelname)s] %(message)s",
                    datefmt="%Y/%m/%d %H:%M:%S",
                    level=logging.INFO)

# load config from file
with open("config.toml", "rb") as f:
    config = tomllib.load(f)


class Paper:
    def __init__(self,
                 date: datetime,
                 title: str,
                 authors: list[Result.Author],
                 id: str,
                 url: str) -> None:
        self.date: datetime = date
        self.title: str = title
        self.authors: str = f"{authors[0].name} et al." if len(
            authors) > 1 else authors[0].name
        self.id: str = id
        self.url: str = url
        self.code: str | None = None

    def get_code_link(self):
        query_url = f"https://arxiv.paperswithcode.com/api/v0/papers/{self.id}"
        result = requests.get(query_url).json()
        if "official" in result and result["official"]:
            self.code = result["official"]["url"]
        else:
            self.code = None

    def __str__(self) -> str:
        return f"|**{self.date.strftime("%Y/%m/%d")}**|**{self.title}**|{self.authors}|[{self.id}]({self.url})|**{f"[link]({self.code})" if self.code else "NULL"}**|"

    def __repr__(self) -> str:
        return str({
            "date": self.date.strftime("%Y/%m/%d"),
            "title": self.title,
            "authors": self.authors,
            "id": self.id,
            "url": self.url,
            "code": self.code
        })

    def __lt__(self, other: Self) -> bool:
        return self.date < other.date

    def __gt__(self, other: Self) -> bool:
        return self.date > other.date

    def __eq__(self, other: Self) -> bool:
        return self.id == other.id


def log(message: str):
    logging.info(message)


def parse_papers(results: Generator[Result, None, None]) -> list[Paper]:

    papers = []

    for result in results:
        papers.append(Paper(
            date=result.published.date(),
            title=result.title,
            authors=result.authors,
            id=result.get_short_id(),
            url=result.entry_id
        ))

    return papers


def content_to_md(content: dict, file: str):
    now = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(
        timezone(timedelta(hours=8))).strftime("%Y/%m/%d %H:%M:%S")

    topic_block = []
    for topic, papers in content.items():
        topic_block.append(Heading(2, topic))
        topic_block.append(Table(
            header=["Publish Date", "Title", "Authors", "PDF", "Code"],
            content=[
                [Bold(paper.date.strftime("%Y/%m/%d")),
                 paper.title,
                 paper.authors,
                 Link(url=paper.url, text_or_image=paper.id),
                 Link(url=paper.code, text_or_image=Bold("link")) if paper.code else Bold("NULL")
                 ] for paper in papers
            ]
        ))

    MdBuilder(
        "---\nlayout: default\n---",
        Blockquote(f"Updated on {now}"),
        "<summary>Table of Contents</summary>",
        "<ol>",
        '\n'.join([
            f" <li><a href=\"#{topic}\">{topic}</a></li>"
            for topic in list(content.keys())]),
        "</ol>",
        topic_block
    ).write_to_file(file)
