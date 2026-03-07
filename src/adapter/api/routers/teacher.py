from fastapi import APIRouter, HTTPException, Request

from src.model.teacher import Teacher
from src.adapter.api.template.teacher import TeacherCreate, TeacherUpdate

router = APIRouter(prefix="/teachers", tags=["teachers"])

@router.get("")
async def get_teachers(req: Request):
    repo = req.app.state.teacher_repo
    teachers = []
    for doc in repo.col.find():
        doc["_id"] = str(doc["_id"])
        teachers.append(doc)
    return teachers

@router.get("/{code}")
async def get_teacher(code: str, req: Request):
    if not isinstance(code, str):
        raise HTTPException(status_code=400, detail="Invalid code")
    repo = req.app.state.teacher_repo
    doc = await repo.get(code)
    if not doc:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return doc.to_dict()

@router.post("")
async def create_teacher(payload: TeacherCreate, req: Request):
    repo = req.app.state.teacher_repo
    teacher = Teacher(
        code=payload.code,
        name=payload.name,
        date_of_birth=payload.date_of_birth,
        gender=payload.gender,
        status=payload.status,
        phone=payload.phone,
        nationality=payload.nationality,
        specialization=payload.specialization,
        position=payload.position,
    )
    saved = await repo.add(teacher)
    return saved.to_dict()

@router.put("")
async def update_teacher(payload: TeacherUpdate, req: Request):
    if not isinstance(payload.code, str):
        raise HTTPException(status_code=400, detail="Invalid code")
    repo = req.app.state.teacher_repo
    updated_teacher = await repo.update(payload.dict())
    if not updated_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return updated_teacher.to_dict()

@router.delete("/{code}")
async def delete_teacher(code: str, req: Request):
    if not isinstance(code, str):
        raise HTTPException(status_code=400, detail="Invalid code")
    repo = req.app.state.teacher_repo
    return await repo.delete(code)