from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: int
    username: str

class TokenRefresh(BaseModel):
    refresh_token: str

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None