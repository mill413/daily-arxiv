from datetime import date as dt
from typing import Self

from arxiv import Result


class Paper:
    def __init__(self,
                 date: dt,
                 title: str,
                 authors: list[Result.Author],
                 id: str,
                 url: str,
                 code_link: str | None) -> None:
        self.date: dt = date
        self.title: str = title
        self.authors: str = f"{authors[0].name} et al." if len(
            authors) > 1 else authors[0].name
        self.id: str = id
        self.url: str = url,
        self.code: str = code_link

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
