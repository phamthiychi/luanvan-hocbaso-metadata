from typing import Optional, Any

class Student:
    def __init__(
        self,
        code: str,
        name: str,
        date_of_birth: str,
        gender: str,
        nationality: str,
        card_id: Optional[str] = None,
        edu_id: Optional[str] = None,
        status: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        other_info: Optional[Any] = None
    ):
        self.code = code
        self.data = StudentData(
            name=name,
            card_id=card_id,
            edu_id=edu_id,
            date_of_birth=date_of_birth,
            gender=gender,
            status=status,
            address=address,
            nationality=nationality,
            phone=phone
        )
        self.other_info = other_info
        self._validate()

    def _validate(self):
        if not self.code:
            raise ValueError("student's code cannot be empty")

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "data": self.data.to_dict(),
            "other_info": self.other_info
        }

    @classmethod
    def from_dict(cls, data: dict):
        student_data = StudentData.from_dict(data.get("data"))
        return cls(
            code=data.get("code"),
            name=student_data.name,
            date_of_birth=student_data.date_of_birth,
            gender=student_data.gender,
            nationality=student_data.nationality,
            card_id=student_data.card_id,
            edu_id=student_data.edu_id,
            status=student_data.status,
            phone=student_data.phone,
            address=student_data.address,
            other_info=data.get("other_info")
        )

class StudentData:
    def __init__(
        self,
        name: str,
        date_of_birth: str,
        gender: str,
        nationality: str,
        card_id: Optional[str] = None,
        edu_id: Optional[str] = None,
        status: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None
    ):
        self.name = name
        self.card_id = card_id
        self.edu_id = edu_id
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.nationality = nationality
        self.status = status
        self.phone = phone
        self.address = address
        self._validate()

    def _validate(self):
        if not self.name:
            raise ValueError("student's name cannot be empty")
        if not self.date_of_birth:
            raise ValueError("student's date of birth cannot be empty")
        if not self.gender:
            raise ValueError("student's gender cannot be empty.")
        if not self.nationality:
            raise ValueError("student's nationality cannot be empty.")

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "card_id": self.card_id,
            "edu_id": self.edu_id,
            "date_of_birth": self.date_of_birth,
            "gender": self.gender,
            "nationality": self.nationality,
            "status": self.status,
            "phone": self.phone,
            "address": self.address
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data.get("name"),
            card_id=data.get("card_id"),
            edu_id=data.get("edu_id"),
            date_of_birth=data.get("date_of_birth"),
            gender=data.get("gender"),
            nationality=data.get("nationality"),
            status=data.get("status"),
            phone=data.get("phone"),
            address=data.get("address"),
        )