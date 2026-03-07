from fastapi import APIRouter, HTTPException, Request

from src.model.student import Student
from src.adapter.api.template.student import StudentCreate, StudentUpdate

router = APIRouter(prefix="/students", tags=["students"])

@router.get("")
async def get_students(req: Request):
    repo = req.app.state.student_repo
    students = []
    for doc in repo.col.find():
        doc["_id"] = str(doc["_id"])
        students.append(doc)
    return students

@router.get("/{code}")
async def get_student(code: str, req: Request):
    if not isinstance(code, str):
        raise HTTPException(status_code=400, detail="Invalid ID")
    repo = req.app.state.student_repo
    doc = await repo.get(code)
    if not doc:
        raise HTTPException(status_code=404, detail="Student not found")
    return doc.to_dict()

@router.post("")
async def create_student(payload: StudentCreate, req: Request):
    repo = req.app.state.student_repo
    student = Student(
        code=payload.code,
        name=payload.name,
        date_of_birth=payload.date_of_birth,
        gender=payload.gender,
        nationality=payload.nationality,
        card_id=payload.card_id,
        edu_id=payload.edu_id,
        status=payload.status,
        phone=payload.phone,
        address=payload.address,
        other_info=payload.other_info
    )
    saved = await repo.add(student)
    return saved.to_dict()

@router.put("")
async def update_student(payload: StudentUpdate, req: Request):
    if not isinstance(payload.code, str):
        raise HTTPException(status_code=400, detail="Invalid ID")
    repo = req.app.state.student_repo
    update_student = await repo.update(payload.dict())
    if not update_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return update_student.to_dict()

@router.delete("/{code}")
async def delete_student(code :str, req: Request):
    if not isinstance(code, str):
        raise HTTPException(status_code=400, detail="Invalid ID")
    repo = req.app.state.student_repo
    return await repo.delete(code)