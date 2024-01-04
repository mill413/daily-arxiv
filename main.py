import tomllib
from Paper import Paper
import arxiv

from utils import parse_papers, content_to_md

# load config from file
with open("config.toml", "rb") as f:
    config = tomllib.load(f)

max_results = config["max_results"]

# get papers from arxiv via arxiv api
client = arxiv.Client()

content: dict[str, list[Paper]] = {}
for k in config["keywords"]:
    topic: str = k["topic"]
    content[topic] = []
    for query in k["filters"]:
        content[topic].extend(parse_papers(client.results(arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        ))))
    
    assert len(content[topic]) > 0, f"content{topic} empty"

    content[topic].sort(reverse=True)
    content[topic] = content[topic][0:max_results]

# write papers of each topic to markdown
content_to_md(content)
