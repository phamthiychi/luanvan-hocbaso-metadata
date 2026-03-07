from fastapi import FastAPI

from src.adapter.database.mongo_manager import mongo_manager
from src.adapter.database.mongo_repository import (
    MongoStudentRepository,
    MongoTeacherRepository,
    MongoSubjectRepository,
    MongoSemesterRepository,
    MongoScoreRepository,
    MongoClassRepository,
    MongoGradeLevelRepository,
    MongoAcademicYearRepository
)

from src.adapter.api.routers.student import router as student_router
from src.adapter.api.routers.teacher import router as teacher_router
from src.adapter.api.routers.subject import router as subject_router
from src.adapter.api.routers.semester import router as semester_router
from src.adapter.api.routers.score import router as score_router
from src.adapter.api.routers.school_class import router as school_class_router
from src.adapter.api.routers.grade_level import router as grade_level_router
from src.adapter.api.routers.academic_year import router as academic_year_router

app = FastAPI(title="HOCBASO API")

@app.on_event("startup")
async def startup():
    db = mongo_manager.get_core_db()
    app.state.student_repo = MongoStudentRepository(db)
    app.state.teacher_repo = MongoTeacherRepository(db)
    app.state.subject_repo = MongoSubjectRepository(db)
    app.state.semester_repo = MongoSemesterRepository(db)
    app.state.score_repo = MongoScoreRepository(db)
    app.state.school_class_repo = MongoClassRepository(db)
    app.state.grade_level_repo = MongoGradeLevelRepository(db)
    app.state.academic_year_repo = MongoAcademicYearRepository(db)

@app.get("/health")
async def health():
    try:
        mongo_manager.admin.command("ping")  # kiểm tra Mongo hoạt động
        return {
            "status": "200 ok",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "504 error",
            "database": "disconnected",
            "error": e
        }

app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(subject_router)
app.include_router(semester_router)
app.include_router(score_router)
app.include_router(school_class_router)
app.include_router(grade_level_router)
app.include_router(academic_year_router)