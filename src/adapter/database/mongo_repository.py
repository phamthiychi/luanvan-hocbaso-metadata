from typing import Generic, Optional, Type, TypeVar

from src.interface.data import Repository
from src.model.student import Student
from src.model.teacher import Teacher
from src.model.subject import Subject
from src.model.semester import Semester
from src.model.score import Score
from src.model.school_class import SchoolClass
from src.model.grade_level import GradeLevel
from src.model.academic_year import AcademicYear

T = TypeVar("T")

class MongoRepositoryBase(Repository[T], Generic[T]):
    collection_name: str
    model_cls: Type[T]

    def __init__(self, db):
        self.db = db
        self.col = db[self.collection_name]

    async def get(self, code: str) -> Optional[T]:
        doc = self.col.find_one({"code": code})
        return None if not doc else self.model_cls.from_dict(doc)

    async def add(self, entity: T) -> T:
        student_exist = await self.get(entity.code)
        if student_exist:
            return student_exist
        result = self.col.insert_one(entity.to_dict())
        doc = self.col.find_one({"_id": result.inserted_id})
        return self.model_cls.from_dict(doc)

    async def delete(self, code: str) -> bool:
        delete_result = self.col.delete_one({"code": code})
        return delete_result.deleted_count > 0

    async def update(self, update_info: dict) -> T | None:
        update_data = {}
        code = update_info.get("code")
        update_info.pop("code", None)
        if "other_info" in update_info.keys():
            update_data = {"other_info": update_info.get("other_info")}
            update_info.pop("other_info", None)
        for key, value in update_info.items():
            if not value:
                continue
            update_data[f"data.{key}"] = value
        update_result = self.col.update_one(
            {"code": code},
            {"$set": update_data}
        )
        if update_result.matched_count == 0:
            return None
        updated_doc = self.col.find_one({"code": code})
        return self.model_cls.from_dict(updated_doc)

class MongoStudentRepository(MongoRepositoryBase[Student]):
    collection_name = "students"
    model_cls = Student

class MongoTeacherRepository(MongoRepositoryBase[Teacher]):
    collection_name = "teachers"
    model_cls = Teacher

class MongoSubjectRepository(MongoRepositoryBase[Subject]):
    collection_name = "subjects"
    model_cls = Subject

class MongoSemesterRepository(MongoRepositoryBase[Semester]):
    collection_name = "semesters"
    model_cls = Semester

class MongoScoreRepository(MongoRepositoryBase[Score]):
    collection_name = "scores"
    model_cls = Score

class MongoClassRepository(MongoRepositoryBase[SchoolClass]):
    collection_name = "classes"
    model_cls = SchoolClass

class MongoGradeLevelRepository(MongoRepositoryBase[GradeLevel]):
    collection_name = "grade_levels"
    model_cls = GradeLevel

class MongoAcademicYearRepository(MongoRepositoryBase[AcademicYear]):
    collection_name = "academic_years"
    model_cls = AcademicYear
