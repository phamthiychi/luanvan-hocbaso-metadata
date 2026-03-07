from fastapi import APIRouter, HTTPException, Request

from src.model.subject import Subject
from src.adapter.api.template.subject import SubjectCreate, SubjectUpdate

router = APIRouter(prefix="/subjects", tags=["subjects"])

@router.get("")
async def get_subjects(req: Request):
    repo = req.app.state.subject_repo
    subjects = []
    for doc in repo.col.find():
        doc["_id"] = str(doc["_id"])
        subjects.append(doc)
    return subjects

@router.get("/{code}")
async def get_subject(code: str, req: Request):
    if not isinstance(code, str):
        raise HTTPException(status_code=400, detail="Invalid code")
    repo = req.app.state.subject_repo
    doc = await repo.get(code)
    if not doc:
        raise HTTPException(status_code=404, detail="Subject not found")
    return doc.to_dict()

@router.post("")
async def create_subject(payload: SubjectCreate, req: Request):
    repo = req.app.state.subject_repo

    subject = Subject(
        code=payload.code,
        name=payload.name,
        total_periods=payload.total_periods,
    )
    saved = await repo.add(subject)
    return saved.to_dict()

@router.put("")
async def update_subject(payload: SubjectUpdate, req: Request):
    if not isinstance(payload.code, str):
        raise HTTPException(status_code=400, detail="Invalid code")
    repo = req.app.state.subject_repo
    updated_subject = await repo.update(payload.dict())
    if not updated_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return updated_subject.to_dict()

@router.delete("/{code}")
async def delete_subject(code: str, req: Request):
    if not isinstance(code, str):
        raise HTTPException(status_code=400, detail="Invalid code")
    repo = req.app.state.subject_repo
    return await repo.delete(code)