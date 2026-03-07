from pydantic import BaseModel
from typing import Optional

class SchoolClassCreate(BaseModel):
    code: str
    name: str
    size: int
    grade_level_id: str
    academic_year_id: str
    special_program: Optional[str] = None

class SchoolClassUpdate(BaseModel):
    code: str
    name: Optional[str] = None
    size: Optional[int] = None
    grade_level_id: Optional[str] = None
    academic_year_id: Optional[str] = None
    special_program: Optional[str] = None