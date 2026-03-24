from openai import OpenAI
from typing import get_args
from src.common.settings import settings

class ChatGptAssistant:
    def __init__(self):
        self.client = OpenAI(api_key=settings.CHAT_GPT_API_KEY)

    def generate_standards(self, model_class : type) -> str:
        instructions = []
        fields = model_class.__annotations__
        for field_name, field_type in fields.items():
            options = get_args(field_type)
            if options:
                label = field_name.capitalize() 
                options_str = ", ".join(options)
                instructions.append(f"- {label}: {options_str}.")
        return "\n    ".join(instructions)
    
    def extract_assessment(self, student_code:str, comment: str,
                           model_class: type, format: type) -> list:
        prompt = f"""
            Bạn là hệ thống AI phân tích học bạ chuyên nghiệp. 
            Dựa trên đoạn nhận xét sau của học sinh {student_code}: "{comment}"
            
            Hãy phân loại các ý kiến vào đúng các tiêu chuẩn sau đây:
            {self.generate_standards(model_class)}
        
            Yêu cầu: Trích xuất chính xác 'evidence' từ văn bản gốc.
        """
        response = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Bạn là trợ lý phân tích dữ liệu giáo dục chuẩn xác."},
                {"role": "user", "content": prompt}
            ],
            response_format=format,
        )
        return response.choices[0].message.parsed \
                .model_dump_json(indent=2, ensure_ascii=False)
        
    
