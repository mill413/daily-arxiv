import arxiv

from utils import Paper, config, content_to_md, log, parse_papers, concat_filters

max_results = config["max_results"]

# get papers from arxiv via arxiv api
client = arxiv.Client()

content: dict[str, list[Paper]] = {}
for k in config["topics"]:
    topic: str = k["name"]

    log(f"Query topic {topic}")
    content[topic] = parse_papers(client.results(arxiv.Search(
        query=concat_filters(k["filters"]),
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )))
    content[topic].sort(reverse=True)

    assert len(content[topic]) > 0, f"Content of {topic} empty"

    log(f"Get code link of {topic}")
    for paper in content[topic]:
        paper.get_code_link()

# write papers of each topic to markdown
content_to_md(content, config["file_path"])
