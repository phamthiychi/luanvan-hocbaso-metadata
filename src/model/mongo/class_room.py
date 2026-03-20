from typing import Optional

class ClassRoom:
    def __init__(
        self,
        code: str,
        name: str,
        size: int,
        grade_level_id: str,
        academic_year_id: str,
        special_program: Optional[str] = None
    ):
        self.code = code
        self.data = ClassRoomData(
            name=name,
            size=size,
            grade_level_id=grade_level_id,
            academic_year_id=academic_year_id,
            special_program=special_program
        )
        self._validate()

    def _validate(self):
        if not self.code:
            raise ValueError("class code cannot be empty")

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "data": self.data.to_dict()
        }

    @classmethod
    def from_dict(cls, data: dict):
        class_data = ClassRoomData.from_dict(data.get("data"))
        return cls(
            code=data.get("code"),
            name=class_data.name,
            size=class_data.size,
            grade_level_id=class_data.grade_level_id,
            academic_year_id=class_data.academic_year_id,
            special_program=class_data.special_program
        )

class ClassRoomData:
    def __init__(
        self,
        name: str,
        size: int,
        grade_level_id: str,
        academic_year_id: str,
        special_program: Optional[str] = None
    ):
        self.name = name
        self.size = size
        self.special_program = special_program
        self.grade_level_id = grade_level_id
        self.academic_year_id = academic_year_id
        self._validate()

    def _validate(self):
        if not self.name:
            raise ValueError("class's name cannot be empty")
        if self.size is None:
            raise ValueError("class's size cannot be empty")
        if self.size <= 0:
            raise ValueError("class's size must be greater than 0")
        if not self.grade_level_id:
            raise ValueError("class's grade level id cannot be empty")
        if not self.academic_year_id:
            raise ValueError("class's academic year id cannot be empty")

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "size": self.size,
            "special_program": self.special_program,
            "grade_level_id": self.grade_level_id,
            "academic_year_id": self.academic_year_id
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data.get("name"),
            size=data.get("size"),
            special_program=data.get("special_program"),
            grade_level_id=data.get("grade_level_id"),
            academic_year_id=data.get("academic_year_id")
        )