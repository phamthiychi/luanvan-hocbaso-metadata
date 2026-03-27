from typing import List

from src.adapter.api.template.student import StudentCreate, StudentUpdate
from src.adapter.api.template.academic_year import AcademicYearCreate, AcademicYearUpdate
from src.adapter.api.template.grade_level import GradeLevelCreate, GradeLevelUpdate
from src.adapter.api.template.class_room import ClassRoomCreate, ClassRoomUpdate

from src.adapter.database.postgres_repository import (
    PostgresAcademicYearRepository,
    PostgresClassRoomRepository,
    PostgresGradeLevelRepository,
    PostgresScoreRepository,
    PostgresSemesterRepository,
    PostgresStudentRepository,
    PostgresSubjectRepository,
    PostgresTeacherRepository,
    PostgresClassEnrollmentRepository,
    PostgresTeachingAssignmentRepository
)
from src.adapter.ontology.neo4j_manager import Neo4jStudentAssessmentStore
from src.adapter.ontology.extract_assessment import AssessmentStudentExtractor

class SystemCore:
    def __init__(self, session):
        # Postgres database
        self.student_repo = PostgresStudentRepository(session)
        self.teacher_repo = PostgresTeacherRepository(session)
        self.subject_repo = PostgresSubjectRepository(session)
        self.semester_repo = PostgresSemesterRepository(session)
        self.score_repo = PostgresScoreRepository(session)
        self.class_room_repo = PostgresClassRoomRepository(session)
        self.grade_level_repo = PostgresGradeLevelRepository(session)
        self.academic_year_repo = PostgresAcademicYearRepository(session)
        self.class_enrollment_repo = PostgresClassEnrollmentRepository(session)
        self.teaching_assignment_repo = PostgresTeachingAssignmentRepository(session)
        # Neo4j database
        self.student_assessment_store = Neo4jStudentAssessmentStore()

    ## ------------------------ Interact with Neo4j database ------------------------
    # def update_student_assessments(self, file_student_comment_dir: str) -> None:
    #     student_assessment_reports = []
    #     extractor = AssessmentStudentExtractor()
    #     datas = read_comment_students(file_student_comment_dir)
    #     for data in datas:
    #         student_assessment_reports.append(
    #             extractor.analyze(data.get("student_id"),
    #                               data.get("comment")).to_dict())
    #     self.student_assessment_store.save_reports(student_assessment_reports)

    async def add_student(self, info: StudentCreate) -> dict:
        academic_year_code = self.academic_year_repo.create_code(info.academic_year)
        grade_level_code = self.grade_level_repo.create_code(info.class_name)
        class_room_code = self.class_room_repo.create_code(info.class_name, grade_level_code)
        academic_year_entity = await self.academic_year_repo.get(academic_year_code)
        grade_level_entity = await self.grade_level_repo.get(grade_level_code)
        class_room_entity = await self.class_room_repo.get(class_room_code)
        start_year, end_year = info.academic_year.split("-")
        if academic_year_entity is None:
            await self.academic_year_repo.add(AcademicYearCreate(
                code=academic_year_code,
                name=info.academic_year,
                start_date=f"{start_year.strip()}-01-01",
                end_date=f"{end_year.strip()}-01-01"
            ).dict())
        if grade_level_entity is None:
            await self.grade_level_repo.add(GradeLevelCreate(
                code=grade_level_code,
                name=f"Khối {int(grade_level_code.split('MK')[1])}",
                max_students=1
            ).dict())
        else:
            await self.grade_level_repo.update(GradeLevelUpdate(
                code=grade_level_code,
                max_students=grade_level_entity.max_students + 1
            ).dict())
        if class_room_entity is None:
            await self.class_room_repo.add(ClassRoomCreate(
                code=class_room_code,
                name=info.class_name,
                size=1,
                grade_level_code=grade_level_code
            ).dict())
        else:
            await self.class_room_repo.update(ClassRoomUpdate(
                code=class_room_code,
                size=class_room_entity.size + 1
            ).dict())
        student_entity = info.dict()
        student_entity.pop("academic_year", None)
        student_entity.pop("class_name", None)
        indexs = [0]
        indexs.extend([int(s.code.split(".")[-1]) for s in await self.student_repo.get_all()])
        student_entity["code"] = f"{academic_year_code[2:]}" \
                       f".{grade_level_code[-2:]}" \
                       f".{class_room_code[-3:]}.{(max(indexs) + 1):03}"
        return await self.student_repo.add(student_entity)

    async def find_student(self, code: str) -> dict:
        return await self.student_repo.get(code)

