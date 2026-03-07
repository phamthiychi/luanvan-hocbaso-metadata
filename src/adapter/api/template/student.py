from pydantic import BaseModel
from typing import Optional, Any

class StudentCreate(BaseModel):
    code: str
    name: str
    date_of_birth: str
    gender: str
    nationality: str
    card_id: Optional[str] = None
    edu_id: Optional[str] = None
    status: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    other_info: Optional[Any] = None

class StudentUpdate(BaseModel):
    code: str
    nationality: Optional[str] = None
    card_id: Optional[str] = None
    status: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    other_info: Optional[Any] = None
