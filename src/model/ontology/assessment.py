import json
from typing import List, Literal
from pydantic import BaseModel, Field

class Assessment(BaseModel):
    category: Literal["Kiến thức", "Kỹ năng", "Thái độ"]
    competency: Literal["Toán học", "Ngôn ngữ", "Giao tiếp", "Giải quyết vấn đề", "Tự học"]
    level: Literal["Hoàn thành tốt", "Hoàn thành", "Cần cố gắng"]
    evidence: str = Field(description="Đoạn văn gốc minh chứng cho nhận xét này")
