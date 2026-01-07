from fastapi import APIRouter

router = APIRouter(
    prefix="",
    tags=["api/v1/sample"],
    responses={404: {"description": "Not found"}},
)

@router.get("")
async def get_sample():
    return {"message": "Hello World"}
