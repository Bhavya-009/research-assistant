import json
import os


def load_saved_summaries():
    filename = "data/summaries/summaries.json"

    if not os.path.exists(filename):
        return []

    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)