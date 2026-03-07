from typing import Optional

class GradeLevel:
    def __init__(
        self,
        code: str,
        name: str,
        max_students: int
    ):
        self.code = code
        self.data = GradeLevelData(
            name=name,
            max_students=max_students
        )
        self._validate()

    def _validate(self):
        if not self.code:
            raise ValueError("grade level's code cannot be empty")

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "data": self.data.to_dict()
        }

    @classmethod
    def from_dict(cls, data: dict):
        grade_data = GradeLevelData.from_dict(data.get("data"))
        return cls(
            code=data.get("code"),
            name=grade_data.name,
            max_students=grade_data.max_students
        )

class GradeLevelData:
    def __init__(
        self,
        name: str,
        max_students: int
    ):
        self.name = name
        self.max_students = max_students
        self._validate()

    def _validate(self):
        if not self.name:
            raise ValueError("grade level's name cannot be empty")
        if self.max_students is None:
            raise ValueError("max_students cannot be empty")

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "max_students": self.max_students
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data.get("name"),
            max_students=data.get("max_students")
        )