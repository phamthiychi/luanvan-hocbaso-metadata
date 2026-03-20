from fastapi import APIRouter, HTTPException, Request

from src.adapter.api.template.class_enrollment import ClassEnrollmentCreate, ClassEnrollmentUpdate

router = APIRouter(prefix="/class-enrollments", tags=["class-enrollments"])

@router.get("/all")
async def get_class_enrollments(req: Request):
    repo = req.app.state.class_enrollment_repo
    return await repo.get_all()

@router.get("")
async def get_class_enrollment(payload: ClassEnrollmentUpdate, req: Request):
    repo = req.app.state.class_enrollment_repo
    code = await repo.create_code(payload.dict())
    doc = await repo.get(code)
    if not doc:
        raise HTTPException(status_code=404, detail="Class enrollment not found")
    return doc.to_dict()

@router.post("")
async def create_class_enrollment(payload: ClassEnrollmentCreate, req: Request):
    repo = req.app.state.class_enrollment_repo
    saved = await repo.add(payload.dict())
    if saved is None:
        raise HTTPException(status_code=409, detail="Already exists")
    return saved.to_dict()

@router.put("")
async def update_class_enrollment(payload: ClassEnrollmentUpdate, req: Request):
    repo = req.app.state.class_enrollment_repo
    update_class = await repo.update(payload.dict())
    if not update_class:
        raise HTTPException(status_code=404, detail="Class enrollment not found")
    return update_class.to_dict()

@router.delete("")
async def delete_class_enrollment(payload: ClassEnrollmentUpdate, req: Request):
    repo = req.app.state.class_enrollment_repo
    code = await repo.create_code(payload.dict())
    return await repo.delete(code)