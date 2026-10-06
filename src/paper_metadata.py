import requests
from difflib import SequenceMatcher


OPENALEX_URL = "https://api.openalex.org/works"
CROSSREF_URL = "https://api.crossref.org/works"


def normalize_title(title):
    """Normalize a title for comparison."""

    return " ".join(
        title.lower()
        .replace(":", " ")
        .replace("-", " ")
        .replace(".", " ")
        .split()
    )


def title_similarity(title1, title2):
    """Return similarity between two titles."""

    return SequenceMatcher(
        None,
        normalize_title(title1),
        normalize_title(title2)
    ).ratio()


def clean_doi(doi):
    """Clean a DOI returned by an API."""

    if not doi:
        return None

    doi = doi.strip()

    prefixes = [
        "https://doi.org/",
        "http://doi.org/",
        "https://dx.doi.org/",
        "http://dx.doi.org/",
        "doi:"
    ]

    for prefix in prefixes:
        if doi.lower().startswith(prefix.lower()):
            doi = doi[len(prefix):]

    return doi.strip()


def get_arxiv_metadata(result):
    """
    Get metadata directly from the arXiv result.

    This is our first source because the paper itself
    came from arXiv.
    """

    journal_ref = getattr(
        result,
        "journal_ref",
        None
    )

    doi = getattr(
        result,
        "doi",
        None
    )

    comment = getattr(
        result,
        "comment",
        None
    )

    # arXiv sometimes stores a DOI as an external link
    if not doi:

        try:

            for link in result.links:

                href = getattr(
                    link,
                    "href",
                    ""
                )

                if "doi.org/" in href.lower():

                    doi = href.split(
                        "doi.org/",
                        1
                    )[1]

                    break

        except Exception:
            pass

    doi = clean_doi(doi)

    # If arXiv explicitly gives a journal reference,
    # we know the paper has a published venue.
    if journal_ref:

        return {
            "venue": journal_ref,
            "venue_type": "Published / Journal or Conference",
            "doi": doi,
            "issn": None
        }

    # No journal reference does NOT automatically mean
    # the paper is a journal article.
    return {
        "venue": None,
        "venue_type": "Preprint",
        "doi": doi,
        "issn": None
    }


