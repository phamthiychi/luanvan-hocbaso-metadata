from typing import Optional

class Score:
    def __init__(
        self,
        code: str,
        name: str,
        description: Optional[str] = None
    ):
        self.code = code
        self.data = ScoreData(
            name=name,
            description=description
        )
        self._validate()

    def _validate(self):
        if not self.code:
            raise ValueError("score's code cannot be empty")

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "data": self.data.to_dict()
        }

    @classmethod
    def from_dict(cls, data: dict):
        score_data = ScoreData.from_dict(data.get("data"))
        return cls(
            code=data.get("code"),
            name=score_data.name,
            description=score_data.description
        )

class ScoreData:
    def __init__(
        self,
        name: str,
        description: Optional[str] = None
    ):
        self.name = name
        self.description = description
        self._validate()

    def _validate(self):
        if not self.name:
            raise ValueError("score's name cannot be empty")

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data.get("name"),
            description=data.get("description")
        )