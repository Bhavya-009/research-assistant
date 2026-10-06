import arxiv

from src.paper_metadata import get_paper_metadata


search = arxiv.Search(
    query='ti:"Attention Is All You Need"',
    max_results=1
)

client = arxiv.Client()

result = next(
    client.results(search)
)

authors = [
    author.name
    for author in result.authors
]

print("TITLE:", result.title)
print("AUTHORS:", authors)

metadata = get_paper_metadata(
    result,
    authors
)

print("\nMETADATA:")
print(metadata)