from pydantic import BaseModel
from typing import Optional


class JobCreateRequest(BaseModel):
    title: str
    company: Optional[str] = None
    description: str