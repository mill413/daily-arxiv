import tomllib
from Paper import Paper
import arxiv

from utils import parse_papers, content_to_md

# load config from file
with open("config.toml", "rb") as f:
    config = tomllib.load(f)

# get papers from arxiv via arxiv api
client = arxiv.Client(delay_seconds=3, num_retries=5)

content: dict[str, list[Paper]] = {}
for k in config["keywords"]:
    topic = k["topic"]
    content[topic] = []
    for query in k["filters"]:
        content[topic].extend(parse_papers(client.results(arxiv.Search(
            query=query,
            max_results=config["max_results"],
            sort_by=arxiv.SortCriterion.SubmittedDate
        ))))
    
    list(set(content[topic])).sort

# write papers of each topic to markdown
content_to_md(content)
