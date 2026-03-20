from __future__ import annotations
from typing import Generic, Optional, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from src.interface.data import Repository
from src.model.postgres.academic_year import AcademicYear
from src.model.postgres.class_room import ClassRoom
from src.model.postgres.grade_level import GradeLevel
from src.model.postgres.score import Score
from src.model.postgres.semester import Semester
from src.model.postgres.student import Student
from src.model.postgres.subject import Subject
from src.model.postgres.teacher import Teacher

T = TypeVar("T")

class PostgresRepository(Repository[T], Generic[T]):
    model_cls: type[T]
    code: str
    field_ignores: Optional[list] = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, create_info: T) -> Optional[T]:
        if self.field_ignores:
            for field in self.field_ignores:
                create_info.pop(field, None)
        entity = self.model_cls(**create_info)
        exist = await self.get(entity.code)
        if exist:
            return None
        try:
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except Exception as e:
            self.session.rollback()
            raise e

    async def get(self, code: str) -> Optional[T]:
        return self.session.query(self.model_cls) \
               .filter(self.model_cls.code == code).first()

    async def get_all(self) -> Optional[list[T]]:
        return self.session.query(self.model_cls).all()

    async def delete(self, code: str) -> bool:
        entity = await self.get(code)
        if entity is None:
            return False
        try:
            self.session.delete(entity)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise e

    async def update(self, update_info: dict) -> Optional[T]:
        code = update_info.get(self.code)
        if code is None:
            raise ValueError(f"'{self.id_field}' is required")
        entity = await self.get(code)
        entity_clone = entity.to_dict().copy()
        if entity is None:
            return None
        for field, value in update_info.items():
            if value is None:
                continue
            if hasattr(entity, field):
                setattr(entity, field, value)
        print(entity.to_dict())
        print(entity_clone)
        if entity.to_dict() == entity_clone:
             raise HTTPException(
                        status_code=400,
                        detail="No fields were changed"
                   )
        try:
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except Exception as e:
            self.session.rollback()
            raise e

class PostgresAcademicYearRepository(PostgresRepository[AcademicYear]):
    model_cls = AcademicYear
    code = "code"

class PostgresSemesterRepository(PostgresRepository[Semester]):
    model_cls = Semester
    code = "code"
    field_ignores = ["academic_year_id"]

class PostgresGradeLevelRepository(PostgresRepository[GradeLevel]):
    model_cls = GradeLevel
    code = "code"

class PostgresClassRoomRepository(PostgresRepository[ClassRoom]):
    model_cls = ClassRoom
    code = "code"
    field_ignores = ["grade_level_id", "academic_year_id"]

class PostgresStudentRepository(PostgresRepository[Student]):
    model_cls = Student
    code = "code"
    field_ignores = ["other_info"]

class PostgresTeacherRepository(PostgresRepository[Teacher]):
    model_cls = Teacher
    code = "code"

class PostgresSubjectRepository(PostgresRepository[Subject]):
    model_cls = Subject
    code = "code"

class PostgresScoreRepository(PostgresRepository[Score]):
    model_cls = Score
    code = "code"
    field_ignores = ["description"]

