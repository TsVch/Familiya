from pathlib import Path
import os
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

# 👇 Для деплоя проекта на Render(веб- хостинг)
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
