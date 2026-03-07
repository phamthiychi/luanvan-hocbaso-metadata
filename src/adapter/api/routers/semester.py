from fastapi import APIRouter, HTTPException, Request

from src.model.semester import Semester
from src.adapter.api.template.semester import SemesterCreate, SemesterUpdate

router = APIRouter(prefix="/semesters", tags=["semesters"])

@router.get("")
async def get_semesters(req: Request):
    repo = req.app.state.semester_repo
    semesters = []
    for doc in repo.col.find():
        doc["_id"] = str(doc["_id"])
        semesters.append(doc)
    return semesters

@router.get("/{code}")
async def get_semester(code: str, req: Request):
    repo = req.app.state.semester_repo
    doc = await repo.get(code)
    if not doc:
        raise HTTPException(status_code=404, detail="Semester not found")
    return doc.to_dict()
@router.post("")
async def create_semester(payload: SemesterCreate, req: Request):
    repo = req.app.state.semester_repo
    semester = Semester(
        code=payload.code,
        name=payload.name,
        start_date=payload.start_date,
        end_date=payload.end_date,
        academic_year_id=payload.academic_year_id,
    )
    saved = await repo.add(semester)
    return saved.to_dict()

@router.put("")
async def update_semester(payload: SemesterUpdate, req: Request):
    if not isinstance(payload.code, str):
        raise HTTPException(status_code=400, detail="Invalid ID")
    repo = req.app.state.semester_repo
    update_semester = await repo.update(payload.dict())
    if not update_semester:
        raise HTTPException(status_code=404, detail="Semester not found")
    return update_semester.to_dict()

@router.delete("/{code}")
async def delete_semester(code: str, req: Request):
    repo = req.app.state.semester_repo
    return await repo.delete(code)