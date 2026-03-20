from pydantic import BaseModel
from typing import Optional

class ClassRoomCreate(BaseModel):
    code: str
    name: str
    size: int
    grade_level_id: Optional[str] = None
    academic_year_id: Optional[str] = None
    special_program: Optional[str] = None

class ClassRoomUpdate(BaseModel):
    code: str
    name: Optional[str] = None
    size: Optional[int] = None
    grade_level_id: Optional[str] = None
    academic_year_id: Optional[str] = None
    special_program: Optional[str] = None