def verify_doi_with_crossref(doi, title):
    """
    Verify a DOI using Crossref.

    We only accept it if the Crossref title is
    sufficiently similar to our actual paper.
    """

    if not doi:
        return None

    try:

        response = requests.get(
            f"{CROSSREF_URL}/{doi}",
            headers={
                "User-Agent":
                    "ResearchAssistant/1.0"
            },
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()

        work = data.get(
            "message"
        )

        if not work:
            return None

        crossref_titles = work.get(
            "title",
            []
        )

        if not crossref_titles:
            return None

        crossref_title = crossref_titles[0]

        similarity = title_similarity(
            title,
            crossref_title
        )

        # Strict verification
        if similarity < 0.90:
            return None

        container_titles = work.get(
            "container-title",
            []
        )

        venue = (
            container_titles[0]
            if container_titles
            else None
        )

        issns = work.get(
            "ISSN",
            []
        )

        issn = (
            issns[0]
            if issns
            else None
        )

        publication_type = work.get(
            "type",
            ""
        )

        if publication_type == "journal-article":
            venue_type = "Journal"

        elif publication_type in [
            "proceedings-article",
            "proceedings"
        ]:
            venue_type = "Conference"

        else:
            venue_type = "Published / Other"

        return {
            "venue": venue or "Not found",
            "venue_type": venue_type,
            "doi": clean_doi(
                work.get("DOI")
            ),
            "issn": issn
        }

    except Exception:
        return None


def search_crossref_by_title(title, authors):
    """
    Search Crossref by title only as a fallback.

    The result is accepted only after strict
    title and author verification.
    """

    try:

        response = requests.get(
            CROSSREF_URL,
            params={
                "query.title": title,
                "rows": 10
            },
            headers={
                "User-Agent":
                    "ResearchAssistant/1.0"
            },
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        results = data.get(
            "message",
            {}
        ).get(
            "items",
            []
        )

        best_result = None
        best_score = 0

        for result in results:

            titles = result.get(
                "title",
                []
            )

            if not titles:
                continue

            result_title = titles[0]

            score = title_similarity(
                title,
                result_title
            )

            # Require very strong title match
            if score < 0.92:
                continue

            # Author verification
            if authors:

                crossref_authors = result.get(
                    "author",
                    []
                )

                crossref_names = []

                for author in crossref_authors:

                    family = author.get(
                        "family",
                        ""
                    ).lower()

                    given = author.get(
                        "given",
                        ""
                    ).lower()

                    crossref_names.append(
                        f"{given} {family}"
                    )

                author_match = False

                for author in authors:

                    last_name = (
                        author
                        .split()[-1]
                        .lower()
                    )

                    if any(
                        last_name in name
                        for name in crossref_names
                    ):
                        author_match = True
                        break

                # If authors were supplied but no author
                # matches, reject the result.
                if not author_match:
                    continue

            if score > best_score:

                best_score = score
                best_result = result

        if not best_result:
            return None

        titles = best_result.get(
            "title",
            []
        )

        container_titles = best_result.get(
            "container-title",
            []
        )

        issns = best_result.get(
            "ISSN",
            []
        )

        publication_type = best_result.get(
            "type",
            ""
        )

        if publication_type == "journal-article":
            venue_type = "Journal"

        elif publication_type in [
            "proceedings-article",
            "proceedings"
        ]:
            venue_type = "Conference"

        else:
            venue_type = "Published / Other"

        return {
            "venue": (
                container_titles[0]
                if container_titles
                else "Not found"
            ),
            "venue_type": venue_type,
            "doi": clean_doi(
                best_result.get("DOI")
            ),
            "issn": (
                issns[0]
                if issns
                else None
            )
        }

    except Exception:
        return None


def search_openalex(title, authors):
    """
    OpenAlex fallback.

    Only accepts a strongly matching title and,
    where possible, matching author.
    """

    try:

        response = requests.get(
            OPENALEX_URL,
            params={
                "search": title,
                "per-page": 10
            },
            timeout=10
        )

        response.raise_for_status()

        results = response.json().get(
            "results",
            []
        )

        best_result = None
        best_score = 0

        for result in results:

            result_title = result.get(
                "display_name",
                ""
            )

            if not result_title:
                continue

            score = title_similarity(
                title,
                result_title
            )

            if score < 0.92:
                continue

            # Author verification
            if authors:

                authorships = result.get(
                    "authorships",
                    []
                )

                openalex_authors = []

                for authorship in authorships:

                    author = authorship.get(
                        "author",
                        {}
                    )

                    name = author.get(
                        "display_name",
                        ""
                    ).lower()

                    if name:
                        openalex_authors.append(
                            name
                        )

                author_match = False

                for author in authors:

                    last_name = (
                        author
                        .split()[-1]
                        .lower()
                    )

                    if any(
                        last_name in name
                        for name in openalex_authors
                    ):
                        author_match = True
                        break

                if not author_match:
                    continue

            if score > best_score:

                best_score = score
                best_result = result

        if not best_result:
            return None

        primary_location = (
            best_result.get(
                "primary_location"
            )
            or {}
        )

        source = (
            primary_location.get(
                "source"
            )
            or {}
        )

        venue = source.get(
            "display_name"
        )

        issn = source.get(
            "issn_l"
        )

        work_type = best_result.get(
            "type"
        )

        if work_type == "article":
            venue_type = "Journal"

        elif work_type == "proceedings-article":
            venue_type = "Conference"

        elif work_type == "preprint":
            venue_type = "Preprint"

        else:
            venue_type = "Published / Other"

        return {
            "venue": venue or "Not found",
            "venue_type": venue_type,
            "doi": clean_doi(
                best_result.get("doi")
            ),
            "issn": issn
        }

    except Exception:
        return None


def get_paper_metadata(result, authors):
    """
    Main metadata pipeline.

    Priority:

    1. arXiv record
    2. Verify arXiv DOI with Crossref
    3. Crossref title search
    4. OpenAlex title search
    5. Safe fallback to Preprint / Unknown

    Quartile is intentionally N/A until the
    journal ranking lookup is implemented.
    """

    title = result.title

    # ------------------------------------------------
    # STEP 1: Read arXiv metadata
    # ------------------------------------------------

    arxiv_metadata = get_arxiv_metadata(
        result
    )

    doi = arxiv_metadata["doi"]

    # ------------------------------------------------
    # STEP 2: Verify DOI
    # ------------------------------------------------

    if doi:

        verified = verify_doi_with_crossref(
            doi,
            title
        )

        if verified:

            verified["quartile"] = "N/A"
            verified["quartile_source"] = None

            return verified

    # ------------------------------------------------
    # STEP 3: Crossref title search
    # ------------------------------------------------

    crossref_metadata = search_crossref_by_title(
        title,
        authors
    )

    if crossref_metadata:

        crossref_metadata["quartile"] = "N/A"
        crossref_metadata[
            "quartile_source"
        ] = None

        return crossref_metadata

    # ------------------------------------------------
    # STEP 4: OpenAlex
    # ------------------------------------------------

    openalex_metadata = search_openalex(
        title,
        authors
    )

    if openalex_metadata:

        openalex_metadata["quartile"] = "N/A"
        openalex_metadata[
            "quartile_source"
        ] = None

        return openalex_metadata

    # ------------------------------------------------
    # STEP 5: Safe fallback
    # ------------------------------------------------

    return {
        "venue": (
            arxiv_metadata["venue"]
            or "Not found"
        ),

        "venue_type": (
            arxiv_metadata["venue_type"]
        ),

        "doi": doi,

        "issn": (
            arxiv_metadata["issn"]
        ),

        "quartile": "N/A",

        "quartile_source": None
    }