from pydantic import BaseModel
# from uuid import UUID
# from datetime import datetime

class User(BaseModel):
    first_name: str
    last_name: str | None = None
    email: str
    phone: str | None = None
    role: str