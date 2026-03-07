from typing import Optional

class Subject:
    def __init__(
        self,
        code: str,
        name: str,
        total_periods: int
    ):
        self.code = code
        self.data = SubjectData(
            name=name,
            total_periods=total_periods
        )
        self._validate()

    def _validate(self):
        if not self.code:
            raise ValueError("subject's code cannot be empty")

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "data": self.data.to_dict()
        }

    @classmethod
    def from_dict(cls, data: dict):
        subject_data = SubjectData.from_dict(data.get("data"))
        return cls(
            code=data.get("code"),
            name=subject_data.name,
            total_periods=subject_data.total_periods
        )

class SubjectData:
    def __init__(
        self,
        name: str,
        total_periods: int
    ):
        self.name = name
        self.total_periods = total_periods
        self._validate()

    def _validate(self):
        if not self.name:
            raise ValueError("subject's name cannot be empty")
        if self.total_periods is None:
            raise ValueError("subject's total periods cannot be empty")

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "total_periods": self.total_periods
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data.get("name"),
            total_periods=data.get("total_periods")
        )