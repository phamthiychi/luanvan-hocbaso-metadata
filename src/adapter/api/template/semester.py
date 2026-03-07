from pydantic import BaseModel
from typing import Optional


class SemesterCreate(BaseModel):
    code: str
    name: str
    start_date: str
    end_date: str
    academic_year_id: str

class SemesterUpdate(BaseModel):
    code: str
    name: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    academic_year_id: Optional[str] = None