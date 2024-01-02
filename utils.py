from datetime import (datetime, timezone, timedelta)
import logging
from typing import Generator
from Paper import Paper
from arxiv import Result

# For Github Actions logging time
logging.Formatter.converter = lambda sec,what:(datetime.now() + timedelta(hours=8)).timetuple()
logging.basicConfig(format="[%(asctime)s %(levelname)s] %(message)s",
                    datefmt="%Y/%m/%d %H:%M:%S",
                    level=logging.INFO)


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
            url=result.entry_id,
            code_link=None  # TODO-code url
        ))

    return papers


def content_to_md(content: dict):
    now = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(
        timezone(timedelta(hours=8))).strftime("%Y/%m/%d %H:%M:%S")

    front_matter = (
        "---",
        "layout: default",
        "---",
        ""
    )

    update_info = (
        f"> Updated on {now}",
        ""
    )

    toc = (
        "<summary>Table of Contents</summary>",
        "<ol>",
        '\n'.join([f" <li><a href=\"#{topic}\">{topic}</a></li>" for topic in list(content.keys())]),
        "</ol>",
        ""
    )

    with open("./index.md", "w") as f:
        f.write("\n".join(front_matter))
        f.write("\n"+"\n".join(update_info))
        f.write("\n"+"\n".join(toc))
        for topic, papers in content.items():
            heading = (
                f"## {topic}",
                ""
            )
            table = (
                "| Publish Date | Title | Authors | PDF | Code |",
                "|:-------------|:------|:--------|:----|:-----|",
                '\n'.join([str(paper) for paper in papers]),
                ""
            )
            f.write("\n"+"\n".join(heading))
            f.write("\n"+"\n".join(table))
