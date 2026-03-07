from typing import Optional

class AcademicYear:
    def __init__(
        self,
        code: str,
        name: str,
        start_date: str,
        end_date: str
    ):
        self.code = code
        self.data = AcademicYearData(
            name=name,
            start_date=start_date,
            end_date=end_date
        )
        self._validate()

    def _validate(self):
        if not self.code:
            raise ValueError("academic year's code cannot be empty")

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "data": self.data.to_dict()
        }

    @classmethod
    def from_dict(cls, data: dict):
        year_data = AcademicYearData.from_dict(data.get("data"))
        return cls(
            code=data.get("code"),
            name=year_data.name,
            start_date=year_data.start_date,
            end_date=year_data.end_date
        )

class AcademicYearData:
    def __init__(
        self,
        name: str,
        start_date: str,
        end_date: str
    ):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self._validate()

    def _validate(self):
        if not self.name:
            raise ValueError("academic year's name cannot be empty")
        if not self.start_date:
            raise ValueError("academic year's start date cannot be empty")
        if not self.end_date:
            raise ValueError("academic year's end date cannot be empty")

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data.get("name"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date")
        )