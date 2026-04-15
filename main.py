from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from database import Base, engine
from routes import auth_router, chats_router, messages_router, upload_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Family Chat MVP")

app.include_router(auth_router)
app.include_router(chats_router)
app.include_router(messages_router)
app.include_router(upload_router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def serve_index():
    index_path = Path("static") / "index.html"
    return FileResponse(index_path)
