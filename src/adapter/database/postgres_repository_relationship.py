from __future__ import annotations

from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.postgres.class_enrollment import ClassEnrollment
from src.model.postgres.teaching_assignment import TeachingAssignment
from src.model.postgres.learning_result import LearningResult
from src.interface.data import Repository

from src.adapter.database.postgres_repository import (
    PostgresAcademicYearRepository,
    PostgresClassRoomRepository,
    PostgresGradeLevelRepository,
    PostgresScoreRepository,
    PostgresSemesterRepository,
    PostgresStudentRepository,
    PostgresSubjectRepository,
    PostgresTeacherRepository
)

# app.state.student_repo = PostgresStudentRepository(session)
# app.state.teacher_repo = PostgresTeacherRepository(session)
# app.state.subject_repo = PostgresSubjectRepository(session)
# app.state.semester_repo = PostgresSemesterRepository(session)
# app.state.score_repo = PostgresScoreRepository(session)
# app.state.class_room_repo = PostgresClassRoomRepository(session)
# app.state.grade_level_repo = PostgresGradeLevelRepository(session)
# app.state.academic_year_repo = PostgresAcademicYearRepository(session)
# app.state.class_enrollment_repo = PostgresClassEnrollmentRepository(session)
# app.state.teaching_assignment_repo = PostgresTeachingAssignmentRepository(session)
# app.state.learning_result_repo = PostgresLearningResultRepository(session)

class PostgresClassEnrollmentRepository(Repository[ClassEnrollment]):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.student = PostgresStudentRepository(session)
        self.classroom = PostgresClassRoomRepository(session)
        self.grade_level = PostgresGradeLevelRepository(session)
        self.academic_year = PostgresAcademicYearRepository(session)
        self.semester = PostgresSemesterRepository(session)

    @staticmethod
    def parse_code(code: str) -> tuple[str, str, str, str]:
        parts = code.split("_")
        return parts[0], parts[1], parts[2], parts[3], parts[4]

    async def create_code(self, info: dict) -> str:
        student_id = info.get("student_id")
        if await self.student.get(student_id) is None:
            raise ValueError("student id is not found")
        class_id = info.get("class_id")
        if await self.classroom.get(class_id) is None:
            raise ValueError("class id is not found")
        grade_level_id = info.get("grade_level_id")
        if await self.grade_level.get(grade_level_id) is None:
            raise ValueError("grade level id is not found")
        academic_year_id = info.get("academic_year_id")
        if await self.academic_year.get(academic_year_id) is None:
            raise ValueError("academic year id is not found")
        semester_id = info.get("semester_id")
        if await self.semester.get(semester_id) is None:
            raise ValueError("semester id is not found")
        return f"{student_id}_{class_id}_{grade_level_id}_{academic_year_id}_{semester_id}"

    async def add(self, create_info: dict) -> ClassEnrollment:
        entity = ClassEnrollment(**create_info)
        code = await self.create_code(create_info)
        exist = await self.get(code)
        if exist:
            return exist
        try:
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except Exception as e:
            self.session.rollback()
            return e

    async def get(self, code: str) -> Optional[ClassEnrollment]:
        student_id, class_id, grade_level_id, academic_year_id, semester_id = self.parse_code(code)
        filters = (
            ClassEnrollment.student_id == student_id,
            ClassEnrollment.class_id == class_id,
            ClassEnrollment.grade_level_id == grade_level_id,
            ClassEnrollment.academic_year_id == academic_year_id,
            ClassEnrollment.semester_id == semester_id,
        )
        stmt = select(ClassEnrollment).where(*filters)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> Optional[list[ClassEnrollment]]:
        return self.session.query(ClassEnrollment).all()

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
            return e

    async def update(self, update_info: dict) -> Optional[ClassEnrollment]:
        code = await self.create_code(update_info)
        entity = await self.get(code)
        if entity is None:
            return None
        for field, value in update_info.items():
            if value is None:
                continue
            if hasattr(entity, field):
                setattr(entity, field, value)
        try:
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except Exception as e:
            self.session.rollback()
            return e

