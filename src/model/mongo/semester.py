from typing import Optional
from datetime import datetime, date

class Semester:
    def __init__(
        self,
        code: str,
        name: str,
        start_date: str,
        end_date: str,
        academic_year_id: str
    ):
        self.code = code
        self.data = SemesterData(
            name=name,
            start_date=start_date,
            end_date=end_date,
            academic_year_id=academic_year_id
        )
        self._validate()

    def _validate(self):
        if not self.code:
            raise ValueError("semester's code cannot be empty")

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "data": self.data.to_dict()
        }

    @classmethod
    def from_dict(cls, data: dict):
        semester_data = SemesterData.from_dict(data.get("data"))
        return cls(
            code=data.get("code"),
            name=semester_data.name,
            start_date=semester_data.start_date,
            end_date=semester_data.end_date,
            academic_year_id=semester_data.academic_year_id
        )

class SemesterData:
    def __init__(
        self,
        name: str,
        start_date: str,
        end_date: str,
        academic_year_id: str
    ):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.academic_year_id = academic_year_id
        self._validate()

    def _validate(self):
        if not self.name:
            raise ValueError("semester's name cannot be empty")
        if not self.start_date:
            raise ValueError("semester's start date cannot be empty")
        if not self.end_date:
            raise ValueError("semester's end date cannot be empty")
        try:
            if not isinstance(self.start_date, date):
                start = datetime.strptime(self.start_date, "%Y-%m-%d")
            if not isinstance(self.end_date, date):
                end = datetime.strptime(self.end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("semester's date must be in format YYYY-MM-DD")
        if start > end:
            raise ValueError("semester's start date must be before end date")
        if not self.academic_year_id:
            raise ValueError("semester's academic year id cannot be empty")

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "academic_year_id": self.academic_year_id
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data.get("name"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            academic_year_id=data.get("academic_year_id")
        )