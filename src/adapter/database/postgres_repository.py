from __future__ import annotations
from typing import Generic, Optional, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from src.common.postgres_model_setting import settings
from src.interface.data import Repository
from src.model.postgres.academic_year import AcademicYear
from src.model.postgres.class_room import ClassRoom
from src.model.postgres.grade_level import GradeLevel
from src.model.postgres.score import Score
from src.model.postgres.semester import Semester
from src.model.postgres.student import Student
from src.model.postgres.subject import Subject
from src.model.postgres.teacher import Teacher
from src.model.postgres.class_enrollment import ClassEnrollment
from src.model.postgres.teaching_assignment import TeachingAssignment

T = TypeVar("T")

### ---------------------------------------------------------------------------------
### Single code
### ---------------------------------------------------------------------------------
class PostgresRepository(Repository[T], Generic[T]):
    model_cls: type[T]
    code: str
    field_ignores: Optional[list] = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, create_info: dict) -> Optional[T]:
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

    async def lookup_code(self, code: str) -> Optional[T]:
        result = self.session.query(self.model_cls.code) \
               .filter(self.model_cls.code == code).first()
        return True if result else False

    async def get(self, code: str) -> Optional[T]:
        if await self.lookup_code(code) is False:
            return None
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

    @staticmethod
    def create_code(academic_year: str) -> str:
        return f'NH{academic_year.replace("-", "").replace(" ", "")}'

class PostgresSemesterRepository(PostgresRepository[Semester]):
    model_cls = Semester
    code = "code"
    field_ignores = ["academic_year_code"]

class PostgresGradeLevelRepository(PostgresRepository[GradeLevel]):
    model_cls = GradeLevel
    code = "code"

    @staticmethod
    def create_code(class_room_name: str) -> str:
        return f"MK{settings.WORD2NUM[class_room_name.split(' ')[0]]:02}"

class PostgresClassRoomRepository(PostgresRepository[ClassRoom]):
    model_cls = ClassRoom
    code = "code"

    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.grade_level = PostgresGradeLevelRepository(session)

    @staticmethod
    def create_code(class_room_name: str, grade_level_code: str) -> str:
        result = class_room_name.split(" ")
        return f"{grade_level_code[-3:]}.ML{settings.WORD2SHORTCUT[result[0]]}{result[1]}"

    async def add(self, create_info: dict) -> Optional[ClassRoom]:
        if await self.grade_level.get(create_info.get("grade_level_code")) is None:
            raise ValueError("grade level is not found")
        return await super().add(create_info)

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

### ---------------------------------------------------------------------------------
### Composite code
### ---------------------------------------------------------------------------------
class PostgresCompositeRepository(Repository[T], Generic[T]):
    model_cls: type[T]

    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    async def create_code(self, info: dict) -> str:
        raise NotImplementedError

    @staticmethod
    def build_filters(self, code: str):
        raise NotImplementedError

    async def add(self, create_info: dict) -> Optional[T]:
        code = await self.create_code(create_info)
        exist = await self.get(code)
        if exist:
            return None
        entity = self.model_cls(**create_info)
        try:
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except Exception as e:
            self.session.rollback()
            raise e

    async def get(self, code: str) -> Optional[T]:
        stmt = select(self.model_cls).where(*self.build_filters(code))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[T]:
        stmt = select(self.model_cls)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

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

    async def update(self, identity_info: dict, update_info: dict) -> Optional[T]:
        code = await self.create_code(identity_info)
        entity = await self.get(code)
        if entity is None:
            return None
        entity_clone = entity.to_dict().copy()
        for field, value in update_info.items():
            if value is None:
                continue
            if hasattr(entity, field):
                setattr(entity, field, value)
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

class PostgresClassEnrollmentRepository(PostgresCompositeRepository[ClassEnrollment]):
    model_cls = ClassEnrollment

    def __init__(self, session):
        super().__init__(session)
        self.student = PostgresStudentRepository(session)
        self.class_room = PostgresClassRoomRepository(session)
        self.academic_year = PostgresAcademicYearRepository(session)
        self.semester = PostgresSemesterRepository(session)
        self.score = PostgresScoreRepository(session)
        self.subject = PostgresSubjectRepository(session)

    @staticmethod
    def parse_code(code: str) -> tuple[str, str, str, str, str, str]:
        parts = code.split("_")
        if len(parts) != 5:
            raise ValueError("Invalid composite code format")
        return parts[0], parts[1], parts[2], parts[3], parts[4], parts[6]

    async def create_code(self, info: dict) -> str:
        student_code = info.get("student_code")
        if await self.student.get(student_code) is None:
            raise ValueError("student code is not found")
        class_code = info.get("class_code")
        if await self.classroom.get(class_code) is None:
            raise ValueError("class code is not found")
        academic_year_code = info.get("academic_year_code")
        if await self.academic_year.get(academic_year_code) is None:
            raise ValueError("academic year code is not found")
        semester_code = info.get("semester_code")
        if await self.semester.get(semester_code) is None:
            raise ValueError("semester code is not found")
        score_code = info.get("score_code")
        if await self.score.get(score_code) is None:
            raise ValueError("score code is not found")
        subject_code = info.get("subject_code")
        if await self.subject.get(subject_code) is None:
            raise ValueError("subject code is not found")
        return f"{student_code}_{class_code}_{academic_year_code}_" \
               f"{semester_code}_{subject_code}"

    def build_filters(self, code: str):
        student_code, class_code, academic_year_code, \
        semester_code, score_code, subject_code = self.parse_code(code)
        return (
            self.model_cls.student_code == student_code,
            self.model_cls.class_code == class_code,
            self.model_cls.academic_year_code == academic_year_code,
            self.model_cls.semester_code == semester_code,
            self.model_cls.score_code == score_code,
            self.model_cls.subject_code == subject_code
        )

class PostgresTeachingAssignmentRepository(PostgresCompositeRepository[TeachingAssignment]):
    model_cls = TeachingAssignment

    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.teacher = PostgresTeacherRepository(session)
        self.class_room = PostgresClassRoomRepository(session)
        self.subject = PostgresSubjectRepository(session)

    @staticmethod
    def parse_code(code: str) -> tuple[str, str, str]:
        parts = code.split("_")
        if len(parts) != 3:
            raise ValueError("Invalid composite code format")
        return parts[0], parts[1], parts[2]

    async def create_code(self, info: dict) -> str:
        teacher_code = info.get("teacher_code")
        if await self.teacher.get(teacher_code) is None:
            raise ValueError("teacher code is not found")
        class_code = info.get("class_code")
        if await self.classroom.get(class_code) is None:
            raise ValueError("class code is not found")
        subject_code = info.get("subject_code")
        if await self.subject.get(subject_code) is None:
            raise ValueError("subject code is not found")
        return f"{teacher_code}_{class_code}_{subject_code}"

    def build_filters(self, code: str):
        teacher_code, class_code, subject_code = self.parse_code(code)
        return (
            self.model_cls.teacher_code == teacher_code,
            self.model_cls.class_code == class_code,
            self.model_cls.subject_code == subject_code
        )