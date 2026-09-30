import json
import os


CONFIG_FILE = "data/research_config.json"


def load_research_interests():

    if not os.path.exists(CONFIG_FILE):
        return []

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("research_interests", [])


def save_research_interest(interest):

    os.makedirs("data", exist_ok=True)

    interests = load_research_interests()

    if interest not in interests:
        interests.append(interest)

    data = {
        "research_interests": interests
    }

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)