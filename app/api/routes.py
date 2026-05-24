from fastapi import APIRouter
from pydantic import BaseModel

from app.services.lore_service import (
    get_lore_response,
    save_lore_entry,
    search_memory,
    load_data
)

router = APIRouter()


# ----------------------------
# REQUEST MODELS
# ----------------------------
class AskRequest(BaseModel):
    question: str


class LoreEntry(BaseModel):
    name: str
    lore: str


# ----------------------------
# WRITE ROUTES (CREATE DATA)
# ----------------------------
@router.post("/add_lore")
def add_lore(entry: LoreEntry):

    saved = save_lore_entry({
        "name": entry.name,
        "lore": entry.lore
    })

    return {
        "message": "Lore saved",
        "entry": saved
    }


# ----------------------------
# READ ROUTES (VIEW DATA)
# ----------------------------
@router.get("/lore")
def get_all_lore():
    return {
        "memory": load_data("memory.json"),
        "characters": load_data("characters.json"),
        "factions": load_data("factions.json"),
        "events": load_data("events.json"),
        "locations": load_data("locations.json")
    }


# ----------------------------
# CORE LOGIC (ASK SYSTEM)
# ----------------------------
@router.post("/ask")
def ask_lore(payload: AskRequest):

    memory_result = search_memory(payload.question)

    if memory_result:
        return {
            "query": payload.question,
            "response": memory_result["lore"],
            "source": "memory",
            "version": "0.2-memory"
        }

    response = get_lore_response(payload.question)

    return {
        "query": payload.question,
        "response": response,
        "source": "lore_core",
        "version": "0.2-memory"
    }