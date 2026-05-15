from turtle import title
from fastapi import FastAPI

app = FastAPI(title="Lore Bot API")

@app.get("/")
def root():
    return {"message": "Lore Bot is online"}