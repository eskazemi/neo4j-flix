from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Base(BaseModel):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
