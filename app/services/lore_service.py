import json

BASE_PATH = "lore_core"


# ----------------------------
# FUZZY MATCH CORE
# ----------------------------
def fuzzy_match_score(text: str, query: str) -> float:
    """
    Simple fuzzy matching using word overlap.
    No external libraries needed.
    """

    if not tags:
        return 0

    text_words = set(text.lower().split())
    query_words = set(query.lower().split())

    if not text_words or not query_words:
        return 0

    intersection = text_words.intersection(query_words)

    return len(intersection) / len(text_words)


# ----------------------------
# FILE LOADER
# ----------------------------
def load_data(file_name):
    with open(f"{BASE_PATH}/{file_name}", "r") as f:
        return json.load(f)


# ----------------------------
# MEMORY SAVE
# ----------------------------
def save_lore_entry(entry):
    data = load_data("memory.json")

    data.append(entry)

    with open(f"{BASE_PATH}/memory.json", "w") as f:
        json.dump(data, f, indent=4)

    return entry


# ----------------------------
# MEMORY SEARCH (FUZZY)
# ----------------------------
def search_memory(question: str):
    data = load_data("memory.json")

    best_match = None
    best_score = 0

    for item in data:
        name = item.get("name", "")

        score = fuzzy_match_score(name, question)

        if score > best_score:
            best_score = score
            best_match = item

    if best_score >= 0.3:
        return best_match

    return None


# ----------------------------
# FALLBACK DATA SEARCH
# ----------------------------
def search_dataset(question, dataset):
    best_match = None
    best_score = 0

    for item in dataset:
        name = item.get("name", "")

        score = fuzzy_match_score(name, question)

        if score > best_score:
            best_score = score
            best_match = item

    if best_score >= 0.3:
        return best_match.get("lore", "")

    return None


# ----------------------------
# MAIN RESPONSE ENGINE
# ----------------------------
def get_lore_response(question: str):

    # 1. Check user memory first
    memory = search_memory(question)
    if memory:
        return memory["lore"]

    # 2. Load static lore
    characters = load_data("characters.json")
    factions = load_data("factions.json")
    events = load_data("events.json")
    locations = load_data("locations.json")

    for dataset in [characters, factions, events, locations]:
        result = search_dataset(question, dataset)
        if result:
            return result

    return "No matching lore found."