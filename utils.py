import logging
import tomllib
from datetime import datetime, timedelta, timezone
from typing import Generator, Self

import requests
from arxiv import Result

# For Github Actions logging time
#logging.Formatter.converter = lambda sec, what: (
#    datetime.now() + timedelta(hours=8)).timetuple()
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
            url=result.entry_id  # TODO-code url
        ))

    return papers


def content_to_md(content: dict, file: str):
    now = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(
        timezone(timedelta(hours=8))).strftime("%Y/%m/%d %H:%M:%S")

    front_matter: list[str] = [
        "---",
        "layout: default",
        "---",
        ""
    ]

    update_info: list[str] = [
        f"> Updated on {now}",
        ""
    ]

    toc: list[str] = [
        "<summary>Table of Contents</summary>",
        "<ol>",
        '\n'.join([f" <li><a href=\"#{topic}\">{topic}</a></li>" for topic in list(content.keys())]),
        "</ol>",
        ""
    ]

    md_content: list[str] = [
        "\n".join(front_matter),
        "\n".join(update_info),
        "\n".join(toc),
    ]

    for topic, papers in content.items():
        heading: list[str] = [
            f"## {topic}",
            ""
        ]
        table: list[str] = [
            "| Publish Date | Title | Authors | PDF | Code |",
            "|:-------------|:------|:--------|:----|:-----|",
            '\n'.join([str(paper) for paper in papers]),
            ""
        ]
        md_content.append("\n".join(heading))
        md_content.append("\n".join(table))

    with open(file, "w") as f:
        f.write("\n".join(md_content))
