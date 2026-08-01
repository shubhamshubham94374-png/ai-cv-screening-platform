import os
import uuid
from app.services.storage.base import StorageService

class LocalStorage(StorageService):
    def __init__(self, upload_dir: str):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    def save(self, file_bytes: bytes, filename: str) -> str:
        ext = os.path.splitext(filename)[1]
        unique_name = f"{uuid.uuid4()}{ext}"
        full_path = os.path.join(self.upload_dir, unique_name)
        with open(full_path, "wb") as f:
            f.write(file_bytes)
        return full_path