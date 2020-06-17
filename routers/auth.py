from fastapi import APIRouter


router = APIRouter()


@router.post("/login")
async def post_generate_token():
    return {"token": "genegate_jwt_token"}