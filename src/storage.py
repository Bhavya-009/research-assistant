import json
import os
from datetime import datetime


# ==================================================
# SAVED PAPER SUMMARIES
# ==================================================

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
        json.dump(
            summaries,
            f,
            indent=4,
            ensure_ascii=False
        )


def delete_summary(index):

    filename = "data/summaries/summaries.json"

    if not os.path.exists(filename):
        return

    with open(filename, "r", encoding="utf-8") as f:
        summaries = json.load(f)

    if 0 <= index < len(summaries):
        summaries.pop(index)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            summaries,
            f,
            indent=4,
            ensure_ascii=False
        )


# ==================================================
# RESEARCH GAPS
# ==================================================

def save_research_gap(gap, direction, papers):

    folder = "data/research_gaps"

    os.makedirs(folder, exist_ok=True)

    filename = os.path.join(
        folder,
        "gaps.json"
    )

    if os.path.exists(filename):

        with open(filename, "r", encoding="utf-8") as f:
            gaps = json.load(f)

    else:

        gaps = []


    new_gap = {
        "gap": gap,
        "direction": direction,
        "papers": papers,
        "status": "New",
        "created_at": datetime.now().isoformat()
    }


    gaps.append(new_gap)


    with open(filename, "w", encoding="utf-8") as f:

        json.dump(
            gaps,
            f,
            indent=4,
            ensure_ascii=False
        )


def load_research_gaps():

    filename = "data/research_gaps/gaps.json"

    if not os.path.exists(filename):
        return []

    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def update_research_gap_status(index, status):

    filename = "data/research_gaps/gaps.json"

    if not os.path.exists(filename):
        return

    with open(filename, "r", encoding="utf-8") as f:
        gaps = json.load(f)


    if 0 <= index < len(gaps):

        gaps[index]["status"] = status


    with open(filename, "w", encoding="utf-8") as f:

        json.dump(
            gaps,
            f,
            indent=4,
            ensure_ascii=False
        )

def save_research_proposal(index, proposal):

    filename = "data/research_gaps/gaps.json"

    if not os.path.exists(filename):
        return

    with open(filename, "r", encoding="utf-8") as f:
        gaps = json.load(f)

    if 0 <= index < len(gaps):
        gaps[index]["research_proposal"] = proposal

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            gaps,
            f,
            indent=4,
            ensure_ascii=False
        )