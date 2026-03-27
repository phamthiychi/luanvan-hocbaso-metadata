from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text

from src.adapter.database.postges_manager import postgres_manager
from src.application.core import SystemCore

from src.adapter.api.routers.student import router as student_router
from src.adapter.api.routers.teacher import router as teacher_router
from src.adapter.api.routers.subject import router as subject_router
from src.adapter.api.routers.semester import router as semester_router
from src.adapter.api.routers.score import router as score_router
from src.adapter.api.routers.class_room import router as class_room_router
from src.adapter.api.routers.grade_level import router as grade_level_router
from src.adapter.api.routers.academic_year import router as academic_year_router
from src.adapter.api.routers.class_enrollment import router as class_enrollment_router
from src.adapter.api.routers.teaching_assignment import router as teaching_assignment_router

app = FastAPI(title="HOCBASO API - POSTGRES")

@app.on_event("startup")
async def startup():
    session = postgres_manager.session
    app.state.core = SystemCore(session)

@app.get("/health")
async def health():
    try:
        postgres_manager.session.execute(text("SELECT 1"))
        print("✅ Database connected")
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
    finally:
        postgres_manager.session.close()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "500 error",
            "error": str(exc)
        }
    )

app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(subject_router)
app.include_router(semester_router)
app.include_router(score_router)
app.include_router(class_room_router)
app.include_router(grade_level_router)
app.include_router(academic_year_router)
app.include_router(class_enrollment_router)
app.include_router(teaching_assignment_router)