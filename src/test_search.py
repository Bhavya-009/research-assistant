from paper_search import search_papers

papers = search_papers("AI agents", 3)

for paper in papers:
    print("\nTITLE:", paper["title"])
    print("DATE:", paper["published"])
    print("URL:", paper["url"])