import arxiv

from src.paper_metadata import get_paper_metadata


def search_papers(query, max_results=5):

    client = arxiv.Client()

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    papers = []

    for result in client.results(search):

        authors = [
            author.name
            for author in result.authors
        ]

        metadata = get_paper_metadata(
            result,
            authors
        )

        papers.append({
            "title": result.title,

            "authors": authors,

            "summary": result.summary,

            "url": result.entry_id,

            "published": result.published.strftime(
                "%Y-%m-%d"
            ),

            "venue": metadata["venue"],

            "venue_type": metadata["venue_type"],

            "doi": metadata["doi"],

            "issn": metadata["issn"],

            "quartile": metadata["quartile"],

            "quartile_source": metadata[
                "quartile_source"
            ]
        })

    return papers