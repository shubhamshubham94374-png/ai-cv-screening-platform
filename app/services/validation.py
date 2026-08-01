import hashlib
from fastapi import HTTPException
from app.core.config import settings

ALLOWED_EXTENSIONS = {".pdf", ".docx"}

def validate_file(filename: str, file_bytes: bytes) -> None:
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}. Only PDF and DOCX allowed.")

    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > settings.max_file_size_mb:
        raise HTTPException(status_code=400, detail=f"File too large ({size_mb:.2f}MB). Max allowed: {settings.max_file_size_mb}MB.")

def compute_file_hash(file_bytes: bytes) -> str:
    return hashlib.sha256(file_bytes).hexdigest()
