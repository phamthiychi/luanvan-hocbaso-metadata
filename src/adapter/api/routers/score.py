from fastapi import APIRouter, HTTPException, Request

from src.model.score import Score
from src.adapter.api.template.score import ScoreCreate, ScoreUpdate

router = APIRouter(prefix="/scores", tags=["scores"])

@router.get("")
async def get_scores(req: Request):
    repo = req.app.state.score_repo
    scores = []
    for doc in repo.col.find():
        doc["_id"] = str(doc["_id"])
        scores.append(doc)
    return scores

@router.get("/{code}")
async def get_score(code: str, req: Request):
    repo = req.app.state.score_repo
    doc = await repo.get(code)
    if not doc:
        raise HTTPException(status_code=404, detail="Score not found")
    return doc.to_dict()

@router.post("")
async def create_score(payload: ScoreCreate, req: Request):
    repo = req.app.state.score_repo
    score = Score(
        code=payload.code,
        name=payload.name,
        description=payload.description,
    )
    saved = await repo.add(score)
    return saved.to_dict()

@router.put("")
async def update_score(payload: ScoreUpdate, req: Request):
    if not isinstance(payload.code, str):
        raise HTTPException(status_code=400, detail="Invalid ID")
    repo = req.app.state.score_repo
    update_score = await repo.update(payload.dict())
    if not update_score:
        raise HTTPException(status_code=404, detail="Score not found")
    return update_score.to_dict()

@router.delete("/{code}")
async def delete_score(code: str, req: Request):
    repo = req.app.state.score_repo
    return await repo.delete(code)