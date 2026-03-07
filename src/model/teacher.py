from typing import Optional

class Teacher:
    def __init__(
        self,
        code: str,
        name: str,
        date_of_birth: str,
        gender: str,
        nationality: str,
        status: Optional[str] = None,
        phone: Optional[str] = None,
        specialization: Optional[str] = None,
        position: Optional[str] = None,
    ):
        self.code = code
        self.data = TeacherData(
            name=name,
            date_of_birth=date_of_birth,
            gender=gender,
            nationality=nationality,
            status=status,
            phone=phone,
            specialization=specialization,
            position=position,
        )
        self._validate()

    def _validate(self):
        if not self.code:
            raise ValueError("teacher's code cannot be empty")

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "data": self.data.to_dict()
        }

    @classmethod
    def from_dict(cls, data: dict):
        teacher_data = TeacherData.from_dict(data.get("data"))
        return cls(
            code=data.get("code"),
            name=teacher_data.name,
            date_of_birth=teacher_data.date_of_birth,
            gender=teacher_data.gender,
            nationality=teacher_data.nationality,
            status=teacher_data.status,
            phone=teacher_data.phone,
            specialization=teacher_data.specialization,
            position=teacher_data.position,
        )


class TeacherData:
    def __init__(
        self,
        name: str,
        date_of_birth: str,
        gender: str,
        nationality: str,
        status: Optional[str] = None,
        phone: Optional[str] = None,
        specialization: Optional[str] = None,
        position: Optional[str] = None,
    ):
        self.name = name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.nationality = nationality
        self.status = status
        self.phone = phone
        self.specialization = specialization
        self.position = position
        self._validate()

    def _validate(self):
        if not self.name:
            raise ValueError("teacher's name cannot be empty")
        if not self.date_of_birth:
            raise ValueError("teacher's date of birth cannot be empty")
        if not self.gender:
            raise ValueError("teacher's gender cannot be empty")
        if not self.nationality:
            raise ValueError("teacher's nationality cannot be empty")

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "date_of_birth": self.date_of_birth,
            "gender": self.gender,
            "status": self.status,
            "phone": self.phone,
            "nationality": self.nationality,
            "specialization": self.specialization,
            "position": self.position,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data.get("name"),
            date_of_birth=data.get("date_of_birth"),
            gender=data.get("gender"),
            nationality=data.get("nationality"),
            status=data.get("status"),
            phone=data.get("phone"),
            specialization=data.get("specialization"),
            position=data.get("position"),
        )