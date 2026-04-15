from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from utils.deps import get_current_user

router = APIRouter(tags=["upload"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}


@router.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    _current_user=Depends(get_current_user),
):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only image uploads are allowed")

    filename = f"{uuid4().hex}{suffix}"
    destination = UPLOAD_DIR / filename

    with destination.open("wb") as buffer:
        buffer.write(file.file.read())

    return {"file_path": f"/uploads/{filename}"}
