from pydantic import BaseModel
from typing import Optional

class LearningResultCreate(BaseModel):
    student_id: str
    class_id: str
    academic_year_id: str
    semester_id: str
    subject_id: str
    score_id: str
    score_value: float
    test_date: str
    comment: Optional[str] = None
    note: Optional[str] = None

class LearningResultUpdate(BaseModel):
    student_id: str
    class_id: str
    academic_year_id: str
    semester_id: str
    subject_id: str
    score_id: str
    score_value: Optional[float] = None
    test_date: Optional[str] = None
    comment: Optional[str] = None
    note: Optional[str] = None