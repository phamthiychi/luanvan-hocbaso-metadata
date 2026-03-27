from typing import List, Literal
from pydantic import BaseModel

class StudentAssessment(BaseModel):
    category: Literal["Kiến thức", "Kỹ năng", "Thái độ"]
    competency: Literal["Toán học", "Ngôn ngữ", "Giao tiếp", "Giải quyết vấn đề", "Tự học"]
    level: Literal["Hoàn thành tốt", "Hoàn thành", "Cần cố gắng"]
    evidence: str

    def to_dict(self):
        return self.model_dump()

class StudentReport(BaseModel):
    code: str
    name: str
    card_id: str
    edu_id: str
    assessments: List[StudentAssessment]

    def to_dict(self):
        return self.model_dump()

