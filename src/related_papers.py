import arxiv

def find_related_papers(paper, max_results=5):

    client = arxiv.Client()

    query = (
        f'"{paper["title"]}" '
        f'OR ({paper["title"]})'
    )

    search = arxiv.Search(
        query=query,
        max_results=max_results + 1,
        sort_by=arxiv.SortCriterion.Relevance
    )

    related_papers = []

    for result in client.results(search):

        # Don't return the selected paper itself
        if result.entry_id == paper["url"]:
            continue

        authors = [
            author.name
            for author in result.authors
        ]

        related_papers.append({
            "title": result.title,
            "authors": authors,
            "summary": result.summary,
            "url": result.entry_id,
            "pdf_url": result.pdf_url,
            "published": result.published.strftime("%Y-%m-%d")
        })

        if len(related_papers) >= max_results:
            break

    return related_papers