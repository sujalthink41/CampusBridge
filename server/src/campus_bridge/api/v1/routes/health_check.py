from fastapi import APIRouter

router = APIRouter(tags=["Internal"])


@router.get("/health")
async def health():
    return {"status": "ok"}
