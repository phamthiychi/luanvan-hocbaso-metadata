from fastapi import APIRouter, HTTPException, Request

from src.model.school_class import SchoolClass
from src.adapter.api.template.school_class import SchoolClassCreate, SchoolClassUpdate

router = APIRouter(prefix="/classes", tags=["classes"])

@router.get("")
async def get_classes(req: Request):
    repo = req.app.state.school_class_repo
    classes = []
    for doc in repo.col.find():
        doc["_id"] = str(doc["_id"])
        classes.append(doc)
    return classes

@router.get("/{code}")
async def get_class(code: str, req: Request):
    repo = req.app.state.school_class_repo
    doc = await repo.get(code)
    if not doc:
        raise HTTPException(status_code=404, detail="Class not found")
    return doc.to_dict()

@router.post("")
async def create_class(payload: SchoolClassCreate, req: Request):
    repo = req.app.state.school_class_repo
    school_class = SchoolClass(
        code=payload.code,
        name=payload.name,
        size=payload.size,
        grade_level_id=payload.grade_level_id,
        academic_year_id=payload.academic_year_id,
        special_program=payload.special_program,
    )
    saved = await repo.add(school_class)
    return saved.to_dict()

@router.put("")
async def update_class(payload: SchoolClassUpdate, req: Request):
    if not isinstance(payload.code, str):
        raise HTTPException(status_code=400, detail="Invalid ID")
    repo = req.app.state.school_class_repo
    update_class = await repo.update(payload.dict())
    if not update_class:
        raise HTTPException(status_code=404, detail="Class not found")
    return update_class.to_dict()

@router.delete("/{code}")
async def delete_class(code: str, req: Request):
    repo = req.app.state.school_class_repo
    return await repo.delete(code)