class PostgresTeachingAssignmentRepository(Repository[TeachingAssignment]):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.teacher = PostgresTeacherRepository(session)
        self.classroom = PostgresClassRoomRepository(session)
        self.subject = PostgresSubjectRepository(session)
        self.academic_year = PostgresAcademicYearRepository(session)
        self.semester = PostgresSemesterRepository(session)

    @staticmethod
    def parse_code(code: str) -> tuple[str, str, str, str, str]:
        parts = code.split("_")
        return parts[0], parts[1], parts[2], parts[3], parts[4]

    async def create_code(self, info: dict) -> str:
        teacher_id = info.get("teacher_id")
        if await self.teacher.get(teacher_id) is None:
            raise ValueError("teacher id is not found")
        class_id = info.get("class_id")
        if await self.classroom.get(class_id) is None:
            raise ValueError("class id is not found")
        subject_id = info.get("subject_id")
        if await self.subject.get(subject_id) is None:
            raise ValueError("subject id is not found")
        academic_year_id = info.get("academic_year_id")
        if await self.academic_year.get(academic_year_id) is None:
            raise ValueError("academic year id is not found")
        semester_id = info.get("semester_id")
        if await self.semester.get(semester_id) is None:
            raise ValueError("semester id is not found")
        return f"{teacher_id}_{class_id}_{subject_id}_{academic_year_id}_{semester_id}"

    async def add(self, create_info: dict) -> TeachingAssignment:
        entity = TeachingAssignment(**create_info)
        code = await self.create_code(create_info)
        exist = await self.get(code)
        if exist:
            return exist
        try:
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except Exception as e:
            self.session.rollback()
            return e

    async def get(self, code: str) -> Optional[TeachingAssignment]:
        teacher_id, class_id, subject_id, academic_year_id, semester_id = self.parse_code(code)
        filters = (
            TeachingAssignment.teacher_id == teacher_id,
            TeachingAssignment.class_id == class_id,
            TeachingAssignment.subject_id == subject_id,
            TeachingAssignment.academic_year_id == academic_year_id,
            TeachingAssignment.semester_id == semester_id,
        )
        stmt = select(TeachingAssignment).where(*filters)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> Optional[list[TeachingAssignment]]:
        return self.session.query(TeachingAssignment).all()

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
            return e

    async def update(self, update_info: dict) -> Optional[TeachingAssignment]:
        code = await self.create_code(update_info)
        entity = await self.get(code)
        if entity is None:
            return None
        for field, value in update_info.items():
            if value is None:
                continue
            if hasattr(entity, field):
                setattr(entity, field, value)
        try:
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except Exception as e:
            self.session.rollback()
            return e

class PostgresLearningResultRepository(Repository[LearningResult]):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.student = PostgresStudentRepository(session)
        self.classroom = PostgresClassRoomRepository(session)
        self.academic_year = PostgresAcademicYearRepository(session)
        self.semester = PostgresSemesterRepository(session)
        self.subject = PostgresSubjectRepository(session)
        self.score = PostgresScoreRepository(session)

    @staticmethod
    def parse_code(code: str) -> tuple[str, str, str, str, str, str]:
        parts = code.split("_")
        return parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]

    async def create_code(self, info: dict) -> str:
        student_id = info.get("student_id")
        if await self.student.get(student_id) is None:
            raise ValueError("student id is not found")
        class_id = info.get("class_id")
        if await self.classroom.get(class_id) is None:
            raise ValueError("class id is not found")
        academic_year_id = info.get("academic_year_id")
        if await self.academic_year.get(academic_year_id) is None:
            raise ValueError("academic year id is not found")
        semester_id = info.get("semester_id")
        if await self.semester.get(semester_id) is None:
            raise ValueError("semester id is not found")
        subject_id = info.get("subject_id")
        if await self.subject.get(subject_id) is None:
            raise ValueError("subject id is not found")
        score_id = info.get("score_id")
        if await self.score.get(score_id) is None:
            raise ValueError("score id is not found")
        return f"{student_id}_{class_id}_{academic_year_id}_{semester_id}_{subject_id}_{score_id}"

    async def add(self, create_info: dict) -> LearningResult:
        entity = LearningResult(**create_info)
        code = await self.create_code(create_info)
        exist = await self.get(code)
        if exist:
            return exist
        try:
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except Exception as e:
            self.session.rollback()
            return e

    async def get(self, code: str) -> Optional[LearningResult]:
        student_id, class_id, academic_year_id, semester_id, subject_id, score_id = self.parse_code(code)
        filters = (
            LearningResult.student_id == student_id,
            LearningResult.class_id == class_id,
            LearningResult.academic_year_id == academic_year_id,
            LearningResult.semester_id == semester_id,
            LearningResult.subject_id == subject_id,
            LearningResult.score_id == score_id,
        )
        stmt = select(LearningResult).where(*filters)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> Optional[list[LearningResult]]:
        return self.session.query(LearningResult).all()

    async def delete(self, code: str) -> bool:
        entity = await self.get(code)
        if entity is None:
            return False
        try:
            self.session.delete(entity)
            self.session.commit()
            return entity
        except Exception as e:
            self.session.rollback()
            return e

    async def update(self, update_info: dict) -> Optional[LearningResult]:
        code = await self.create_code(update_info)
        entity = await self.get(code)
        if entity is None:
            return None
        for field, value in update_info.items():
            if value is None:
                continue
            if hasattr(entity, field):
                setattr(entity, field, value)
        try:
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except Exception as e:
            self.session.rollback()
            return e
