import json
import os
from datetime import datetime


def save_summary(paper, summary):

    os.makedirs("data/summaries", exist_ok=True)

    data = {
        "title": paper["title"],
        "authors": paper["authors"],
        "published": paper["published"],
        "url": paper["url"],
        "summary": summary,
        "saved_at": datetime.now().isoformat()
    }

    filename = "data/summaries/summaries.json"

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            summaries = json.load(f)
    else:
        summaries = []

    summaries.append(data)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(summaries, f, indent=4, ensure_ascii=False)