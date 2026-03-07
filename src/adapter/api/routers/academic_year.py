from fastapi import APIRouter, HTTPException, Request

from src.model.academic_year import AcademicYear
from src.adapter.api.template.academic_year import AcademicYearCreate, AcademicYearUpdate

router = APIRouter(prefix="/academic-years", tags=["academic-years"])

@router.get("")
async def get_academic_years(req: Request):
    repo = req.app.state.academic_year_repo
    academic_years = []
    for doc in repo.col.find():
        doc["_id"] = str(doc["_id"])
        academic_years.append(doc)
    return academic_years

@router.get("/{code}")
async def get_academic_year(code: str, req: Request):
    repo = req.app.state.academic_year_repo
    doc = await repo.get(code)
    if not doc:
        raise HTTPException(status_code=404, detail="Academic year not found")
    return doc.to_dict()

@router.post("")
async def create_academic_year(payload: AcademicYearCreate, req: Request):
    repo = req.app.state.academic_year_repo
    academic_year = AcademicYear(
        code=payload.code,
        name=payload.name,
        start_date=payload.start_date,
        end_date=payload.end_date,
    )
    saved = await repo.add(academic_year)
    return saved.to_dict()


@router.put("")
async def update_academic_year(payload: AcademicYearUpdate, req: Request):
    if not isinstance(payload.code, str):
        raise HTTPException(status_code=400, detail="Invalid ID")
    repo = req.app.state.academic_year_repo
    update_academic_year = await repo.update(payload.dict())
    if not update_academic_year:
        raise HTTPException(status_code=404, detail="AcademicYear not found")
    return update_academic_year.to_dict()

@router.delete("/{code}")
async def delete_academic_year(code: str, req: Request):
    repo = req.app.state.academic_year_repo
    return await repo.delete(code)