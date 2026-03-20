from pydantic import BaseModel
from typing import Optional

class ClassEnrollmentCreate(BaseModel):
    student_id: str
    class_id: str
    grade_level_id: str
    academic_year_id: str
    semester_id: str
    enrollment_date: str
    note: Optional[str] = None

class ClassEnrollmentUpdate(BaseModel):
    student_id: str
    class_id: str
    grade_level_id: str
    academic_year_id: str
    semester_id: str
    enrollment_date: Optional[str] = None
    note: Optional[str] = None