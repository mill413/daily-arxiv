from datetime import date
from arxiv import Result


class Paper:
    def __init__(self,
                 date: date,
                 title: str,
                 authors: list[Result.Author],
                 id: str,
                 url: str,
                 code_link: str | None) -> None:
        self.date: str = date.strftime("%Y/%m/%d")
        self.title: str = title
        self.authors: str = f"{authors[0].name} et al." if len(
            authors) > 1 else authors[0].name
        self.id: str = id
        self.url: str = url,
        self.code: str = code_link

    def __str__(self) -> str:
        return f"|**{self.date}**|**{self.title}**|{self.authors}|[{self.id}]({self.url})|**{f"[link]({self.code})" if self.code else "NULL"}**|"

    def __repr__(self) -> str:
        return str({
            "date": self.date,
            "title": self.title,
            "authors": self.authors,
            "id": self.id,
            "url": self.url,
            "code": self.code
        })
