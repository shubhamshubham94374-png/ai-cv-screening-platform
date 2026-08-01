from abc import ABC, abstractmethod

class StorageService(ABC):
    @abstractmethod
    def save(self, file_bytes: bytes, filename: str) -> str:
        """Save file, return the storage path/key."""
        pass
    