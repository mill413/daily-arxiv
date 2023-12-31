import datetime as dt
import logging
from typing import Generator
from Paper import Paper
from arxiv import Result

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
    now = dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc).astimezone(
        dt.timezone(dt.timedelta(hours=8))).strftime("%Y/%m/%d %H:%M:%S")

    layout_str = """---
layout: default
---"""

    update_str = f"> Updated on {now}"

    toc_str = f"""<summary>Table of Contents</summary>
<ol>
{'\n'.join([f"<li><a href=\"#{topic}\">{topic}</a></li>" for topic in list(content.keys())])}
</ol>
"""

    tables = ""
    header = """| Publish Date | Title | Authors | PDF | Code |
|:-------------|:------|:--------|:----|:-----|"""

    for topic, papers in content.items():
        tables += f"""## {topic}

{header}
{'\n'.join([str(paper) for paper in papers])}

"""

    with open("./index.md", "w") as f:
        f.write(layout_str+"\n\n")
        f.write(update_str+"\n\n")
        f.write(toc_str+"\n")
        f.write(tables)
