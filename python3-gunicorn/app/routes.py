from fastapi import APIRouter, Response

router = APIRouter()


@router.get("/healthcheck", response_class=Response)
async def get_healthcheck() -> None:
    return None

@router.get("/")
async def read_root():
    return {"message": "Hello, World!"}
