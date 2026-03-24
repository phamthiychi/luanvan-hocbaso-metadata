from typing import List
from pydantic import BaseModel

from src.model.ontology.assessment import Assessment

class StudentReport(BaseModel):
    student_code: str
    assessments: List[Assessment]
