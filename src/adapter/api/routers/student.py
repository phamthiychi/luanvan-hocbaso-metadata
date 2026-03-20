from fastapi import APIRouter, HTTPException, Request

from src.adapter.api.template.student import StudentCreate, StudentUpdate

router = APIRouter(prefix="/students", tags=["students"])

@router.get("")
async def get_students(req: Request):
    repo = req.app.state.student_repo
    return await repo.get_all()

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
    saved = await repo.add(payload.dict())
    if saved is None:
        raise HTTPException(status_code=409, detail="Already exists")
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