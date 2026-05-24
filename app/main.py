from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router

app = FastAPI(title="Lore Bot v0.1")

app.include_router(router)

app.mount("/", StaticFiles(directory="app/static", html=True), name="static")


@app.get("/health")
def health():
    return {"status": "ok"}